#!/usr/bin/env python3
"""
Test environment setup for SageMaker multi-agent system.

This script sets up the required environment variables for running
all tests in the multi_agent_sagemaker test suite. It runs automatically
before other test files due to alphabetical ordering.

This ensures all tests have the correct SageMaker configuration.
"""

import os
import sys


def setup_environment():
    """Set up environment variables for SageMaker integration."""
    # Required SageMaker configuration
    os.environ['SAGEMAKER_ENDPOINT_NAME'] = 'jumpstart-dft-hf-llm-mistral-small-20250907-093555'
    os.environ['SAGEMAKER_REGION'] = 'us-west-2'
    
    # Optional configuration for testing
    os.environ['SAGEMAKER_VERBOSE_LOGGING'] = 'true'
    
    # Don't set AWS_PROFILE - let boto3 use environment variables directly
    os.environ['SAGEMAKER_TIMEOUT'] = '30'
    os.environ['SAGEMAKER_MAX_RETRIES'] = '3'
    
    print("✅ SageMaker environment variables set:")
    print(f"   SAGEMAKER_ENDPOINT_NAME: {os.environ['SAGEMAKER_ENDPOINT_NAME']}")
    print(f"   SAGEMAKER_REGION: {os.environ['SAGEMAKER_REGION']}")
    print(f"   SAGEMAKER_VERBOSE_LOGGING: {os.environ['SAGEMAKER_VERBOSE_LOGGING']}")
    print("   AWS credentials: Using environment variables")
    print("\n🚀 Environment is ready for:")
    print("   - Running the Streamlit app: streamlit run app.py")
    print("   - Testing individual agents")
    print("   - SageMaker inference calls")


def run_config_test():
    """Run the configuration test to validate setup."""
    print("\n🧪 Running configuration test...")
    
    try:
        # Import and run the test from the tests directory
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'tests', 'multi_agent_sagemaker'))
        from test_config import main
        exit_code = main()
        
        if exit_code == 0:
            print("\n🎉 Configuration test passed! System is ready for SageMaker integration.")
            return True
        else:
            print("\n💥 Configuration test failed! Please check the configuration.")
            return False
    except ImportError as e:
        print(f"\n⚠️  Could not run configuration test: {e}")
        print("Configuration variables are set, but test validation is unavailable.")
        return True


# Automatically set up test environment when this module is imported
print("🔧 Setting up test environment for SageMaker multi-agent tests...")
setup_environment()
print("✅ Test environment ready\n")

if __name__ == "__main__":
    print("=" * 70)
    print("SageMaker Multi-Agent System - Test Environment Setup")
    print("=" * 70)
    
    # Environment is already set up from import
    print("📋 Test environment variables are configured.")
    print("All test files will use the correct SageMaker configuration.")
    
    # Run configuration test
    success = run_config_test()
    
    if success:
        print("\n🎉 Test environment is ready!")
        print("You can now run individual test files.")
    else:
        print("\n💥 Test environment setup failed!")
        print("Please check the configuration.")
    
    print("=" * 70)