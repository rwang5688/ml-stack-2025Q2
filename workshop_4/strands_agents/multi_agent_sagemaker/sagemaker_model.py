#!/usr/bin/env python3
"""
SageMaker Integration with Strands Agents

Using the native Strands SDK SageMaker support.

IMPORTANT MODEL COMPATIBILITY NOTE:
===================================
Model Compatibility:
The SageMaker provider is designed to work with models that support OpenAI-compatible chat 
completion APIs. During development and testing, the provider has been validated with 
Mistral-Small-24B-Instruct-2501, which demonstrated reliable performance across various 
conversational AI tasks.

Base language models (like Open Llama 7b V2) will fail with "Template error: template not found"
because they lack the required chat completion API compatibility.

Reference: https://strandsagents.com/latest/documentation/docs/user-guide/concepts/model-providers/sagemaker/

Note: Tool calling support varies by model. Models like Mistral-Small-24B-Instruct-2501 have 
demonstrated reliable tool calling capabilities, but not all models deployed on SageMaker support 
this feature. Verify your model's capabilities before implementing tool-based workflows.
"""

import boto3
import warnings
from strands import Agent
from strands.models.sagemaker import SageMakerAIModel
from config import get_sagemaker_endpoint, get_aws_region

# Suppress urllib3 warnings about unclosed connections
warnings.filterwarnings("ignore", message=".*unclosed.*", category=ResourceWarning)
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def create_sagemaker_model():
    """Create a SageMaker AI model using native Strands support."""
    
    # Get endpoint name from config
    endpoint_name = get_sagemaker_endpoint()
    
    # Get AWS region from config
    region = get_aws_region()
    
    # Create the SageMaker AI Model object using official Strands format
    sagemaker_model = SageMakerAIModel(
        endpoint_config={
            "endpoint_name": endpoint_name,
            "region_name": region,
        },
        payload_config={
            "max_tokens": 1000,
            "temperature": 0.7,
            "stream": True,  # Enable streaming for better user experience
        }
    )
    
    return sagemaker_model


def cleanup_connections():
    """Clean up any lingering HTTP connections."""
    try:
        import urllib3
        urllib3.disable_warnings()
        # Force cleanup of connection pools
        urllib3.poolmanager.clear()
    except:
        pass


def create_simple_agent(system_prompt: str, tools=None):
    """Create a Strands agent with SageMaker model - the RIGHT way."""
    
    # Create SageMaker model
    sagemaker_model = create_sagemaker_model()
    
    # Create agent with SageMaker model
    agent = Agent(
        system_prompt=system_prompt,
        model=sagemaker_model,  # This is how you actually use SageMaker with Strands!
        tools=tools or []
    )
    
    return agent


# Example usage
if __name__ == "__main__":
    try:
        print("🚀 Creating SageMaker-enabled agent the SIMPLE way...")
        
        math_agent = create_simple_agent(
            "You are a helpful math assistant. Solve problems step by step."
        )
        
        print("✅ Agent created successfully!")
        print("🧮 Testing with a math question...")
        
        # Test the agent (using official format from docs)
        response = math_agent("What is 15 + 27?")
        print(f"📝 Response: {response}")
        
    except Exception as e:
        print(f"❌ Error: {e}")