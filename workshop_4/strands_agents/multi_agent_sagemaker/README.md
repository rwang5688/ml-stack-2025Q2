# SageMaker Multi-Agent System

This is a multi-agent system powered by Strands Agents that uses Amazon SageMaker Inference Endpoints for all model inference calls. The system maintains the same functionality as the original multi_agent_example but routes all LLM requests through SageMaker endpoints.

## Quick Start

### 1. Set Up Environment

**Important**: You must run the environment setup before using the system.

```bash
# Navigate to the multi_agent_sagemaker directory
cd workshop_4/strands_agents/multi_agent_sagemaker

# Set up environment variables and test configuration
python setup_env.py
```

This will:
- Set the required SageMaker endpoint and authentication
- Validate the configuration
- Confirm the system is ready

### 2. Run the Streamlit App

After successful environment setup:

```bash
streamlit run app.py
```

### 3. Alternative: Test Individual Components

You can also test individual agents directly:

```bash
python teachers_assistant.py
python math_assistant.py
# etc.
```

## Configuration

The system requires these environment variables:

### Required
- `SAGEMAKER_ENDPOINT_NAME`: Your SageMaker inference endpoint name
- `SAGEMAKER_EXECUTION_ROLE_ARN`: SageMaker execution role ARN

### Optional
- `SAGEMAKER_REGION`: AWS region (default: us-west-2)
- `SAGEMAKER_TIMEOUT`: Request timeout in seconds (default: 30)
- `SAGEMAKER_MAX_RETRIES`: Maximum retry attempts (default: 3)
- `SAGEMAKER_VERBOSE_LOGGING`: Enable detailed logging (default: false)

## Current Configuration

The `setup_env.py` script is pre-configured with:
- **Endpoint**: `jumpstart-dft-hf-llm-mistral-small-20250908-025809`
- **Region**: `us-west-2`
- **Execution Role**: `arn:aws:iam::442042509097:role/service-role/AmazonSageMaker-ExecutionRole-20250606T132304`

## Architecture

The system includes:
- **Teacher's Assistant**: Central orchestrator that routes queries to specialized agents
- **Math Assistant**: Handles mathematical calculations and problems
- **English Assistant**: Processes grammar and writing tasks
- **Language Assistant**: Manages translations
- **Computer Science Assistant**: Handles programming questions
- **General Assistant**: Processes general queries

All agents use SageMaker Inference Endpoints for model inference instead of default Strands model providers.

## Troubleshooting

### Configuration Issues
If you encounter configuration errors:
1. Run `python setup_env.py` to check environment variables
2. Verify your SageMaker endpoint is active and accessible
3. Confirm your AWS credentials have SageMaker permissions

### SageMaker Endpoint Issues
- Ensure the endpoint `jumpstart-dft-hf-llm-mistral-small-20250908-025809` is deployed and in service
- Check that your execution role has the necessary SageMaker permissions
- Verify the endpoint is in the `us-west-2` region

### Streamlit Issues
- Always run `python setup_env.py` before `streamlit run app.py`
- Environment variables must be set in the same terminal session
- If the app fails to start, check the configuration test output

## Development

For development and testing:
- Configuration: `config.py`
- Tests: `../tests/multi_agent_sagemaker/`
- Environment setup: `setup_env.py`
- Example configuration: `.env.example`

## Next Steps

After successful setup, you can:
1. Use the Streamlit interface to interact with all agents
2. Ask mathematical questions (routed to Math Assistant)
3. Request translations (routed to Language Assistant)
4. Get programming help (routed to Computer Science Assistant)
5. Ask general questions (routed to General Assistant)

All responses will be generated using your SageMaker inference endpoint with automatic CloudWatch logging.