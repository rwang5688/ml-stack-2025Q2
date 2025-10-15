#!/usr/bin/env python3
"""
# 📁 Teacher's Assistant Strands Agent

A specialized Strands agent that is the orchestrator to utilize sub-agents and tools at its disposal to answer a user query.

## What This Example Shows

"""

from strands import Agent
from strands_tools import file_read, file_write, editor
from sagemaker_model import create_simple_agent
from english_assistant import english_assistant
from language_assistant import language_assistant
from math_assistant import math_assistant
from computer_science_assistant import computer_science_assistant
from no_expertise import general_assistant


# Define the teacher system prompt - focused on pure routing
TEACHER_SYSTEM_PROMPT = """
You are a routing agent that determines which specialist to call and returns their complete response.

Available specialists:
- math_assistant: For mathematical calculations, problems, and concepts
- english_assistant: For writing, grammar, literature, and composition  
- language_assistant: For translation and language-related queries
- computer_science_assistant: For programming, algorithms, data structures, and code execution
- general_assistant: For all other topics outside these specialized domains

Your process:
1. Analyze the user's query
2. Call the appropriate specialist tool with the user's exact query
3. Return the specialist's response exactly as provided - do not modify, summarize, or add to it

CRITICAL: Your final response must be identical to what the specialist tool returns. Do not add any commentary, questions, or additional text.
"""

# Create the teacher agent with SageMaker integration and specialized assistant tools
teacher_agent = create_simple_agent(
    system_prompt=TEACHER_SYSTEM_PROMPT,
    tools=[math_assistant, language_assistant, english_assistant, computer_science_assistant, general_assistant],
)


# Example usage
if __name__ == "__main__":
    print("\n🎓 Teacher's Assistant CLI (SageMaker) 🎓\n")
    print("Ask a question in any subject area, and I'll route it to the appropriate SageMaker-powered specialist.")
    print("Type 'exit' to quit.")

    # Interactive loop
    while True:
        try:
            user_input = input("\n> ")
            if user_input.lower() == "exit":
                print("\nGoodbye! 👋")
                break

            response = teacher_agent(user_input)
            
            # Debug: Print response structure (matching app.py)
            print(f"DEBUG - SageMaker CLI response type: {type(response)}")
            print(f"DEBUG - SageMaker CLI response: {response}")
            
            # Simplified response extraction - just convert to string (matching app.py)
            content = str(response)
            
            print(f"DEBUG - SageMaker CLI final content: {content}")
            print(f"\n{content}")
            
        except KeyboardInterrupt:
            print("\n\nExecution interrupted. Exiting...")
            break
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            print("Please try asking a different question.")
    
    # Clean up connections on exit
    try:
        from sagemaker_model import cleanup_connections
        cleanup_connections()
    except:
        pass
