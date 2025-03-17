#!/usr/bin/env python3
"""
Simplified Advanced AI Agent
This script provides a simplified version of the advanced agent without external dependencies.
"""
import os
import re
import json
import requests
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file if it exists
load_dotenv()

class SimplifiedAgent:
    """
    Simplified AI agent with basic functionality for math and search
    """
    
    def __init__(self):
        """Initialize the agent with basic capabilities"""
        logger.info("Initializing SimplifiedAgent...")
        
        # Track whether we have API keys for certain services
        self.has_google_search = (
            bool(os.getenv("GOOGLE_SEARCH_API_KEY")) and
            bool(os.getenv("GOOGLE_SEARCH_ENGINE_ID"))
        )
        
        # Track available tools - always enable search with fallback mechanism
        self.available_tools = {
            "math": True,
            "search": True  # Always enable search, we'll use fallback if no API keys
        }
        
        # Print status
        self._print_status()
    
    def _print_status(self):
        """Print the status of available tools"""
        logger.info("\nAgent Status:")
        logger.info(f"  Math Tools: Available")
        logger.info(f"  Search Tools: Available (using {'Google API' if self.has_google_search else 'simulated results'})")
        
        if not self.has_google_search:
            logger.info("\nNote: For full search functionality, set these environment variables in a .env file:")
            logger.info("  GOOGLE_SEARCH_API_KEY=your_google_search_api_key_here")
            logger.info("  GOOGLE_SEARCH_ENGINE_ID=your_google_search_engine_id_here")
            logger.info("  Using simulated search results as fallback.")
    
    def _determine_query_type(self, query):
        """Determine the type of query based on content"""
        query_lower = query.lower()
        
        # Check for math operations
        if any(term in query_lower for term in ["calculate", "add", "sum", "plus", 
                                              "subtract", "minus", "difference", 
                                              "multiply", "product", "times", 
                                              "divide", "quotient", 
                                              "power", "exponent", "squared", "cubed"]):
            logger.info(f"Determined query type: math")
            return "math"
            
        # Check if it's a search query
        if any(term in query_lower for term in ["search", "find", "look up", "google", 
                                              "information about", "tell me about"]):
            logger.info(f"Determined query type: search")
            return "search"
            
        # Default to general response
        logger.info(f"Determined query type: general")
        return "general"
    
    def execute_math(self, query):
        """Execute a math operation based on the query"""
        logger.info(f"Executing math query: {query}")
        # Extract numbers and operation from the query
        numbers = re.findall(r'\d+', query)
        
        if len(numbers) < 2:
            logger.warning("Not enough numbers found in math query")
            return "I need at least two numbers to perform a calculation."
        
        # Convert to integers
        try:
            num1 = int(numbers[0])
            num2 = int(numbers[1])
        except ValueError:
            logger.error("Failed to parse numbers in math query")
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
                logger.error("Division by zero attempted")
                return "Cannot divide by zero."
            result = num1 / num2
            operation = "division"
        elif any(term in query_lower for term in ["power", "exponent", "squared", "cubed"]):
            result = num1 ** num2
            operation = "exponentiation"
        else:
            logger.warning("Could not determine math operation")
            return "I couldn't determine the math operation to perform."
        
        response = f"The result of {operation} is: {result}"
        logger.info(f"Math result: {response}")
        return response
    
    def execute_search(self, query):
        """Execute a search query using Google Custom Search"""
        logger.info(f"Executing search query: {query}")
        
        # Extract the search terms
        search_query = query.replace("search", "").replace("find", "").replace("look up", "").strip()
        logger.info(f"Extracted search terms: {search_query}")
        
        # Check if we have Google Search API keys
        if self.has_google_search:
            try:
                # Get API key and search engine ID from environment variables
                api_key = os.getenv("GOOGLE_SEARCH_API_KEY")
                search_engine_id = os.getenv("GOOGLE_SEARCH_ENGINE_ID")
                
                # Construct the API URL
                url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q={search_query}"
                logger.info(f"Making request to Google Custom Search API")
                
                # Make the request
                response = requests.get(url)
                results = response.json()
                
                # Check if there are search results
                if "items" not in results:
                    logger.warning(f"No search results found for: {search_query}")
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
                
                logger.info(f"Formatted {len(results['items'][:3])} search results")
                return formatted_results
                
            except Exception as e:
                logger.error(f"Error during search: {str(e)}", exc_info=True)
                # Fall back to simulated results
                logger.info("Falling back to simulated search results")
                return self._provide_simulated_search_results(search_query)
        
        # If we don't have Google Search API keys, provide simulated results
        logger.info("Google Search API keys not available, using simulated search results")
        return self._provide_simulated_search_results(search_query)
    
    def _provide_simulated_search_results(self, query):
        """Provide simulated search results when API keys are not available"""
        logger.info(f"Generating simulated search results for: {query}")
        
        # Format the query for better display
        formatted_query = query.strip().title()
        
        # Generate simulated search results
        results = f"Here are some search results for '{query}':\n\n"
        
        results += f"1. **{formatted_query}: A Comprehensive Guide**\n"
        results += f"   This comprehensive guide covers everything you need to know about {query}, including history, applications, and future developments.\n"
        results += f"   URL: https://example.com/guide-to-{query.replace(' ', '-').lower()}\n\n"
        
        results += f"2. **The Complete History of {formatted_query}**\n"
        results += f"   Learn about the origins and evolution of {query} through the ages, with insights from leading experts in the field.\n"
        results += f"   URL: https://example.com/history-of-{query.replace(' ', '-').lower()}\n\n"
        
        results += f"3. **Latest Research on {formatted_query} (2025)**\n"
        results += f"   Discover the most recent scientific breakthroughs and research findings related to {query}, published in leading academic journals.\n"
        results += f"   URL: https://example.com/research-{query.replace(' ', '-').lower()}\n\n"
        
        results += f"4. **{formatted_query} for Beginners: Getting Started**\n"
        results += f"   A beginner-friendly introduction to {query} with practical examples and step-by-step tutorials for newcomers.\n"
        results += f"   URL: https://example.com/beginners-{query.replace(' ', '-').lower()}\n\n"
        
        results += f"5. **Top 10 Applications of {formatted_query} in Modern Industry**\n"
        results += f"   Explore how {query} is being applied across various industries to solve real-world problems and drive innovation.\n"
        results += f"   URL: https://example.com/applications-{query.replace(' ', '-').lower()}\n\n"
        
        results += "Note: These are simulated search results. For actual web search results, please configure the Google Search API keys in your environment variables."
        
        logger.info("Generated simulated search results")
        return results
    
    def execute_general(self, query):
        """Handle general queries"""
        logger.info(f"Executing general query: {query}")
        
        # Special handling for common queries
        query_lower = query.lower()
        
        # Special handling for testing and greeting queries
        if query_lower in ["testing", "test", "hello", "hi"]:
            response = """I can help you with various types of questions:
            
1. Math questions - Try asking "Calculate 25 + 17" or "What is 8 times 9?"
2. Search queries - Try asking "Search for information about artificial intelligence"

What would you like to know about?"""
            logger.info(f"Special response for '{query}': {response}")
            return response
        
        # For very short queries that might be just a single word or country name
        elif len(query_lower.split()) <= 2:
            response = f"""I notice you've asked about "{query}". I can provide more information if you ask a more specific question.

Try asking something like:
1. "Tell me about {query}"
2. "Search for information about {query}"
3. "Calculate 25 + 17" (for math questions)"""
            logger.info(f"Short query response for '{query}': {response}")
            return response
        
        # Default general response
        response = f"I received your question: '{query}'. This is a simplified version of the agent that only handles math and search queries. Try asking a math question like 'What is 5 plus 7?' or a search query like 'Search for information about artificial intelligence'."
        logger.info(f"General response: {response}")
        return response
    
    def process_query(self, query):
        """Process a query and return a response"""
        logger.info(f"Processing query: {query}")
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
