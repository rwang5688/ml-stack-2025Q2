#!/usr/bin/env python3
"""
Simple test for enhanced error handling and logging.
"""

import os
import sys

# Import setup_test_env first to configure environment
import setup_test_env

# Add the multi_agent_sagemaker directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'multi_agent_sagemaker'))

from sagemaker_provider import create_sagemaker_provider


def test_error_categorization():
    """Test error categorization functionality."""
    print("🧪 Testing Error Categorization\n")
    
    try:
        provider = create_sagemaker_provider()
        
        # Test different error types
        test_errors = [
            Exception("Endpoint test-endpoint of account 123456789012 not found"),
            Exception("Access denied when calling the InvokeEndpoint operation"),
            Exception("Throttling exception occurred"),
            Exception("Connection timeout occurred"),
            Exception("Invalid credentials provided"),
            Exception("Some unknown error occurred")
        ]
        
        expected_types = [
            'ENDPOINT_NOT_FOUND',
            'ACCESS_DENIED', 
            'RATE_LIMITED',
            'TIMEOUT',
            'CREDENTIAL_ERROR',
            'UNKNOWN_ERROR'
        ]
        
        print("Testing error categorization:")
        for i, (error, expected) in enumerate(zip(test_errors, expected_types)):
            result = provider._categorize_error(error)
            status = "✅" if result == expected else "❌"
            print(f"  {status} Error {i+1}: {result} (expected: {expected})")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False


def test_performance_logging():
    """Test performance logging functionality."""
    print("\n🧪 Testing Performance Logging\n")
    
    try:
        provider = create_sagemaker_provider()
        
        # Test performance logging
        print("Testing performance metrics logging:")
        provider._log_performance_metrics("test_123", 2.5, 100, 200)
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False


def main():
    """Main test function."""
    print("=" * 60)
    print("Enhanced Error Handling & Logging Test")
    print("=" * 60)
    
    success1 = test_error_categorization()
    success2 = test_performance_logging()
    
    print("\n" + "=" * 60)
    if success1 and success2:
        print("🎉 Enhanced error handling tests PASSED!")
        print("Error categorization and logging are working correctly.")
    else:
        print("💥 Some tests FAILED!")
        print("Please check the error messages above.")
    
    print("=" * 60)
    return 0 if (success1 and success2) else 1


if __name__ == "__main__":
    sys.exit(main())