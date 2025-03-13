#!/usr/bin/env python3
"""
Basic demonstration of Gofannon library functionality
with interactive user query support
"""
from gofannon.basic_math.addition import Addition
from gofannon.basic_math.subtraction import Subtraction
from gofannon.basic_math.multiplication import Multiplication
from gofannon.basic_math.division import Division
from gofannon.basic_math.exponents import Exponents
from gofannon.reasoning.sequential_cot import SequentialCoT
import re

class InteractiveDemo:
    """Interactive demonstration of Gofannon library functionality"""
    
    def __init__(self):
        """Initialize the demo with math tools"""
        # Create instances of the math tools
        self.addition = Addition()
        self.subtraction = Subtraction()
        self.multiplication = Multiplication()
        self.division = Division()
        self.exponents = Exponents()
        
        # Optional: Initialize the reasoning tool (requires API key)
        self.cot = SequentialCoT()
    
    def demo_basic_math(self):
        """Demonstrate the basic math functionality"""
        print("\n=== Basic Math Tools Demo ===")
        
        # Perform some basic calculations
        add_result = self.addition.fn(num1=5, num2=3)
        subtract_result = self.subtraction.fn(num1=10, num2=4)
        multiply_result = self.multiplication.fn(num1=6, num2=7)
        divide_result = self.division.fn(num1=20, num2=5)
        power_result = self.exponents.fn(base=2, power=8)
        
        # Display the results
        print(f"Addition: 5 + 3 = {add_result}")
        print(f"Subtraction: 10 - 4 = {subtract_result}")
        print(f"Multiplication: 6 × 7 = {multiply_result}")
        print(f"Division: 20 ÷ 5 = {divide_result}")
        print(f"Power: 2^8 = {power_result}")
    
    def demo_sequential_cot(self):
        """Demonstrate the sequential chain of thought reasoning functionality"""
        print("\n=== Sequential Chain of Thought Demo ===")
        
        # Define a simple reasoning problem
        problem = "What is the sum of all even numbers between 1 and 10?"
        
        print(f"Problem: {problem}")
        print("Note: This demo requires an OpenAI API key to be set in the environment.")
        print("Skipping actual API call to avoid errors.")
    
    def parse_math_query(self, query):
        """
        Parse a user query to identify math operations and numbers
        
        Args:
            query (str): The user's query
            
        Returns:
            dict: Information extracted from the query
        """
        operation = None
        numbers = []
        
        # Extract numbers
        numbers = [float(num) for num in re.findall(r'\d+\.?\d*', query)]
        
        # Determine operation
        if any(term in query.lower() for term in ["add", "sum", "plus", "+"]):
            operation = "add"
        elif any(term in query.lower() for term in ["subtract", "minus", "difference", "-"]):
            operation = "subtract"
        elif any(term in query.lower() for term in ["multiply", "product", "times", "*", "×"]):
            operation = "multiply"
        elif any(term in query.lower() for term in ["divide", "quotient", "/", "÷"]):
            operation = "divide"
        elif any(term in query.lower() for term in ["power", "exponent", "^", "**", "raised"]):
            operation = "power"
        
        return {
            "operation": operation,
            "numbers": numbers
        }
    
    def process_query(self, query):
        """
        Process a user query and return the result
        
        Args:
            query (str): The user's query
            
        Returns:
            str: Response to the query
        """
        # Parse the query
        parsed = self.parse_math_query(query)
        operation = parsed["operation"]
        numbers = parsed["numbers"]
        
        # Check if we have enough information
        if operation is None:
            return "I couldn't determine what mathematical operation you want to perform. Try asking about addition, subtraction, multiplication, division, or exponents."
        
        if len(numbers) < 2:
            return "I need at least two numbers to perform a calculation. Please provide more numbers in your query."
        
        # Get the first two numbers
        num1, num2 = numbers[0], numbers[1]
        
        # Perform the calculation
        result = None
        if operation == "add":
            result = self.addition.fn(num1=num1, num2=num2)
            return f"Addition: {num1} + {num2} = {result}"
        
        elif operation == "subtract":
            result = self.subtraction.fn(num1=num1, num2=num2)
            return f"Subtraction: {num1} - {num2} = {result}"
        
        elif operation == "multiply":
            result = self.multiplication.fn(num1=num1, num2=num2)
            return f"Multiplication: {num1} × {num2} = {result}"
        
        elif operation == "divide":
            if num2 == 0:
                return "Error: Cannot divide by zero"
            result = self.division.fn(num1=num1, num2=num2)
            return f"Division: {num1} ÷ {num2} = {result}"
        
        elif operation == "power":
            result = self.exponents.fn(base=num1, power=num2)
            return f"Exponentiation: {num1} ^ {num2} = {result}"
        
        return "I couldn't process your query. Please try again."
    
    def run_interactive_mode(self):
        """Run the demo in interactive mode, accepting user queries"""
        print("\n=== Interactive Mode ===")
        print("Type 'exit' or 'quit' to end the demo")
        print("Example queries:")
        print("  - What is 25 + 10?")
        print("  - Calculate 8 × 7")
        print("  - Divide 100 by 4")
        print("  - What is 2 to the power of 6?")
        
        while True:
            query = input("\nEnter your query: ")
            
            # Check for exit command
            if query.lower() in ["exit", "quit", "q"]:
                print("Exiting interactive mode")
                break
            
            # Process the query
            try:
                response = self.process_query(query)
                print("\n" + "="*50)
                print(response)
                print("="*50)
            except Exception as e:
                print(f"Error processing query: {e}")
        
        print("Thank you for using the Gofannon demo!")

def main():
    """Main function to run the demonstrations"""
    print("Gofannon Library Demonstration")
    print("==============================")
    
    try:
        # Create the interactive demo
        demo = InteractiveDemo()
        
        # Run the standard demos
        demo.demo_basic_math()
        demo.demo_sequential_cot()
        
        # Run in interactive mode
        demo.run_interactive_mode()
        
    except Exception as e:
        print(f"Error during demonstration: {e}")

if __name__ == "__main__":
    main()
