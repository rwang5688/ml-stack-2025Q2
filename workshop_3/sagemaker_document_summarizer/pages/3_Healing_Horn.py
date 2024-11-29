import uuid
import boto3
import pandas as pd
import streamlit as st
import json
import logging
from botocore.client import Config

st.set_page_config(
    page_title="Healing Horn Agent",
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


bedrock_config = Config(connect_timeout=120, read_timeout=120, retries={'max_attempts': 0})
bedrock_client = boto3.client('bedrock-agent-runtime', config=bedrock_config)


### Complete this section after setting up an agent in Amazon Bedrock integrated with the knowledge base from WiscomCare and the given lambda function
### TODO fill in values
agentId='5JQ7JSZUXG'
agentAliasId='0OYTF8GAAH' #Version1
agentAliasId='AYQA2JTG1B' #Verison2
sessionId=f'{uuid.uuid4()}'

def invoke_agent(agentId,agentAliasId,sessionId,inputText):
    
    response = bedrock_client.invoke_agent(
        sessionState={
            'sessionAttributes': {
                'string': 'string'
            },
            'promptSessionAttributes': {
                'string': 'string'
            }
        },
        agentId=agentId,
        agentAliasId=agentAliasId,
        sessionId=sessionId,
        enableTrace=True,
        inputText=inputText
    )
    
    
    event_stream = response['completion']
   
    try:
        for event in event_stream:      
            if 'chunk' in event:
                data = event['chunk']['bytes']
                answer = data.decode('utf8')
            elif 'trace' in event:
                logging.info(json.dumps(event['trace'], indent=2))
                print(event['trace'])
            else:
                raise Exception("unexpected event.", event)
    except Exception as e:
        raise Exception("unexpected event.", e)
    
    return answer
    





if __name__ == "__main__":
    
    st.title(":rainbow[UniCare Generative AI]")

    st.header(":unicorn_face: :violet[Healing Horn]")
    st.subheader("_Magical Healing Agent_", divider='rainbow')
    
    agent_url = "https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html"
    st.markdown("Hi, my name is Healing Horn, your AI healthcare agent powered by [Agents for Amazon Bedrock](%s). I can retrieve medical records such as patient's status, conditions, and policy type for improved quality of care. You can ask me questions like:" % agent_url)
    st.markdown("- Query patient_id 9 in bullet points")
    st.markdown("- Does patient_id 9 need a surgery")
    st.markdown("- What are some facts of conditions, treatment, and prevention for patient_id 9?")
    st.markdown("- How can lung cancer patients improve their quality of life?")
    st.markdown("- Does patient_id 9 have sufficient insurance coverage for their condition?")
    st.divider()
    
    text = st.text_input("Enter a question for patient_id ranges from 1 to 100", placeholder='Type here...', help="Patient ID ranges from 1 to 100")
    
    if text != "":
        st.write(f'You entered: ', text)
        with st.spinner(text="Working on it..."):
            response = invoke_agent(
                agentId=agentId,
                agentAliasId=agentAliasId,
                sessionId=sessionId,
                inputText=text
                )
            with st.container():
                st.markdown(response)

        
