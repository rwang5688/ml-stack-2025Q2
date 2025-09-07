#!/usr/bin/env python3
"""
Simple configuration for SageMaker endpoint
"""

import os


def get_sagemaker_endpoint():
    """Get SageMaker endpoint name from environment variable."""
    endpoint_name = os.getenv('SAGEMAKER_ENDPOINT_NAME')
    if not endpoint_name:
        raise ValueError("SAGEMAKER_ENDPOINT_NAME environment variable is required")
    return endpoint_name


def get_aws_region():
    """Get AWS region from environment variable."""
    return os.getenv('AWS_DEFAULT_REGION', 'us-west-2')


def get_configuration():
    """Get complete configuration for backward compatibility."""
    endpoint = get_sagemaker_endpoint()
    region = get_aws_region()
    
    # Simple config object for compatibility
    class Config:
        def __init__(self):
            self.endpoint_name = endpoint
            self.region = region
            self.verbose_logging = os.getenv('SAGEMAKER_VERBOSE_LOGGING', 'false').lower() == 'true'
    
    class AWSConfig:
        def __init__(self):
            self.region = region
    
    return Config(), AWSConfig()