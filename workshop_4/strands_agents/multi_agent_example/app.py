import streamlit as st
from strands import Agent
from strands.models import BedrockModel

# Import the specialized assistants
from computer_science_assistant import computer_science_assistant
from english_assistant import english_assistant
from language_assistant import language_assistant
from math_assistant import math_assistant
from no_expertise import general_assistant

# Define the teacher's assistant system prompt - focused on pure routing
TEACHER_SYSTEM_PROMPT = """
You are a routing agent that determines which specialist to call and returns their complete response.

Available specialists:
- math_assistant: For mathematical calculations, problems, and concepts
- english_assistant: For writing, grammar, literature, and composition  
- language_assistant: For translation and language-related queries
- computer_science_assistant: For programming, algorithms, data structures, and code execution
- general_assistant: For all other topics outside these specialized domains

Your process:
1. Analyze the user's query
2. Call the appropriate specialist tool with the user's exact query
3. Return the specialist's response exactly as provided - do not modify, summarize, or add to it

CRITICAL: Your final response must be identical to what the specialist tool returns. Do not add any commentary, questions, or additional text.
"""

# Set page config
st.set_page_config(
    page_title="Teacher's Assistant Chatbot (Bedrock)",
    page_icon="🎓",
    layout="wide"
)

# Main title
st.title("🎓 Teacher's Assistant Chatbot (Bedrock)")

# Welcome message
st.write("Welcome to your AI-powered educational assistant with Bedrock integration! Ask questions about math, English, computer science, languages, or any general topic.")

# Initialize session state for conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Initialize the teacher agent
@st.cache_resource
def get_teacher_agent():
    # Specify the Bedrock ModelID
    bedrock_model = BedrockModel(
        model_id="us.amazon.nova-pro-v1:0",
        temperature=0.1,  # Lower temperature for more consistent routing
    )
    
    # Create the teacher agent with specialized tools
    return Agent(
        model=bedrock_model,
        system_prompt=TEACHER_SYSTEM_PROMPT,
        callback_handler=None,
        tools=[math_assistant, language_assistant, english_assistant, computer_science_assistant, general_assistant],
    )

# React to user input
if prompt := st.chat_input("Ask me anything about math, English, computer science, languages, or general topics..."):

    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # Get the teacher agent
            teacher_agent = get_teacher_agent()
            
            # Process the query through the orchestrator
            with st.spinner("Thinking..."):
                response = teacher_agent(prompt)
                
                # Debug: Print response structure
                print(f"DEBUG - Bedrock response type: {type(response)}")
                print(f"DEBUG - Bedrock response: {response}")
                
                # Simplified response extraction - just convert to string like SageMaker version
                content = str(response)
                
                print(f"DEBUG - Bedrock final content: {content}")
                
                # If response looks like tool call JSON, there's still an issue
                if content.startswith('[{"name":') or content.startswith('{"name":'):
                    content = "I apologize, but there was an issue processing your request. Please try again."
            
            # Display the response
            message_placeholder.markdown(content)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": content})
            
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            message_placeholder.markdown(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})

# Sidebar
st.sidebar.header("About")
st.sidebar.write("This is an AI-powered educational chatbot with Bedrock integration that can help with:")
st.sidebar.write("📊 **Math**: Calculations, algebra, geometry, statistics")
st.sidebar.write("📝 **English**: Writing, grammar, literature analysis")
st.sidebar.write("🌍 **Languages**: Translation and language learning")
st.sidebar.write("💻 **Computer Science**: Programming, algorithms, debugging")
st.sidebar.write("🧠 **General Topics**: Any other questions you might have")

# Configuration status
st.sidebar.header("Bedrock Configuration")
try:
    # Get the model info from the cached agent
    teacher_agent = get_teacher_agent()
    model_id = "us.amazon.nova-pro-v1:0"  # We know this from the code
    st.sidebar.success("✅ Bedrock Connected")
    st.sidebar.write(f"**Model**: {model_id}")
    st.sidebar.write(f"**Provider**: Amazon Bedrock")
except Exception as e:
    st.sidebar.error("❌ Bedrock Configuration Error")
    st.sidebar.write("Check your AWS credentials and permissions")

st.sidebar.header("Features")
st.sidebar.write("- Multi-agent AI system")
st.sidebar.write("- Specialized subject experts")
st.sidebar.write("- Interactive chat interface")
st.sidebar.write("- Real-time responses")

# Clear chat button
if st.sidebar.button("Clear Chat History"):
    st.session_state.messages = []
    st.rerun()

# Force cache clear button for debugging
if st.sidebar.button("🔄 Force Refresh (Debug)"):
    st.cache_data.clear()
    st.cache_resource.clear()
    st.rerun()