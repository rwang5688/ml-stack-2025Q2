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