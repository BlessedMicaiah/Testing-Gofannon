#!/usr/bin/env python3
"""
Backend server for Advanced AI Agent Interface
This script creates a Flask server that interfaces with the advanced_agent.py functionality
"""
import sys
import os
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Add parent directory to path so we can import the advanced_agent module
# Fix the import path to point to the root directory where advanced_agent.py is located
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from advanced_agent import AdvancedAgent

app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for all routes

# Initialize the Advanced Agent
agent = AdvancedAgent()

@app.route('/')
def index():
    """Serve the simple UI HTML file as the default endpoint"""
    return send_from_directory('static', 'simple-ui.html')
    
# Return API information if JSON is accepted
@app.route('/api')
def api_info():
    """Return API information"""
    api_endpoints = {
        "message": "Welcome to the Advanced Agent API",
        "endpoints": {
            "/api/agent": "Submit a query to the advanced agent",
            "/api/search": "Search for academic papers",
            "/api/tools": "Get information about available tools"
        }
    }
    return jsonify(api_endpoints)

@app.route('/api/agent', methods=['POST'])
def query_agent():
    """Route to handle general agent queries"""
    data = request.json
    query = data.get('query', '')
    
    if not query:
        return jsonify({'error': 'Query is required'}), 400
    
    try:
        # Determine query type and process using the appropriate method
        query_type = agent._determine_query_type(query)
        result = ""
        
        if query_type == "math":
            parsed_query = agent._parse_math_query(query)
            result = agent.execute_math(parsed_query)
        elif query_type == "reasoning":
            parsed_query = {"topic": query, "steps": 3}
            result = agent.execute_reasoning(parsed_query)
            if isinstance(result, dict) and "reasoning" in result:
                result = result["reasoning"]
        elif query_type == "knowledge":
            parsed_query = agent._parse_knowledge_query(query)
            result = agent.execute_knowledge(parsed_query)
            # Format result for better display
            if "entries" in result and result["entries"]:
                entries_text = []
                for i, entry in enumerate(result["entries"]):
                    entry_text = f"Paper {i+1}: {entry.get('title', 'No title')}\n"
                    entry_text += f"Summary: {entry.get('summary', 'No summary')}\n"
                    entry_text += f"Link: {entry.get('link', 'No link')}\n"
                    entries_text.append(entry_text)
                result = "\n\n".join(entries_text)
            else:
                result = "No relevant papers found."
        else:
            result = "I'm not sure how to process that type of query."
        
        return jsonify({'response': result})
    except Exception as e:
        print(f"Error processing query: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/search', methods=['POST'])
def search_papers():
    """Route to handle ArXiv research paper searches"""
    data = request.json
    query = data.get('query', '')
    
    if not query:
        return jsonify({'error': 'Query is required'}), 400
    
    try:
        # Parse the query for knowledge search
        parsed_query = agent._parse_knowledge_query(query)
        
        # Execute the search
        results = agent.execute_knowledge(parsed_query)
        
        # Format the results for frontend
        formatted_results = []
        if 'entries' in results:
            for entry in results['entries']:
                formatted_results.append({
                    'title': entry.get('title', 'Untitled'),
                    'summary': entry.get('summary', 'No summary available'),
                    'link': entry.get('link', '')
                })
        
        return jsonify({'results': formatted_results})
    except Exception as e:
        print(f"Error searching papers: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/tools', methods=['GET'])
def get_tools():
    """Route to get available tools information"""
    try:
        tools_info = {
            'math': list(agent.math_tools.keys()),
            'reasoning': list(agent.reasoning_tools.keys()) if agent.available_tools['reasoning'] else [],
            'knowledge': list(agent.knowledge_tools.keys()),
            'available': agent.available_tools
        }
        return jsonify(tools_info)
    except Exception as e:
        print(f"Error getting tools info: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/static/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory('static', path)

if __name__ == '__main__':
    print("Starting Advanced Agent Backend Server...")
    app.run(host='0.0.0.0', port=5000, debug=True)
