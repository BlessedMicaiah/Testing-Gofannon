#!/usr/bin/env python3
"""
Simplified Advanced AI Agent
This script provides a simplified version of the advanced agent without external dependencies.
"""
import os
import re
import json
import requests
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class SimplifiedAgent:
    """
    Simplified AI agent with basic functionality for math and search
    """
    
    def __init__(self):
        """Initialize the agent with basic capabilities"""
        print("Initializing SimplifiedAgent...")
        
        # Track whether we have API keys for certain services
        self.has_google_search = (
            bool(os.getenv("GOOGLE_SEARCH_API_KEY")) and
            bool(os.getenv("GOOGLE_SEARCH_ENGINE_ID"))
        )
        
        # Track available tools
        self.available_tools = {
            "math": True,
            "search": self.has_google_search
        }
        
        # Print status
        self._print_status()
    
    def _print_status(self):
        """Print the status of available tools"""
        print("\nAgent Status:")
        print(f"  Math Tools: Available")
        print(f"  Search Tools: {'Available' if self.available_tools['search'] else 'Unavailable (requires API keys)'}")
        
        if not self.has_google_search:
            print("\nNote: For full functionality, set these environment variables in a .env file:")
            print("  GOOGLE_SEARCH_API_KEY=your_google_search_api_key_here")
            print("  GOOGLE_SEARCH_ENGINE_ID=your_google_search_engine_id_here")
    
    def _determine_query_type(self, query):
        """Determine the type of query based on content"""
        query_lower = query.lower()
        
        # Check for math operations
        if any(term in query_lower for term in ["calculate", "add", "sum", "plus", 
                                              "subtract", "minus", "difference", 
                                              "multiply", "product", "times", 
                                              "divide", "quotient", 
                                              "power", "exponent", "squared", "cubed"]):
            return "math"
            
        # Check if it's a search query
        if any(term in query_lower for term in ["search", "find", "look up", "google", 
                                              "information about", "tell me about"]):
            return "search"
            
        # Default to general response
        return "general"
    
    def execute_math(self, query):
        """Execute a math operation based on the query"""
        # Extract numbers and operation from the query
        numbers = re.findall(r'\d+', query)
        
        if len(numbers) < 2:
            return "I need at least two numbers to perform a calculation."
        
        # Convert to integers
        try:
            num1 = int(numbers[0])
            num2 = int(numbers[1])
        except ValueError:
            return "I couldn't parse the numbers in your query."
        
        # Determine operation
        query_lower = query.lower()
        
        if any(term in query_lower for term in ["add", "sum", "plus"]):
            result = num1 + num2
            operation = "addition"
        elif any(term in query_lower for term in ["subtract", "minus", "difference"]):
            result = num1 - num2
            operation = "subtraction"
        elif any(term in query_lower for term in ["multiply", "product", "times"]):
            result = num1 * num2
            operation = "multiplication"
        elif any(term in query_lower for term in ["divide", "quotient"]):
            if num2 == 0:
                return "Cannot divide by zero."
            result = num1 / num2
            operation = "division"
        elif any(term in query_lower for term in ["power", "exponent", "squared", "cubed"]):
            result = num1 ** num2
            operation = "exponentiation"
        else:
            return "I couldn't determine the math operation to perform."
        
        return f"The result of {operation} is: {result}"
    
    def execute_search(self, query):
        """Execute a search query using Google Custom Search"""
        if not self.has_google_search:
            return "Search functionality is not available. Please set the GOOGLE_SEARCH_API_KEY and GOOGLE_SEARCH_ENGINE_ID environment variables."
        
        try:
            # Extract the search terms
            search_query = query.replace("search", "").replace("find", "").replace("look up", "").strip()
            
            # Get API key and search engine ID from environment variables
            api_key = os.getenv("GOOGLE_SEARCH_API_KEY")
            search_engine_id = os.getenv("GOOGLE_SEARCH_ENGINE_ID")
            
            # Construct the API URL
            url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q={search_query}"
            
            # Make the request
            response = requests.get(url)
            results = response.json()
            
            # Check if there are search results
            if "items" not in results:
                return f"No results found for '{search_query}'."
            
            # Format the top 3 results
            formatted_results = "Here are the top search results:\n\n"
            
            for i, item in enumerate(results["items"][:3], 1):
                title = item.get("title", "No title")
                link = item.get("link", "No link")
                snippet = item.get("snippet", "No description")
                
                formatted_results += f"{i}. **{title}**\n"
                formatted_results += f"   {snippet}\n"
                formatted_results += f"   URL: {link}\n\n"
            
            return formatted_results
            
        except Exception as e:
            return f"An error occurred while searching: {str(e)}"
    
    def execute_general(self, query):
        """Handle general queries"""
        return f"I received your question: '{query}'. This is a simplified version of the agent that only handles math and search queries. Try asking a math question like 'What is 5 plus 7?' or a search query like 'Search for information about artificial intelligence'."
    
    def process_query(self, query):
        """Process a query and return a response"""
        # Determine the type of query
        query_type = self._determine_query_type(query)
        
        # Execute the appropriate function based on query type
        if query_type == "math":
            return self.execute_math(query)
        elif query_type == "search":
            return self.execute_search(query)
        else:
            return self.execute_general(query)

# For testing
if __name__ == "__main__":
    agent = SimplifiedAgent()
    
    # Test with a few example queries
    test_queries = [
        "What is 5 plus 7?",
        "Search for information about artificial intelligence",
        "What are the implications of quantum computing on cryptography?"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        response = agent.process_query(query)
        print(f"Response: {response}")
