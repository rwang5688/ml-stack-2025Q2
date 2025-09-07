import streamlit as st
import sys
import os

# Set environment variable to skip Python execution prompts to prevent UI hanging
os.environ["STRANDS_AUTO_APPROVE"] = "true"

# Add the current directory to the Python path to import the agents
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from strands import Agent
    from sagemaker_model import create_simple_agent
    from english_assistant import english_assistant
    from language_assistant import language_assistant
    from math_assistant import math_assistant
    from computer_science_assistant import computer_science_assistant
    from no_expertise import general_assistant
    
    # Define the teacher system prompt
    TEACHER_SYSTEM_PROMPT = """
    You are TeachAssist, a sophisticated educational orchestrator designed to coordinate educational support across multiple subjects. Your role is to:

    1. Analyze incoming student queries and determine the most appropriate specialized agent to handle them:
       - Math Agent: For mathematical calculations, problems, and concepts
       - English Agent: For writing, grammar, literature, and composition
       - Language Agent: For translation and language-related queries
       - Computer Science Agent: For programming, algorithms, data structures, and code execution
       - General Assistant: For all other topics outside these specialized domains

    2. Key Responsibilities:
       - Accurately classify student queries by subject area
       - Route requests to the appropriate specialized agent
       - Maintain context and coordinate multi-step problems
       - Ensure cohesive responses when multiple agents are needed

    3. Decision Protocol:
       - If query involves calculations/numbers → Math Agent
       - If query involves writing/literature/grammar → English Agent
       - If query involves translation → Language Agent
       - If query involves programming/coding/algorithms/computer science → Computer Science Agent
       - If query is outside these specialized areas → General Assistant
       - For complex queries, coordinate multiple agents as needed

    Always confirm your understanding before routing to ensure accurate assistance.
    """

    # Create the teacher agent with SageMaker integration
    teacher_agent = create_simple_agent(
        system_prompt=TEACHER_SYSTEM_PROMPT,
        tools=[math_assistant, language_assistant, english_assistant, computer_science_assistant, general_assistant],
    )
    
    AGENTS_AVAILABLE = True
except ImportError as e:
    st.error(f"Could not import required modules: {e}")
    AGENTS_AVAILABLE = False

# Set page config
st.set_page_config(
    page_title="Teacher's Assistant Chatbot (SageMaker)",
    page_icon="🎓",
    layout="wide"
)

# Main title
st.title("🎓 Teacher's Assistant Chatbot (SageMaker)")

# Welcome message
st.write("Welcome to your AI-powered educational assistant with SageMaker integration! Ask questions about math, English, computer science, languages, or any general topic.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask me anything about math, English, computer science, languages, or general topics..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    if AGENTS_AVAILABLE:
        try:
            # Get response from teacher agent
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = teacher_agent(prompt)
                    response_text = str(response)
                    st.markdown(response_text)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response_text})
        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            st.chat_message("assistant").markdown(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
    else:
        fallback_msg = "Sorry, the AI agents are not available. Please check that all required dependencies are installed."
        st.chat_message("assistant").markdown(fallback_msg)
        st.session_state.messages.append({"role": "assistant", "content": fallback_msg})

# Sidebar
st.sidebar.header("About")
st.sidebar.write("This is an AI-powered educational chatbot with SageMaker integration that can help with:")
st.sidebar.write("📊 **Math**: Calculations, algebra, geometry, statistics")
st.sidebar.write("📝 **English**: Writing, grammar, literature analysis")
st.sidebar.write("🌍 **Languages**: Translation and language learning")
st.sidebar.write("💻 **Computer Science**: Programming, algorithms, debugging")
st.sidebar.write("🧠 **General Topics**: Any other questions you might have")

# Configuration status
st.sidebar.header("SageMaker Configuration")
try:
    from config import get_sagemaker_endpoint, get_aws_region
    endpoint = get_sagemaker_endpoint()
    region = get_aws_region()
    st.sidebar.success("✅ SageMaker Connected")
    st.sidebar.write(f"**Endpoint**: {endpoint}")
    st.sidebar.write(f"**Region**: {region}")
except Exception as e:
    st.sidebar.error("❌ SageMaker Configuration Error")
    st.sidebar.write("Run `python setup_env.py` first")

st.sidebar.header("Features")
st.sidebar.write("- Multi-agent AI system")
st.sidebar.write("- Specialized subject experts")
st.sidebar.write("- Interactive chat interface")
st.sidebar.write("- Real-time responses")

# Clear chat button
if st.sidebar.button("Clear Chat History"):
    st.session_state.messages = []
    st.rerun()