#!/usr/bin/env python3
"""
Test SageMaker model integration with Strands
"""

import sys
import os

# Add the multi_agent_sagemaker directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'multi_agent_sagemaker'))

from sagemaker_model import create_sagemaker_model, create_simple_agent


def test_sagemaker_model():
    """Test SageMaker model creation and agent integration."""
    
    print("🧪 Testing SageMaker Model Integration")
    print("=" * 50)
    
    try:
        print("1. Creating SageMaker model...")
        model = create_sagemaker_model()
        print("✅ SageMaker model created")
        
        print("\n2. Creating agent with SageMaker model...")
        agent = create_simple_agent("You are a helpful assistant.")
        print("✅ Agent created with SageMaker model")
        
        print("\n3. Testing agent response...")
        response = agent.chat("What is 2 + 2?")
        print(f"✅ Response: {response}")
        
        print("\n🎉 All tests passed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    
    return True


if __name__ == "__main__":
    success = test_sagemaker_model()
    sys.exit(0 if success else 1)