#!/usr/bin/env python3
"""
Simple test script for SageMaker configuration management.

This script validates that the configuration system works correctly
and provides helpful feedback for setup.
"""

import os
import sys
# Add the multi_agent_sagemaker directory to the path to import config
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'multi_agent_sagemaker'))
from config import get_configuration, SageMakerConfig, AWSConfig


def test_configuration():
    """Test the configuration loading and validation."""
    print("🧪 Testing SageMaker Configuration System\n")
    
    try:
        # Test configuration loading
        config, aws_config = get_configuration()
        
        print("✅ Configuration loaded successfully!")
        print(f"   Endpoint: {config.endpoint_name}")
        print(f"   Region: {config.region}")
        print(f"   Timeout: {config.timeout}s")
        print(f"   Max Retries: {config.max_retries}")
        print(f"   Verbose Logging: {config.verbose_logging}")
        
        # Show authentication method
        print(f"   Auth Method: Default credential chain")
        
        return True
        
    except ValueError as e:
        print(f"❌ Configuration Error: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {str(e)}")
        return False


def show_environment_status():
    """Show current environment variable status."""
    print("\n📋 Environment Variables Status:")
    
    required_vars = ['SAGEMAKER_ENDPOINT_NAME']
    optional_vars = [
        'SAGEMAKER_REGION', 'SAGEMAKER_TIMEOUT', 'SAGEMAKER_MAX_RETRIES', 
        'SAGEMAKER_VERBOSE_LOGGING'
    ]
    aws_vars = [
        'AWS_DEFAULT_REGION', 'AWS_PROFILE'
    ]
    
    print("\n   Required:")
    for var in required_vars:
        value = os.getenv(var)
        status = "✅ Set" if value else "❌ Missing"
        print(f"     {var}: {status}")
    
    print("\n   Optional:")
    for var in optional_vars:
        value = os.getenv(var)
        status = f"✅ {value}" if value else "⚪ Default"
        print(f"     {var}: {status}")
    
    print("\n   AWS Configuration:")
    for var in aws_vars:
        value = os.getenv(var)
        status = f"✅ {value}" if value else "⚪ Not set"
        print(f"     {var}: {status}")


def main():
    """Main test function."""
    print("=" * 60)
    print("SageMaker Configuration Test")
    print("=" * 60)
    
    # Show environment status
    show_environment_status()
    
    # Test configuration
    success = test_configuration()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 Configuration test PASSED!")
        print("The system is ready for SageMaker integration.")
    else:
        print("💥 Configuration test FAILED!")
        print("Please check the error messages above and fix the configuration.")
        print("\n💡 Quick Setup Example:")
        print("   export SAGEMAKER_ENDPOINT_NAME=my-llm-endpoint")
        print("   export SAGEMAKER_REGION=us-west-2")
        print("   export AWS_PROFILE=default")
        print("   export SAGEMAKER_VERBOSE_LOGGING=true")
    
    print("=" * 60)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())