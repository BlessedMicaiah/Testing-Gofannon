#!/usr/bin/env python3
"""
Creating a Basic AI Agent with Gofannon
This script demonstrates how to create a simple AI agent using Gofannon tools
without requiring external API keys for demonstration purposes.
"""
import os
import re
from dotenv import load_dotenv

# Import Gofannon math tools
from gofannon.basic_math.addition import Addition
from gofannon.basic_math.subtraction import Subtraction
from gofannon.basic_math.multiplication import Multiplication
from gofannon.basic_math.division import Division
from gofannon.basic_math.exponents import Exponents

class BasicAgent:
    """A simple agent that uses Gofannon's math tools"""
    
    def __init__(self):
        """Initialize the agent with basic tools"""
        print("Initializing BasicAgent with math tools...")
        
        # Initialize the math tools
        self.tools = {
            "addition": Addition(),
            "subtraction": Subtraction(),
            "multiplication": Multiplication(),
            "division": Division(),
            "exponents": Exponents()
        }
        
        print(f"Agent ready with {len(self.tools)} tools")
    
    def parse_query(self, query):
        """
        Parse a user query to identify math operations and numbers
        
        Args:
            query (str): The user's query
            
        Returns:
            dict: Information extracted from the query
        """
        print(f"Parsing query: '{query}'")
        
        # Extract all numbers from the query
        numbers = [float(num) for num in re.findall(r'\d+\.?\d*', query)]
        
        # Identify math operations in the query
        operations = []
        
        if any(term in query.lower() for term in ["add", "sum", "plus", "+"]):
            operations.append("addition")
        
        if any(term in query.lower() for term in ["subtract", "minus", "difference", "-"]):
            operations.append("subtraction")
        
        if any(term in query.lower() for term in ["multiply", "product", "times", "*", "×"]):
            operations.append("multiplication")
        
        if any(term in query.lower() for term in ["divide", "quotient", "/", "÷"]):
            operations.append("division")
        
        if any(term in query.lower() for term in ["power", "exponent", "^", "**", "raised"]):
            operations.append("exponents")
        
        print(f"Extracted {len(numbers)} numbers: {numbers}")
        print(f"Identified {len(operations)} operations: {operations}")
        
        return {
            "operations": operations,
            "numbers": numbers
        }
    
    def execute_operations(self, parsed_query):
        """
        Execute the math operations based on the parsed query
        
        Args:
            parsed_query (dict): The parsed query with operations and numbers
            
        Returns:
            dict: Results of each operation
        """
        operations = parsed_query["operations"]
        numbers = parsed_query["numbers"]
        results = {}
        
        # Check if we have enough numbers
        if len(numbers) < 2:
            print("Warning: Not enough numbers for operations")
            return {"error": "Need at least two numbers for calculations"}
        
        # Use the first two numbers for operations
        num1, num2 = numbers[0], numbers[1]
        print(f"Using numbers: {num1} and {num2}")
        
        # Perform each identified operation
        for op in operations:
            try:
                if op == "addition":
                    results[op] = self.tools[op].fn(num1=num1, num2=num2)
                
                elif op == "subtraction":
                    results[op] = self.tools[op].fn(num1=num1, num2=num2)
                
                elif op == "multiplication":
                    results[op] = self.tools[op].fn(num1=num1, num2=num2)
                
                elif op == "division":
                    if num2 == 0:
                        results[op] = "Error: Division by zero"
                    else:
                        results[op] = self.tools[op].fn(num1=num1, num2=num2)
                
                elif op == "exponents":
                    results[op] = self.tools[op].fn(base=num1, power=num2)
                
                print(f"Executed {op}: {results[op]}")
            
            except Exception as e:
                print(f"Error in {op}: {e}")
                results[op] = f"Error: {str(e)}"
        
        return results
    
    def format_response(self, query, parsed_query, results):
        """
        Format a natural language response based on the results
        
        Args:
            query (str): The original query
            parsed_query (dict): The parsed query
            results (dict): Results of operations
            
        Returns:
            str: Formatted response
        """
        if "error" in results:
            return f"I couldn't process your query: {results['error']}"
        
        if not results:
            return "I couldn't identify any math operations to perform. Try asking about addition, subtraction, multiplication, division, or exponents."
        
        response = f"Based on your query: '{query}'\n\n"
        
        # Add a result section for each operation
        for op, result in results.items():
            num1, num2 = parsed_query["numbers"][0], parsed_query["numbers"][1]
            
            if op == "addition":
                response += f"Addition: {num1} + {num2} = {result}\n"
            
            elif op == "subtraction":
                response += f"Subtraction: {num1} - {num2} = {result}\n"
            
            elif op == "multiplication":
                response += f"Multiplication: {num1} × {num2} = {result}\n"
            
            elif op == "division":
                response += f"Division: {num1} ÷ {num2} = {result}\n"
            
            elif op == "exponents":
                response += f"Exponentiation: {num1}^{num2} = {result}\n"
        
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
        print(f"Running agent with query: {query}")
        
        # Step 1: Parse the query
        parsed_query = self.parse_query(query)
        
        # Step 2: Execute the operations
        results = self.execute_operations(parsed_query)
        
        # Step 3: Format and return the response
        response = self.format_response(query, parsed_query, results)
        
        print("Response ready")
        print("="*50)
        
        return response

def main():
    """Main function to demonstrate the basic agent"""
    print("Basic Gofannon Agent Demo")
    print("========================")
    
    # Initialize the agent
    agent = BasicAgent()
    
    # Example queries
    example_queries = [
        "What is 25 + 10?",
        "Calculate 8 * 7",
        "Divide 100 by 4",
        "What is 2 raised to the power of 6?",
        "Tell me the sum of 15 and 7, and also their product"
    ]
    
    # Run the agent with each example query
    for i, query in enumerate(example_queries, 1):
        print(f"\nQuery {i}: {query}")
        response = agent.run(query)
        print("\nResponse:")
        print(response)
    
    # Interactive mode
    print("\n\nEntering interactive mode (type 'exit' to quit)")
    
    while True:
        user_query = input("\nEnter your query: ")
        
        if user_query.lower() in ["exit", "quit", "q"]:
            print("Exiting interactive mode")
            break
        
        response = agent.run(user_query)
        print("\nResponse:")
        print(response)

if __name__ == "__main__":
    main()
