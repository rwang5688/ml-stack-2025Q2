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


# Define a focused system prompt for file operations
TEACHER_SYSTEM_PROMPT = """
You are TeachAssist, a sophisticated educational orchestrator designed to coordinate educational support across multiple subjects. Your role is to:

1. Analyze incoming student queries and determine the most appropriate specialized agent to handle them:
   - Math Agent: For mathematical calculations, problems, and concepts
   - English Agent: For writing, grammar, literature, and composition
   - Language Agent: For translation and language-related queries
   - Computer Science Agent: For programming, algorithms, data structures, and code execution
   - General Assistant: For all other topics outside these specialized domains

2. Key Responsibilities:
   - Accurately classify student queries by subject area
   - Route requests to the appropriate specialized agent
   - Return the COMPLETE response from the specialized agent without modification
   - Maintain context and coordinate multi-step problems when needed

3. Decision Protocol:
   - If query involves calculations/numbers → Math Agent
   - If query involves writing/literature/grammar → English Agent
   - If query involves translation → Language Agent
   - If query involves programming/coding/algorithms/computer science → Computer Science Agent
   - If query is outside these specialized areas → General Assistant
   - For complex queries, coordinate multiple agents as needed

4. Response Protocol:
   - When a specialized agent provides a response, return that response in full
   - Do not add additional commentary unless specifically requested
   - Do not summarize or truncate the specialist's response
   - The specialist's expertise should be the primary content delivered to the user

Route the query to the appropriate specialist and return their complete response.
"""

# Create the teacher agent with SageMaker integration and specialized assistant tools
teacher_agent = create_simple_agent(
    system_prompt=TEACHER_SYSTEM_PROMPT,
    tools=[math_assistant, language_assistant, english_assistant, computer_science_assistant, general_assistant],
)


# Example usage
if __name__ == "__main__":
    print("\n📁 Teacher's Assistant Strands Agent (SageMaker) 📁\n")
    print("Ask a question in any subject area, and I'll route it to the appropriate SageMaker-enabled specialist.")
    print("Type 'exit' to quit.")

    # Interactive loop
    while True:
        try:
            user_input = input("\n> ")
            if user_input.lower() == "exit":
                print("\nGoodbye! 👋")
                break

            response = teacher_agent(
                user_input, 
            )
            
            # Extract and print only the relevant content from the specialized agent's response
            content = str(response)
            print(content)
            
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
