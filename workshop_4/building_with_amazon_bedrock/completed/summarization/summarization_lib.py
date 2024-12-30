import boto3

def get_summary(input_text):
    
    with open("amazon-leadership-principles-070621-us.pdf", "rb") as doc_file:
        doc_bytes = doc_file.read()

    doc_message = {
        "role": "user",
        "content": [
            {
                "document": {
                    "name": "Document 1",
                    "format": "pdf",
                    "source": {
                        "bytes": doc_bytes #Look Ma, no base64 encoding!
                    }
                }
            },
            { "text": input_text }
        ]
    }
    
    session = boto3.Session()
    bedrock = session.client(service_name='bedrock-runtime')
    
    response = bedrock.converse(
        #modelId="amazon.nova-pro-v1:0",
        #modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        #modelId="anthropic.claude-3-5-sonnet-20241022-v2:0",
        modelId="anthropic.claude-3-5-haiku-20241022-v1:0",
        #modelId="meta.llama3-2-3b-instruct-v1:0",
        messages=[doc_message],
        inferenceConfig={
            "maxTokens": 2000,
            "temperature": 0
        },
    )
    
    return response['output']['message']['content'][0]['text']
