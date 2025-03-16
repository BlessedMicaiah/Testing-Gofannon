#!/usr/bin/env python3
"""
Enhanced Backend server for AI Agent Interface
This script creates a Flask server that interfaces with the advanced_agent.py functionality
with a focus on Google Search for research paper results
"""
import os
import sys
import logging
import traceback
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Check environment variables for feature flags
USE_ADVANCED_AGENT = os.getenv("USE_ADVANCED_AGENT", "true").lower() == "true"
ENABLE_ENHANCED_ARXIV = os.getenv("ENABLE_ENHANCED_ARXIV", "true").lower() == "true"

logger.info(f"USE_ADVANCED_AGENT: {USE_ADVANCED_AGENT}")
logger.info(f"ENABLE_ENHANCED_ARXIV: {ENABLE_ENHANCED_ARXIV}")

# Import the enhanced ArXiv search if enabled
enhanced_search = None
if ENABLE_ENHANCED_ARXIV:
    try:
        logger.info("Importing EnhancedArxivSearch...")
        from enhanced_arxiv import EnhancedArxivSearch
        enhanced_search = EnhancedArxivSearch()
        logger.info("Successfully imported EnhancedArxivSearch")
    except ImportError as e:
        logger.warning(f"Failed to import EnhancedArxivSearch: {str(e)}")
        enhanced_search = None

# Import the appropriate agent based on configuration
if USE_ADVANCED_AGENT:
    logger.info("Importing AdvancedAgent...")
    from advanced_agent import AdvancedAgent
    agent_class = AdvancedAgent
    logger.info("Successfully imported AdvancedAgent")
else:
    logger.info("Importing SimplifiedAgent (USE_ADVANCED_AGENT is disabled)...")
    from simplified_agent import SimplifiedAgent
    agent_class = SimplifiedAgent
    logger.info("Successfully imported SimplifiedAgent")

app = Flask(__name__, static_folder='advanced_agent_interface/backend/static')
CORS(app)  # Enable CORS for all routes

# Initialize the Agent
logger.info(f"Initializing {agent_class.__name__}...")
agent = agent_class()

@app.route('/')
def index():
    """Serve the simple UI HTML file as the default endpoint"""
    logger.info("Serving index page")
    return send_from_directory('advanced_agent_interface/backend/static', 'simple-ui.html')
    
@app.route('/api')
def api_info():
    """Return API information"""
    logger.info("API info requested")
    api_endpoints = {
        "message": "Welcome to the AI Agent API",
        "endpoints": {
            "/api/agent": "Submit a query to the agent",
            "/api/search": "Search for research papers",
            "/api/tools": "Get information about available tools"
        }
    }
    return jsonify(api_endpoints)

@app.route('/api/agent', methods=['POST'])
def query_agent():
    """Route to handle general agent queries"""
    data = request.json
    query = data.get('query', '')
    
    logger.info(f"Agent query received: {query}")
    
    if not query:
        logger.warning("Empty query received")
        return jsonify({'error': 'Query is required'}), 400
    
    try:
        # Process the query using our agent
        logger.info(f"Processing query with {agent_class.__name__}")
        
        # Use the appropriate method based on the agent type
        if hasattr(agent, 'process_query'):
            # SimplifiedAgent
            result = agent.process_query(query)
        else:
            # AdvancedAgent
            result = agent.run(query)
            
        logger.info(f"Agent response: {result}")
        return jsonify({'response': result})
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}", exc_info=True)
        error_trace = traceback.format_exc()
        logger.error(f"Traceback: {error_trace}")
        return jsonify({'error': str(e), 'traceback': error_trace}), 500

@app.route('/api/search', methods=['POST'])
def search_papers():
    """Route to search for research papers"""
    data = request.json
    query = data.get('query', '')
    max_results = data.get('max_results', 5)
    include_abstracts = data.get('include_abstracts', True)
    
    logger.info(f"Research paper search query received: {query}")
    
    if not query:
        logger.warning("Empty search query received")
        return jsonify({'error': 'Query is required'}), 400
    
    try:
        # Use the enhanced ArXiv search if available
        if enhanced_search:
            logger.info(f"Processing search query with EnhancedArxivSearch")
            results = enhanced_search.search(
                query=query,
                max_results=max_results,
                include_abstracts=include_abstracts
            )
            logger.info(f"Enhanced search returned {len(results)} results")
            return jsonify({'results': results})
        
        # Fall back to the agent's search if enhanced search is not available
        elif isinstance(agent, AdvancedAgent):
            # AdvancedAgent
            logger.info(f"Processing search query with AdvancedAgent")
            try:
                # Parse the query for knowledge search
                parsed_query = agent._parse_knowledge_query(query)
                logger.info(f"Parsed knowledge query: {parsed_query}")
                
                # Execute the search
                results = agent.execute_knowledge(parsed_query)
                logger.info(f"Got {len(results.get('entries', []))} search results")
                
                # Format the results for frontend
                formatted_results = []
                if 'entries' in results:
                    for entry in results['entries']:
                        formatted_results.append({
                            'title': entry.get('title', 'Untitled'),
                            'authors': ', '.join(entry.get('authors', ['Unknown'])),
                            'summary': entry.get('summary', 'No summary available'),
                            'link': entry.get('link', ''),
                            'published': entry.get('published', '')
                        })
                
                return jsonify({'results': formatted_results})
            except Exception as inner_e:
                logger.error(f"Error in AdvancedAgent search: {str(inner_e)}", exc_info=True)
                # Fall back to text query if knowledge search fails
                search_query = "search for " + query
                result = agent.run(search_query)
                logger.info(f"Fallback search response: {result}")
                return jsonify({'results': result})
    except Exception as e:
        logger.error(f"Error processing search query: {str(e)}", exc_info=True)
        error_trace = traceback.format_exc()
        logger.error(f"Traceback: {error_trace}")
        return jsonify({'error': str(e), 'traceback': error_trace}), 500

@app.route('/api/tools', methods=['GET'])
def get_tools():
    """Route to get available tools information"""
    logger.info("Tools info requested")
    try:
        # Get tools info based on the agent type
        if hasattr(agent, 'available_tools'):
            # SimplifiedAgent
            tools_info = {
                'available': agent.available_tools
            }
        else:
            # AdvancedAgent
            tools_info = {
                'math': list(agent.math_tools.keys()) if hasattr(agent, 'math_tools') else [],
                'reasoning': list(agent.reasoning_tools.keys()) if hasattr(agent, 'reasoning_tools') else [],
                'knowledge': list(agent.knowledge_tools.keys()) if hasattr(agent, 'knowledge_tools') else [],
                'available': {
                    'math': True,
                    'reasoning': hasattr(agent, 'reasoning_tools'),
                    'knowledge': hasattr(agent, 'knowledge_tools'),
                    'enhanced_search': enhanced_search is not None
                }
            }
            
        logger.info(f"Tools info: {tools_info}")
        return jsonify(tools_info)
    except Exception as e:
        logger.error(f"Error getting tools info: {str(e)}", exc_info=True)
        error_trace = traceback.format_exc()
        return jsonify({'error': str(e), 'traceback': error_trace}), 500

@app.route('/static/<path:path>')
def serve_static(path):
    """Serve static files"""
    logger.info(f"Serving static file: {path}")
    return send_from_directory('advanced_agent_interface/backend/static', path)

if __name__ == '__main__':
    logger.info(f"Starting {agent_class.__name__} Backend Server...")
    # Get port from environment variable for Render compatibility
    port = int(os.environ.get("PORT", 5000))
    # In production, don't use debug mode and bind to 0.0.0.0
    logger.info(f"Server will run on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False if os.environ.get("RENDER") else True)
