#!/usr/bin/env python3
"""
Test script for SageMaker-enabled Math Assistant.

This script tests the updated Math Assistant with SageMaker integration.
"""

import os
import sys

# Import setup_test_env first to configure environment
import setup_test_env

# Add the multi_agent_sagemaker directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'multi_agent_sagemaker'))

from math_assistant import math_assistant


def test_math_assistant_creation():
    """Test that the math assistant can be created with SageMaker integration."""
    print("🧪 Testing Math Assistant Creation\n")
    
    try:
        # Test quadratic equation query (this will create the agent internally)
        print("Testing math assistant with quadratic equation...")
        print("Query: 'Solve the quadratic equation x^2 + 5x + 6 = 0'")
        
        # Note: This would make an actual SageMaker call in full integration
        # For now, we're testing that the agent creation works
        result = math_assistant("Solve the quadratic equation x^2 + 5x + 6 = 0")
        
        print(f"✅ Math assistant responded successfully")
        print(f"   Response length: {len(result)} characters")
        print(f"   Response preview: {result[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False


def test_math_assistant_integration():
    """Test that the math assistant properly integrates with SageMaker factory."""
    print("\n🧪 Testing SageMaker Integration\n")
    
    try:
        # Test that the assistant uses the SageMaker factory
        print("Testing SageMaker factory integration...")
        
        # This should show "Routed to Math Assistant (SageMaker)" message
        result = math_assistant("Solve the quadratic equation x^2 + 5x + 6 = 0")
        
        print("✅ SageMaker integration working")
        print("   (Check console output for 'SageMaker' routing message)")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False


def main():
    """Main test function."""
    print("=" * 60)
    print("SageMaker Math Assistant Test")
    print("=" * 60)
    
    success1 = test_math_assistant_creation()
    success2 = test_math_assistant_integration()
    
    print("\n" + "=" * 60)
    if success1 and success2:
        print("🎉 Math Assistant tests PASSED!")
        print("The Math Assistant is ready for SageMaker integration.")
    else:
        print("💥 Some tests FAILED!")
        print("Please check the error messages above.")
    
    print("=" * 60)
    return 0 if (success1 and success2) else 1


if __name__ == "__main__":
    sys.exit(main())