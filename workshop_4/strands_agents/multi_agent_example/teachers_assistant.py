#!/usr/bin/env python3
"""
# 📁 Teacher's Assistant Strands Agent

A specialized Strands agent that is the orchestrator to utilize sub-agents and tools at its disposal to answer a user query.

## What This Example Shows

"""

from strands import Agent
from strands.models import BedrockModel
from strands_tools import file_read, file_write, editor
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

# Create a file-focused agent with selected tools
bedrock_model = BedrockModel(
    model_id="us.amazon.nova-pro-v1:0",
    temperature=0.1,  # Lower temperature for more consistent routing
)

teacher_agent = Agent(
    model=bedrock_model,
    system_prompt=TEACHER_SYSTEM_PROMPT,
    callback_handler=None,
    tools=[math_assistant, language_assistant, english_assistant, computer_science_assistant, general_assistant],
)


# Example usage
if __name__ == "__main__":
    print("\n🎓 Teacher's Assistant CLI (Bedrock) 🎓\n")
    print("Ask a question in any subject area, and I'll route it to the appropriate Bedrock-powered specialist.")
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
            print(f"DEBUG - Bedrock CLI response type: {type(response)}")
            print(f"DEBUG - Bedrock CLI response: {response}")
            
            # Simplified response extraction - just convert to string (matching app.py)
            content = str(response)
            
            print(f"DEBUG - Bedrock CLI final content: {content}")
            print(f"\n{content}")
            
        except KeyboardInterrupt:
            print("\n\nExecution interrupted. Exiting...")
            break
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            print("Please try asking a different question.")
