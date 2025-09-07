#!/usr/bin/env python3
"""
Simple SageMaker Integration with Strands Agents

Using the native Strands SDK SageMaker support - much cleaner!
"""

import boto3
from strands import Agent
from strands.models.sagemaker import SageMakerAIModel
from config import get_sagemaker_endpoint


def create_sagemaker_model():
    """Create a SageMaker AI model using native Strands support."""
    
    # Get endpoint name from config
    endpoint_name = get_sagemaker_endpoint()
    
    # Create endpoint configuration
    endpoint_config = SageMakerAIModel.SageMakerAIEndpointConfig(
        endpoint_name=endpoint_name
    )
    
    # Create payload configuration
    payload_config = SageMakerAIModel.SageMakerAIPayloadSchema(
        input_key="inputs",
        output_key="generated_text"
    )
    
    # Create the SageMaker AI Model object using native Strands support
    sagemaker_model = SageMakerAIModel(
        endpoint_config=endpoint_config,
        payload_config=payload_config,
        boto_session=boto3.Session()
    )
    
    return sagemaker_model


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
        
        # Test the agent
        response = math_agent.chat("What is 15 + 27?")
        print(f"📝 Response: {response}")
        
    except Exception as e:
        print(f"❌ Error: {e}")