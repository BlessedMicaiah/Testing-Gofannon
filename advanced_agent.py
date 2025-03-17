#!/usr/bin/env python3
"""
Advanced AI Agent with Gofannon
This script demonstrates a more advanced agent with multiple tools and reasoning capabilities.
"""
import os
import re
import sys
import json
import logging
import traceback
import xml.etree.ElementTree as ET
from dotenv import load_dotenv

# Add the current directory to the Python path to ensure imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file if it exists
load_dotenv()

# Try importing Gofannon tools with better error handling
try:
    logger.info("Importing Gofannon tools...")
    # Import Gofannon tools
    from gofannon.basic_math.addition import Addition
    from gofannon.basic_math.subtraction import Subtraction
    from gofannon.basic_math.multiplication import Multiplication
    from gofannon.basic_math.division import Division
    from gofannon.basic_math.exponents import Exponents
    from gofannon.reasoning.sequential_cot import SequentialCoT
    from gofannon.arxiv.search import Search as ArxivSearch
    logger.info("Successfully imported Gofannon tools")
except ImportError as e:
    logger.error(f"Error importing Gofannon tools: {str(e)}")
    logger.error(f"Import error traceback: {traceback.format_exc()}")
    logger.error(f"Current Python path: {sys.path}")
    logger.error(f"Current working directory: {os.getcwd()}")
    # Define fallback classes if imports fail
    class DummyTool:
        def __init__(self):
            pass
        def run(self, *args, **kwargs):
            return "This tool is not available due to import errors."
    
    Addition = DummyTool
    Subtraction = DummyTool
    Multiplication = DummyTool
    Division = DummyTool
    Exponents = DummyTool
    SequentialCoT = DummyTool
    ArxivSearch = DummyTool

class AdvancedAgent:
    """
    Advanced AI agent with multiple tools and reasoning capabilities
    Note: Some features would require API keys in a real implementation
    """
    
    def __init__(self):
        """Initialize the agent with various tools"""
        print("Initializing AdvancedAgent...")
        
        # Initialize math tools
        self.math_tools = {
            "addition": Addition(),
            "subtraction": Subtraction(),
            "multiplication": Multiplication(),
            "division": Division(),
            "exponents": Exponents()
        }
        
        # Initialize reasoning tools
        self.reasoning_tools = {
            "sequential_cot": SequentialCoT()
        }
        
        # Initialize knowledge tools (ArXiv for academic information)
        self.knowledge_tools = {
            "arxiv": ArxivSearch()
        }
        
        # Track whether we have API keys for certain services
        self.has_openai_key = bool(os.getenv("OPENAI_API_KEY"))
        self.has_google_search = (
            bool(os.getenv("GOOGLE_SEARCH_API_KEY")) and
            bool(os.getenv("GOOGLE_SEARCH_ENGINE_ID"))
        )
        
        # Track available tools
        self.available_tools = {
            "math": True,
            "reasoning": self.has_openai_key,
            "search": self.has_google_search,
            "knowledge": True  # ArXiv doesn't need API keys
        }
        
        # Print status
        self._print_status()
    
    def _print_status(self):
        """Print the status of available tools"""
        print("\nAgent Status:")
        print(f"  Math Tools: Available ({len(self.math_tools)} tools)")
        print(f"  Reasoning Tools: {'Available' if self.available_tools['reasoning'] else 'Unavailable (requires API key)'}")
        print(f"  Search Tools: {'Available' if self.available_tools['search'] else 'Unavailable (requires API keys)'}")
        print(f"  Knowledge Tools: Available (ArXiv API)")
        
        if not (self.has_openai_key or self.has_google_search):
            print("\nNote: For full functionality, set these environment variables in a .env file:")
            print("  OPENAI_API_KEY=your_openai_api_key_here")
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
            
        # Check if it's a knowledge query that ArXiv might handle
        if any(term in query_lower for term in ["research", "paper", "article", "study", 
                                               "academic", "science", "scientific", 
                                               "physics", "math", "computer science", 
                                               "biology", "publication"]):
            return "knowledge"
        
        # Check for reasoning requests
        elif any(term in query_lower for term in ["explain", "why", "how", "reason", 
                                                 "analyze", "consider", "evaluate",
                                                 "what is", "define", "meaning of"]):
            return "reasoning"
        
        # Check for search requests
        elif any(term in query_lower for term in ["search", "find", "look up", 
                                                 "information about", "tell me about",
                                                 "what do you know about"]):
            return "search"
        
        # Default to reasoning for general questions
        else:
            return "reasoning"
    
    def _parse_knowledge_query(self, query):
        """Parse a knowledge query for ArXiv"""
        # Extract the main topic from the query
        topic = query.lower()
        for prefix in ["what is", "tell me about", "define", "explain", "research on", "papers about"]:
            topic = topic.replace(prefix, "").strip()
        
        # Default parameters for ArXiv search
        max_results = 3
        
        return {
            "topic": topic,
            "max_results": max_results
        }
    
    def execute_reasoning(self, parsed_query):
        """Execute reasoning based on parsed query"""
        topic = parsed_query.get("topic", "")
        steps = parsed_query.get("steps", 3)
        
        # First try to get information from ArXiv for the topic
        try:
            arxiv_results = self.execute_knowledge({"topic": topic, "max_results": 1})
            if "entries" in arxiv_results and arxiv_results["entries"]:
                entry = arxiv_results["entries"][0]
                knowledge_base = f"Based on scientific literature: {entry.get('summary', '')}"
            else:
                knowledge_base = ""
        except Exception:
            knowledge_base = ""
        
        # Use actual API if available, otherwise simulate
        if self.available_tools["reasoning"]:
            try:
                result = self.reasoning_tools["sequential_cot"].fn(prompt=topic, steps=steps)
                return {"reasoning": result}
            except Exception as e:
                print(f"Error with reasoning API: {e}")
                # Fall back to simulation if API fails
                return {"reasoning": self._simulate_reasoning(topic, steps, knowledge_base)}
        else:
            # Simulate reasoning with any knowledge we have
            return {"reasoning": self._simulate_reasoning(topic, steps, knowledge_base)}
    
    def _simulate_reasoning(self, query, steps=3, knowledge_base=""):
        """
        Simulate chain-of-thought reasoning when API key isn't available
        
        Args:
            query (str): The query to reason about
            steps (int): Number of reasoning steps
            knowledge_base (str): Optional knowledge to incorporate
            
        Returns:
            str: Simulated reasoning output
        """
        print(f"Simulating reasoning for: '{query}'")
        
        # Special responses for testing and common queries
        query_lower = query.lower()
        
        if query_lower in ["testing", "test", "hello", "hi"]:
            return """I can help you with various types of questions:
            
1. Math questions - Try asking "Calculate 25 + 17" or "What is 8 times 9?"
2. Research paper searches - Try asking "Find research papers about quantum computing"
3. General knowledge questions - Try asking "Tell me about artificial intelligence"

What would you like to know about?"""
        
        # For very short queries that might be just a single word
        elif len(query_lower.split()) <= 2:
            return f"""I notice you've asked about "{query}". I can provide more information if you ask a more specific question.

Try asking something like:
1. "Tell me about {query}"
2. "What is {query} used for?"
3. "Find research papers about {query}"
4. "Calculate 25 + 17" (for math questions)"""
        
        # For an egg query, provide actual information
        if "egg" in query_lower:
            reasoning = (
                f"I'll explain what an egg is:\n\n"
                f"Step 1: Basic Definition\n"
                f"  An egg is a reproductive cell or structure laid by female animals, particularly birds, reptiles, and some fish and invertebrates. "
                f"In everyday contexts, the term usually refers to chicken eggs used in cooking.\n\n"
                f"Step 2: Structure and Composition\n"
                f"  A typical bird egg consists of several parts:\n"
                f"  - Shell: A hard protective outer layer made primarily of calcium carbonate\n"
                f"  - Membranes: Thin layers just inside the shell that protect against bacterial infection\n"
                f"  - Air cell: A pocket of air usually at the larger end of the egg\n"
                f"  - Albumen: The egg white, which is mostly protein (primarily albumin)\n"
                f"  - Yolk: The yellow center, rich in fats, proteins, vitamins, and minerals\n"
                f"  - Chalazae: Rope-like strands that anchor the yolk in the center of the egg\n\n"
                f"Step 3: Function and Significance\n"
                f"  Eggs serve as:\n"
                f"  - A reproductive structure containing nutrients and everything needed for an embryo to develop\n"
                f"  - An important food source for humans, containing high-quality protein and various nutrients\n"
                f"  - A versatile culinary ingredient used in countless recipes across many cultures\n"
            )
            return reasoning
        
        # Incorporate any knowledge we have from ArXiv
        if knowledge_base:
            base_info = f"Based on available information: {knowledge_base}\n\n"
        else:
            base_info = ""
            
        # Simple simulation of reasoning steps
        if query.lower() == "gear":
            return """I can help you with various types of questions:
            
1. Math questions - Try asking "Calculate 25 + 17" or "What is 8 times 9?"
2. Research paper searches - Try asking "Find research papers about quantum computing"
3. General knowledge questions - Try asking "Tell me about artificial intelligence"

What would you like to know about?"""
        else:
            reasoning = (
                f"{base_info}I'll break down my thought process for answering: '{query}'\n\n"
                f"Step 1: First, I need to understand what the query is asking for.\n"
                f"  The query is about: {query}\n\n"
                f"Step 2: I'll identify what information or calculations are needed.\n"
                f"  For this query, I would need to {self._get_reasoning_action(query)}\n\n"
                f"Step 3: Now I can formulate my response based on the analysis.\n"
                f"  {self._get_reasoning_conclusion(query)}\n"
            )
            
            return reasoning
    
    def _get_reasoning_action(self, query):
        """Generate a simulated reasoning action based on query content"""
        if any(term in query.lower() for term in ["calculate", "add", "subtract", "multiply", "divide"]):
            return "perform the mathematical operation implied in the query"
        elif any(term in query.lower() for term in ["explain", "why", "how", "what is"]):
            return "provide an explanation about the concept mentioned in the query"
        elif any(term in query.lower() for term in ["find", "search", "look up"]):
            return "search for relevant information about the topic"
        else:
            return "analyze the query to determine the best approach to answer it"
    
    def _get_reasoning_conclusion(self, query):
        """Generate a simulated reasoning conclusion"""
        if any(term in query.lower() for term in ["calculate", "add", "subtract", "multiply", "divide"]):
            return "I would provide the mathematical result after performing the calculation"
        elif any(term in query.lower() for term in ["explain", "why", "how", "what is"]):
            return "I would provide a clear explanation of the concept, with relevant examples if helpful"
        elif any(term in query.lower() for term in ["find", "search", "look up"]):
            return "I would present the most relevant information found during the search"
        else:
            return "I would provide a comprehensive answer addressing all aspects of the query"

    def _parse_math_query(self, query):
        """Parse a math query to extract operations and numbers"""
        # Extract all numbers
        numbers = [float(num) for num in re.findall(r'\d+\.?\d*', query)]
        
        # Identify math operations
        operations = []
        if any(term in query.lower() for term in ["add", "sum", "plus", "+"]):
            operations.append("addition")
        
        if any(term in query.lower() for term in ["subtract", "minus", "difference", "-"]):
            operations.append("subtraction")
        
        if any(term in query.lower() for term in ["multiply", "product", "times", "*", "×"]):
            operations.append("multiplication")
        
        if any(term in query.lower() for term in ["divide", "quotient", "/", "÷"]):
            operations.append("division")
        
        if any(term in query.lower() for term in ["power", "exponent", "^", "**", "squared", "cubed"]):
            operations.append("exponents")
        
        return {
            "operations": operations,
            "numbers": numbers
        }
    
    def _parse_reasoning_query(self, query):
        """Parse a reasoning query"""
        # For reasoning, we mainly need to determine the topic and desired steps
        topic = query
        
        # Try to extract the number of steps if specified
        steps = 3  # Default number of steps
        step_match = re.search(r'(\d+)\s+steps?', query)
        if step_match:
            steps = int(step_match.group(1))
        
        return {
            "topic": topic,
            "steps": steps
        }
    
    def _parse_search_query(self, query):
        """Parse a search query to extract the search term"""
        # Remove search indicators to get the actual search term
        search_term = query.lower()
        for prefix in ["search for", "search", "find", "look up", "tell me about", "information about", "what do you know about"]:
            search_term = search_term.replace(prefix, "").strip()
        
        return {
            "search_term": search_term
        }
    
    def execute_math(self, parsed_query):
        """Execute math operations based on parsed query"""
        operations = parsed_query.get("operations", [])
        numbers = parsed_query.get("numbers", [])
        results = {}
        
        # Check if we have enough numbers
        if len(numbers) < 2:
            return {"error": "Need at least two numbers for calculations"}
        
        # Use the first two numbers for operations
        num1, num2 = numbers[0], numbers[1]
        
        # Perform each identified operation
        for op in operations:
            try:
                if op == "addition":
                    results[op] = self.math_tools[op].fn(num1=num1, num2=num2)
                
                elif op == "subtraction":
                    results[op] = self.math_tools[op].fn(num1=num1, num2=num2)
                
                elif op == "multiplication":
                    results[op] = self.math_tools[op].fn(num1=num1, num2=num2)
                
                elif op == "division":
                    if num2 == 0:
                        results[op] = "Error: Division by zero"
                    else:
                        results[op] = self.math_tools[op].fn(num1=num1, num2=num2)
                
                elif op == "exponents":
                    results[op] = self.math_tools[op].fn(base=num1, power=num2)
                
            except Exception as e:
                results[op] = f"Error: {str(e)}"
        
        return results

    def execute_search(self, parsed_query):
        """Execute search based on parsed query"""
        search_term = parsed_query.get("search_term", "")
        
        # Use actual API if available, otherwise simulate
        if self.available_tools["search"]:
            # In a real implementation, this would call the Google Search API
            return {"error": "Real search API call not implemented in this demo"}
        else:
            # Simulate search results
            return {
                "search_results": [
                    {"title": f"Simulated result 1 for '{search_term}'", "snippet": "This is a simulated search result."},
                    {"title": f"Simulated result 2 for '{search_term}'", "snippet": "This is another simulated search result."},
                    {"title": f"Simulated result 3 for '{search_term}'", "snippet": "This is yet another simulated search result."}
                ],
                "simulation_note": "These are simulated results. Set up API keys for real search functionality."
            }
    
    def format_math_response(self, query, results):
        """Format a response for math queries"""
        if "error" in results:
            return f"I couldn't process your math query: {results['error']}"
        
        if not results:
            return "I couldn't identify any math operations to perform in your query."
        
        response = f"For your query: '{query}'\n\n"
        
        for op, result in results.items():
            if op == "addition":
                response += f"Addition result: {result}\n"
            elif op == "subtraction":
                response += f"Subtraction result: {result}\n"
            elif op == "multiplication":
                response += f"Multiplication result: {result}\n"
            elif op == "division":
                response += f"Division result: {result}\n"
            elif op == "exponents":
                response += f"Exponentiation result: {result}\n"
        
        return response
    
    def format_reasoning_response(self, query, results):
        """Format a response for reasoning queries"""
        if "error" in results:
            return f"I couldn't process your reasoning query: {results['error']}"
        
        if "reasoning" not in results:
            return "I couldn't generate any reasoning for your query."
        
        response = f"Reasoning for your query: '{query}'\n\n"
        response += results["reasoning"]
        
        if not self.available_tools["reasoning"]:
            response += "\n\n(Note: This is a simulated response. Set up an OpenAI API key for real reasoning.)"
        
        return response
    
    def format_search_response(self, query, results):
        """Format a response for search queries"""
        if "error" in results:
            return f"I couldn't process your search query: {results['error']}"
        
        if "search_results" not in results:
            return "I couldn't find any search results for your query."
        
        response = f"Search results for: '{query}'\n\n"
        
        for i, result in enumerate(results["search_results"], 1):
            response += f"{i}. {result['title']}\n"
            response += f"   {result['snippet']}\n\n"
        
        if "simulation_note" in results:
            response += f"\n{results['simulation_note']}"
        
        return response
    
    def execute_knowledge(self, parsed_query):
        """
        Execute knowledge query using ArXiv
        
        Args:
            parsed_query: Dictionary with topic and parameters
            
        Returns:
            dict: Results from ArXiv
        """
        topic = parsed_query.get("topic", "")
        max_results = parsed_query.get("max_results", 3)
        
        try:
            # Query ArXiv for the topic
            arxiv_response = self.knowledge_tools["arxiv"].fn(
                query=topic,
                max_results=max_results
            )
            
            # Parse the XML response
            return self._parse_arxiv_response(arxiv_response)
        except Exception as e:
            print(f"Error querying ArXiv: {e}")
            return {"error": str(e)}
    
    def _parse_arxiv_response(self, xml_text):
        """
        Parse ArXiv API response XML
        
        Args:
            xml_text: XML response from ArXiv
            
        Returns:
            dict: Parsed information
        """
        try:
            # Handle namespace in ArXiv XML
            ns = {
                'atom': 'http://www.w3.org/2005/Atom',
                'opensearch': 'http://a9.com/-/spec/opensearch/1.1/'
            }
            
            root = ET.fromstring(xml_text)
            
            # Parse total results
            total_results = root.find('.//opensearch:totalResults', ns)
            total_results = int(total_results.text) if total_results is not None else 0
            
            # Parse entries
            entries = []
            for entry in root.findall('.//atom:entry', ns):
                parsed_entry = {}
                
                # Get title
                title = entry.find('./atom:title', ns)
                if title is not None:
                    parsed_entry['title'] = title.text
                
                # Get authors
                authors = []
                for author in entry.findall('./atom:author/atom:name', ns):
                    if author.text:
                        authors.append(author.text)
                parsed_entry['authors'] = authors
                
                # Get summary
                summary = entry.find('./atom:summary', ns)
                if summary is not None:
                    parsed_entry['summary'] = summary.text
                
                # Get link
                link = entry.find('./atom:id', ns)
                if link is not None:
                    parsed_entry['link'] = link.text
                
                # Get published date
                published = entry.find('./atom:published', ns)
                if published is not None:
                    parsed_entry['published'] = published.text
                
                entries.append(parsed_entry)
            
            return {
                'total_results': total_results,
                'entries': entries
            }
        except Exception as e:
            print(f"Error parsing ArXiv response: {e}")
            return {'error': str(e), 'xml': xml_text[:200] + '...'}
    
    def format_knowledge_response(self, query, results):
        """
        Format a response for knowledge queries
        
        Args:
            query: The original query
            results: Results from knowledge tools
            
        Returns:
            str: Formatted response
        """
        if "error" in results:
            # Fall back to simulated reasoning
            return self.format_reasoning_response(query, {"reasoning": self._simulate_reasoning(query)})
        
        if not results.get("entries"):
            return f"I couldn't find specific research articles about '{query}'. Would you like me to try a different approach?"
        
        # Format a response based on the ArXiv results
        response = f"Here's what I found about '{query}' from scientific research:\n\n"
        
        for i, entry in enumerate(results["entries"][:3], 1):
            response += f"{i}. {entry.get('title', 'Untitled paper')}\n"
            response += f"   Authors: {', '.join(entry.get('authors', ['Unknown']))}\n"
            
            # Trim and format summary
            summary = entry.get('summary', '')
            if len(summary) > 300:
                summary = summary[:300] + "..."
            response += f"   Summary: {summary}\n"
            
            if entry.get('link'):
                response += f"   Link: {entry.get('link')}\n"
            
            response += "\n"
        
        response += f"\nTotal results found: {results.get('total_results', len(results.get('entries', [])))}"
        return response
    
    def run(self, query):
        """
        Run the agent with a user query
        
        Args:
            query (str): The user's query
            
        Returns:
            str: Response to the query
        """
        print("\n" + "="*50)
        print(f"Processing query: {query}")
        
        # Step 1: Parse the query
        parsed_query = self.parse_query(query)
        print(f"Query type: {parsed_query['type']}")
        
        # Step 2: Execute the appropriate tools
        query_type = parsed_query["type"]
        if query_type == "math":
            results = self.execute_math(parsed_query)
            response = self.format_math_response(query, results)
        
        elif query_type == "reasoning":
            results = self.execute_reasoning(parsed_query)
            response = self.format_reasoning_response(query, results)
        
        elif query_type == "search":
            results = self.execute_search(parsed_query)
            response = self.format_search_response(query, results)
            
        elif query_type == "knowledge":
            parsed_knowledge = self._parse_knowledge_query(query)
            results = self.execute_knowledge(parsed_knowledge)
            response = self.format_knowledge_response(query, results)
        
        else:
            response = "I'm not sure how to process this type of query."
        
        print("Response generated")
        print("="*50)
        
        return response
    
    def parse_query(self, query):
        """
        Parse a user query to identify operations and parameters
        
        Args:
            query (str): The user's query
            
        Returns:
            dict: Parsed information from the query
        """
        # Determine query type
        query_type = self._determine_query_type(query)
        
        # Extract relevant information based on query type
        parsed = {
            "type": query_type,
            "text": query
        }
        
        # Extract additional information based on query type
        if query_type == "math":
            parsed.update(self._parse_math_query(query))
        elif query_type == "reasoning":
            parsed.update(self._parse_reasoning_query(query))
        elif query_type == "search":
            parsed.update(self._parse_search_query(query))
        elif query_type == "knowledge":
            parsed.update(self._parse_knowledge_query(query))
        
        return parsed

def run_examples(agent):
    """Run a set of example queries with the agent"""
    examples = [
        # Math examples
        "What is 42 + 18?",
        "Calculate 15 * 8",
        "What is 2 to the power of 10?",
        
        # Reasoning examples
        "Explain why the sky appears blue",
        "What are the key principles of machine learning?",
        
        # Search examples
        "Search for information about climate change",
        "Tell me about the history of artificial intelligence",
        
        # Knowledge examples
        "What is the current research on COVID-19 vaccines?",
        "Find papers about the application of AI in healthcare"
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n[Example {i}] Query: {example}")
        response = agent.run(example)
        print("\nResponse:")
        print(response)
        
        # Just run 3 examples by default to keep output manageable
        if i >= 3:
            print("\n(Note: Only showing 3 examples for brevity)")
            break

def interactive_mode(agent):
    """Run the agent in interactive mode"""
    print("\n" + "="*50)
    print("Interactive Mode")
    print("Type 'exit' or 'quit' to end the session")
    print("="*50)
    
    while True:
        query = input("\nEnter your query: ")
        
        if query.lower() in ["exit", "quit", "q"]:
            print("Exiting interactive mode")
            break
        
        response = agent.run(query)
        print("\nResponse:")
        print(response)

def main():
    """Main function to run the advanced agent"""
    print("Advanced Gofannon Agent Demo")
    print("===========================")
    
    # Initialize the agent
    agent = AdvancedAgent()
    
    # Run example queries
    run_examples(agent)
    
    # Interactive mode
    interactive_mode(agent)

if __name__ == "__main__":
    main()
