### Building with Amazon Bedrock: Retrieval Augmented Generation (RAG) Chatbot and Document Summarization

Workshop: https://catalog.workshops.aws/building-with-amazon-bedrock/en-US

#### Prerequisites

1. Create and activate Python virtual environment.

- $ cd building_with_amazon_bedrock
- $ python3 -m venv .venv
- Linux:
- $ source .venv/bin/activate
- Windows:
- $ source .venv/Scripts/activate

2. Install dependencies.

- $ cd building_with_amazon_bedrock
- $ pip install -r setup/requirements.txt

3. Populate Chroma DB data collections for RAG Chatbot.

- $ cd data
- $ python populate_collection.py

#### Retrieval Augmented Generation (RAG) Chatbot

Lab: https://catalog.workshops.aws/building-with-amazon-bedrock/en-US/intermediate/bedrock-rag-chatbot

Code: building_with_amazon_bedrock/completed/rag_chatbot

- $ cd building_with_amazon_bedrock
- $ cd completed/rag_chatbot
- $ ./run_rag_chatbot_app.sh
- Linux (VSCode Server): Use web browser to preview application.
- Windows: Use web browser to visit localhost URL.

#### Document Summarization

Lab: https://catalog.workshops.aws/building-with-amazon-bedrock/en-US/intermediate/bedrock-summarization

Code: building_with_amazon_bedrock/completed/summarization

- $ cd building_with_amazon_bedrock
- $ cd completed/summarization
- $ ./run_summarization_app.sh
- Linux (VSCode Server): Use web browser to preview application.
- Windows: Use web browser to visit localhost URL.
