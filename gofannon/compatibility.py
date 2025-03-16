"""
Compatibility layer for different versions of the OpenAI package.
This allows the code to work with both older and newer versions of the OpenAI API.
"""
import os
import sys

# Import directly from openai
from openai import OpenAI, APIError

# Print version info for debugging
print("Using native OpenAI client (version 1.0.0+)")
