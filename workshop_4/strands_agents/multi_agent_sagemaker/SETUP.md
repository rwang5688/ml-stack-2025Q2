# SageMaker Multi-Agent System Setup Instructions

This guide will help you set up and configure the SageMaker-enabled multi-agent system.

## Prerequisites

### 1. AWS Account and SageMaker Endpoint
- Active AWS account with SageMaker access
- Deployed SageMaker Inference Endpoint
- AWS credentials with SageMaker permissions

### 2. Required Permissions
Your AWS credentials need the following permissions:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "sagemaker:InvokeEndpoint",
                "sagemaker:DescribeEndpoint"
            ],
            "Resource": "arn:aws:sagemaker:*:*:endpoint/*"
        }
    ]
}
```

## Installation Steps

### 1. Install Dependencies
```bash
# Install Python dependencies
pip install -r requirements.txt

# Or if using the parent requirements:
pip install -r ../requirements.txt
```

### 2. Configure AWS Credentials
Choose one of these methods:

#### Option A: AWS CLI (Recommended)
```bash
aws configure
# Enter your AWS Access Key ID, Secret Access Key, and region
```

#### Option B: Environment Variables
```bash
export AWS_ACCESS_KEY_ID=your-access-key
export AWS_SECRET_ACCESS_KEY=your-secret-key
export AWS_SESSION_TOKEN=your-session-token  # If using temporary credentials
```

#### Option C: AWS Profile
```bash
export AWS_PROFILE=your-profile-name
```

### 3. Configure SageMaker Settings
```bash
# Set your SageMaker endpoint name (REQUIRED)
export SAGEMAKER_ENDPOINT_NAME=your-endpoint-name

# Optional: Set region (default: us-west-2)
export SAGEMAKER_REGION=us-west-2

# Optional: Enable verbose logging for debugging
export SAGEMAKER_VERBOSE_LOGGING=true
```

### 4. Validate Configuration
```bash
# Run the setup script to validate configuration
python setup_env.py
```

This will:
- Set the required environment variables
- Test SageMaker endpoint connectivity
- Validate AWS credentials
- Confirm the system is ready

### 5. Run the Application
```bash
# Start the Streamlit web interface
streamlit run app.py

# Or run the command-line interface
python teachers_assistant.py
```

## Configuration Files

### Environment Variables (.env)
Copy and customize the template:
```bash
cp .env.template .env
# Edit .env with your actual values
```

### JSON Configuration (Advanced)
For advanced use cases:
```bash
cp config.json.template config.json
# Edit config.json with your settings
```

## Troubleshooting

### Common Issues

#### 1. "SAGEMAKER_ENDPOINT_NAME environment variable is required"
**Solution**: Set the endpoint name
```bash
export SAGEMAKER_ENDPOINT_NAME=your-actual-endpoint-name
```

#### 2. "Endpoint not found"
**Causes**:
- Incorrect endpoint name
- Endpoint not deployed
- Wrong region

**Solution**: 
- Verify endpoint name in AWS Console
- Check endpoint status (InService)
- Confirm region matches

#### 3. "Access denied"
**Causes**:
- Missing AWS credentials
- Insufficient permissions

**Solution**:
- Run `aws sts get-caller-identity` to verify credentials
- Check IAM permissions for SageMaker access

#### 4. "Configuration test failed"
**Solution**: Run the setup script for detailed diagnostics
```bash
python setup_env.py
```

### Getting Help

1. **Check Configuration**: Run `python setup_env.py` for detailed status
2. **Test Connectivity**: Use the test scripts in `../tests/multi_agent_sagemaker/`
3. **Verify Credentials**: Run `aws sts get-caller-identity`
4. **Check Endpoint**: Verify in AWS SageMaker Console

## Example Configuration

For reference, here's a working configuration:
```bash
export SAGEMAKER_ENDPOINT_NAME=jumpstart-dft-hf-llm-openlm-researc-20250907-051801
export SAGEMAKER_REGION=us-west-2
export SAGEMAKER_VERBOSE_LOGGING=true
```

## Next Steps

After successful setup:
1. **Test Individual Agents**: Try each specialized assistant
2. **Use Web Interface**: Access via Streamlit for full functionality
3. **Monitor Performance**: Check CloudWatch logs for endpoint metrics
4. **Scale as Needed**: Adjust endpoint configuration based on usage

## Advanced Features

The system includes hooks for future enhancements:
- Specialized endpoints per agent type
- Advanced error handling and retry logic
- Performance monitoring and metrics
- Load balancing and failover

See the code comments for implementation details.