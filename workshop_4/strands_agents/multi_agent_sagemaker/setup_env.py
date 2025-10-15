#!/usr/bin/env python3
"""
Environment setup script for SageMaker multi-agent system.

This script sets up the required environment variables for running
the SageMaker-enabled multi-agent system, including the Streamlit app.

Usage:
    python setup_env.py              # Set environment and run config test
    python setup_env.py --no-test    # Set environment only (no test)
"""

import os
import sys


def setup_environment():
    """Set up environment variables for SageMaker integration."""
    # Required SageMaker configuration
    # TODO: Replace with your actual SageMaker endpoint name
    endpoint_name = 'jumpstart-dft-hf-llm-mistral-small-{YYYYMMDD}-{HHMMSS}'
    
    if '{YYYYMMDD}' in endpoint_name or '{HHMMSS}' in endpoint_name:
        print("⚠️  WARNING: You need to replace the endpoint name template with your actual endpoint!")
        print("   Current template: jumpstart-dft-hf-llm-mistral-small-{YYYYMMDD}-{HHMMSS}")
        print("   Example actual:   jumpstart-dft-hf-llm-mistral-small-20250908-025809")
        print("   Please edit setup_env.py and replace the endpoint_name variable.")
        return False
    
    os.environ['SAGEMAKER_ENDPOINT_NAME'] = endpoint_name
    os.environ['SAGEMAKER_REGION'] = 'us-west-2'
    
    # Optional configuration for testing
    os.environ['SAGEMAKER_VERBOSE_LOGGING'] = 'true'
    os.environ['SAGEMAKER_TIMEOUT'] = '30'
    os.environ['SAGEMAKER_MAX_RETRIES'] = '3'
    
    # Don't set AWS_PROFILE - let boto3 use environment variables directly
    
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


if __name__ == "__main__":
    print("=" * 70)
    print("SageMaker Multi-Agent System - Environment Setup")
    print("=" * 70)
    
    # Set up environment
    setup_success = setup_environment()
    
    if not setup_success:
        print("\n❌ Setup failed! Please update the endpoint name in setup_env.py")
        print("=" * 70)
        sys.exit(1)
    
    # Check if user wants to skip test
    run_test = "--no-test" not in sys.argv
    
    if run_test:
        success = run_config_test()
        if success:
            print("\n📋 Next Steps:")
            print("   1. Run the Streamlit app: streamlit run app.py")
            print("   2. Or test individual components in Python")
        else:
            print("\n📋 Fix the configuration issues above before proceeding.")
    else:
        print("\n📋 Environment variables set. Run 'python setup_env.py' to test configuration.")
    
    print("=" * 70)