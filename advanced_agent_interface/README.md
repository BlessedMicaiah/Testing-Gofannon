# Advanced Agent Interface

This project provides a modern React-based user interface for interacting with the advanced_agent.py AI agent. It consists of a React frontend and a Flask backend that communicates with the existing agent implementation.

## Project Structure

```
advanced_agent_interface/
├── backend/
│   └── server.py         # Flask server that interfaces with advanced_agent.py
└── frontend/
    ├── public/
    │   └── index.html    # HTML entry point
    ├── src/
    │   ├── components/
    │   │   ├── ui/       # UI components
    │   │   └── ResearchComponent.jsx
    │   ├── App.jsx       # Main application component
    │   └── index.js      # React entry point
    └── package.json      # NPM dependencies
```

## Setup Instructions

### Backend Setup

1. Make sure you have Python 3.7+ installed
2. Install the required Python packages:

```bash
pip install flask flask-cors
```

3. Start the Flask backend server:

```bash
cd advanced_agent_interface/backend
python server.py
```

The backend server will run on http://localhost:5000

### Frontend Setup

1. Make sure you have Node.js and npm installed
2. Install the frontend dependencies:

```bash
cd advanced_agent_interface/frontend
npm install
```

3. Start the React development server:

```bash
npm start
```

The frontend will be available at http://localhost:3000

## Features

- **AI Agent Interaction**: Submit queries to the advanced AI agent
- **Research Papers**: Search for academic papers using the ArXiv integration
- **Available Tools**: View information about the tools available through the agent

## API Endpoints

- `POST /api/agent`: Submit a query to the AI agent
- `POST /api/search`: Search for academic papers
- `GET /api/tools`: Get information about available tools

## Requirements

- Python 3.7+
- Node.js 14+ and npm
- Required Python packages: flask, flask-cors
- Required npm packages: react, react-dom, react-scripts
