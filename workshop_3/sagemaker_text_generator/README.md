### SageMaker Application Development: SageMaker Text Generator

Reference: https://catalog.us-east-1.prod.workshops.aws/workshops/0b6e72fe-77ee-4777-98cc-237eec795fdb/en-US/fm/06-chatbot

Notes:
- Reference is for a Bedrock Chatbot.
- We changed the Lambda function code to invoke a SageMaker Inference Endpoint for DistilGPT2 for text generation task.

Deployment and Test instructions:

1. Create a Lambda function: `sagemaker_text_generator_yyyymmdd`.

- Navigate to Lambda functions console.
- Click **Create function**.
- Set Function name: `sagemaker_text_generator_yyyymmdd` and Runtime: Latest Python runtime.
- Note: Runtime must be at or beyond the Python version of the Deep Learning Container Image.
- Click **Create function**.

2. Add and deploy code for the Lambda function: `sagemaker_text_generator_yyyymmdd`.

- Nvigate to Code.
- Copy and paste contents of repo's `lambda_function.py` to file `lambda_function.py`.
- Replace <SageMaker Inference Endpoint Name> with the actual SageMaker Inference Endpoint Name, e.g., distilgpt2-pt-ep-yyyy-mm-dd-hh-mm-ss.
- Click **File > Save**.
- Create a new file: `index.html`.
- Copy and paste contents of repo's `index.html` to file `index.html`.
- Click **File > Save**.
- Click **Deploy**.

3. Configure the Lambda function: `sagemaker_text_generator_yyyymmdd`.

- Navigate to Configuration > General Configuration.
- Click **Edit**.  Set timeout to 1 minute (60 seconds). Click **Save**.
- Navigate to Configuration > Permissions.
- Navigate to the Lambda function's exeuction role.
- Click **Add permissions > Attach policies**.
- Add `AmazonSageMakerFullAccess`.
- Click **Add permissions**.
- Navigate back to and refresh the Lambda function's Configuration > Permissions page.
- Confirm the Lambda function's execution role has the newly added permissions.

4. Test the Lambda function: `sagemaker_text_generator_yyyymmdd`.

- Navigate to Test.
- Select `Create new event`.
- Set Event name: `test`.
- Copy and paste contents of repo's `test_event.json` to Event JSON.
- Click **Save**.
- Click **Test**.
- Confirm Lambda function executes successfully.

5. Create and configure an API Gateway REST API with name: `sagemaker_text_generator_yyyymmdd` and stage: `demo`.

- Navigate to API Gateway APIs console.
- Click **Create API**.
- Click `REST API`.
- Click **Build**.
- Select `New API`.
- Set API Name: `sagemaker_text_generator_yyyymmdd` and API endpoint type: `Regional` (default).
- Click **Create API**.
- Navigate to Resources.
- Click **Create method**.
- Set Method type: `ANY`, Integration type: `Lambda function`, and Lambda proxy integration: `True`.
- Set Lambda function: ARN of the `sagemaker_text_generator_yyyymmdd` Lambda function.
- Click **Create method**.
- Click **Deploy API**.
- Set Stage: `*New stage*` and Stage name: `demo`.
- Click **Deploy**.

6. Test SageMaker Text Generator: `sagemaker_text_generator_yyyymmdd`.

- Copy `demo` stage's Invoke URL: `https://<api id>.execute-api.us-west-2.amazonaws.com/demo`
- Open new web browser tab.
- Past `demo` stage's Invoke URL.
- Wait for SageMaker Text Generator page to appear.
- Enter prompt, e.g., `How are you?`
- Click **Send**.
- Wait for response to appear.
