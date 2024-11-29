import boto3
from botocore.client import Config
import os
import streamlit as st
import langchain
from langchain_community.llms import Bedrock
from langchain_community.chat_models import BedrockChat
from langchain_aws import ChatBedrock
from langchain_community.retrievers import AmazonKnowledgeBasesRetriever
from langchain.chains import RetrievalQA
from langchain_aws import BedrockLLM


st.set_page_config(
    page_title="WisdomCare",
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


if __name__ == "__main__":
    
    st.title(":rainbow[UniCare Generative AI]")
    st.header(":medical_symbol: :green[WisdomCare]")
    st.subheader("_Health Information Knowledge Base_", divider='rainbow')
    
    kb_url = "https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html"
    
    st.markdown("Thanks for visiting WisdomCare powered by [Knowledge Base for Amazon Bedrock](%s)!" % kb_url)
    st.markdown("I am equipped to assist you with information such as causes, symptoms, and treatment for health topics including, alzheimer, arthritis, asthma, covid-19, ear infection, fibromyalgia, high blood pressure, kidney disease, lung cancer, or stroke.") 
    
    st.markdown("You can ask me questions like, \"_What are 5 key risk factors for lung cancer?_\", \"_What are the symptoms of fibromyalgia?_\", or \"_What is the treatment for ear infection?_\"")
    st.divider()
    
    ### Complete this section after setting up knowledge base in Amazon Bedrock console, TODO fill in values  
    retriever = AmazonKnowledgeBasesRetriever(
        knowledge_base_id="ZJ4CRKX8XX",
        retrieval_config={
            "vectorSearchConfiguration": {"numberOfResults": 4}},
    )
    
    
    
    modelId="anthropic.claude-3-haiku-20240307-v1:0"
    
    model_kwargs =  { 
    "max_tokens": 512,
    "temperature": 0.0,
}
    
    claude3_client = ChatBedrock(
        client=bedrock_runtime,
        model_id=modelId,
        model_kwargs=model_kwargs,
    )
    
    qa = RetrievalQA.from_chain_type(
        llm=claude3_client,
        retriever=retriever,
        return_source_documents=True
    )
    
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
        

    if prompt := st.chat_input("Ask me a question"):
        with st.chat_message("human"):
            st.markdown(prompt)
            
        st.session_state.messages.append({"role": "human", "content": prompt})
        
        with st.chat_message("assistant"):
            with st.spinner('Processing...'):
                message_placeholder = st.empty()
                full_response = ""
                answer = qa.invoke(prompt)
                full_response = answer['result']
                message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})


    

