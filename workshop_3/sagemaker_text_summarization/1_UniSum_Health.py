import os
import boto3
import sagemaker
import streamlit as st
from langchain_aws import ChatBedrock
from langchain_community.llms import Bedrock
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import AmazonTextractPDFLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

st.set_page_config(
    page_title="UniSum Health",
    page_icon=":🦄",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
    <style>
    .block-container {padding-top: 1rem;padding-bottom: 0rem;padding-left: 5rem;padding-right: 5rem}
    h1 {text-align: center;}
    MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)


target_region = os.environ.get("AWS_REGION")    
    
bedrock_runtime = boto3.client(
    service_name='bedrock-runtime',
    region_name=target_region,
    endpoint_url='https://bedrock-runtime.us-west-2.amazonaws.com'
)

s3 = boto3.client(
    service_name='s3',
    region_name=target_region,
)

textract_client = boto3.client("textract", region_name=target_region)


modelId = "anthropic.claude-3-haiku-20240307-v1:0"

model_kwargs =  { 
    "max_tokens": 512,
    "temperature": 0.0,
}

claude3_client = ChatBedrock(
    client=bedrock_runtime,
    model_id=modelId,
    model_kwargs=model_kwargs,
)

def read_file_from_s3(bucket_name, file_name):
    obj = s3.get_object(Bucket=bucket_name, Key=file_name)
    data = obj['Body'].read()
    return data


def summarize_text(data):  
    
    template = """
    %INSTRUCTIONS:
    Please summarize the following piece of text.
    
    %TEXT:
    {text}
    """
    
    prompt = PromptTemplate(
        input_variables=["text"],
        template=template,
    )
    
    messages = [
        ("human","{question}"),
    ]
    
    prompt = ChatPromptTemplate.from_messages(messages)
    chain = prompt | claude3_client | StrOutputParser()

    ### Complete this section, TODO fill in values
    # Chain Invoke
    response = chain.invoke(data)

    summary_chain = load_summarize_chain(
        llm=claude3_client,
        chain_type='map_reduce',
        verbose=False
    )
    
    st.write(response)
    st.divider() 



if __name__ == "__main__":

    st.title(":rainbow[UniCare Generative AI]")

    st.header(":stethoscope: :blue[UniSum Health]")
    st.subheader("_Your Medical Summary Assistant_", divider='rainbow')
    st.write("Our clinicians are busy! Please help us summarize medical transcripts so that we can focus on improving patient experience.")
    
    sess = sagemaker.Session()
    s3_bucket = sess.default_bucket()
    
    uploaded_file = st.file_uploader(label="Upload a transcript PDF here.")
    
    if uploaded_file is not None:
        s3.upload_fileobj(uploaded_file, s3_bucket, uploaded_file.name)
        file_path = f's3://{s3_bucket}/{uploaded_file.name}'
        st.write(f'Successfully uploaded to {file_path}')

        
        with st.spinner(text="Working on it..."):
            loader = AmazonTextractPDFLoader(file_path, client=textract_client)
            
            
            ### Complete this section, TODO fill in values
            # Load PDF and split into chunks.
            documents = loader.load_and_split()
            summarize_text(documents)
            
    

