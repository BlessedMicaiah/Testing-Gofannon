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

# Add parent directory to path so we can import the simplified_agent module
# Fix the import path to point to the root directory where simplified_agent.py is located
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from simplified_agent import SimplifiedAgent

app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for all routes

# Initialize the Simplified Agent
agent = SimplifiedAgent()

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
        # Process the query using our simplified agent
        result = agent.process_query(query)
        return jsonify({'response': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search', methods=['POST'])
def search_papers():
    """Route to search for papers"""
    data = request.json
    query = data.get('query', '')
    
    if not query:
        return jsonify({'error': 'Query is required'}), 400
    
    try:
        # Use our simplified agent's search functionality
        search_query = "search " + query
        result = agent.process_query(search_query)
        
        # Return the raw result for now
        return jsonify({'results': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tools', methods=['GET'])
def get_tools():
    """Route to get available tools information"""
    try:
        tools_info = {
            'available': agent.available_tools
        }
        return jsonify(tools_info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/static/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory('static', path)

if __name__ == '__main__':
    print("Starting Advanced Agent Backend Server...")
    # Get port from environment variable for Render compatibility
    port = int(os.environ.get("PORT", 5000))
    # In production, don't use debug mode and bind to 0.0.0.0
    app.run(host='0.0.0.0', port=port, debug=False if os.environ.get("RENDER") else True)
