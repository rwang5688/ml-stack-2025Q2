#!/usr/bin/env python3
"""
Quick test for all SageMaker-enabled assistants.

This script tests that all assistants can be created with SageMaker integration.
"""

import os
import sys

# Import setup_test_env first to configure environment
import setup_test_env

# Add the multi_agent_sagemaker directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'multi_agent_sagemaker'))

from math_assistant import math_assistant
from english_assistant import english_assistant
from language_assistant import language_assistant
from computer_science_assistant import computer_science_assistant
from no_expertise import general_assistant


def test_all_assistants():
    """Test that all assistants can be created and show SageMaker routing."""
    print("🧪 Testing All SageMaker-Enabled Assistants\n")
    
    assistants = [
        ("Math Assistant", math_assistant, "Solve the quadratic equation x^2 + 5x + 6 = 0"),
        ("English Assistant", english_assistant, "What is a noun?"),
        ("Language Assistant", language_assistant, "Translate \"Hello, how are you?\" to Spanish"),
        ("Computer Science Assistant", computer_science_assistant, "Write a Python function to check if a string is a palindrome"),
        ("General Assistant", general_assistant, "What is the weather like?")
    ]
    
    results = []
    
    for name, assistant_func, test_query in assistants:
        try:
            print(f"Testing {name}...")
            print(f"  Query: '{test_query}'")
            
            # This should show the SageMaker routing message
            response = assistant_func(test_query)
            
            print(f"  ✅ {name} responded successfully")
            print(f"  Response length: {len(response)} characters")
            print(f"  Response preview: {response[:80]}...")
            print()
            
            results.append(True)
            
        except Exception as e:
            print(f"  ❌ {name} failed: {str(e)}")
            print()
            results.append(False)
    
    return all(results)


def main():
    """Main test function."""
    print("=" * 70)
    print("All SageMaker Assistants Test")
    print("=" * 70)
    
    success = test_all_assistants()
    
    print("=" * 70)
    if success:
        print("🎉 All assistants are working with SageMaker integration!")
        print("Check the console output for 'SageMaker' routing messages.")
    else:
        print("💥 Some assistants failed!")
        print("Please check the error messages above.")
    
    print("=" * 70)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())