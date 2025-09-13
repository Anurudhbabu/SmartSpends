# -*- coding: utf-8 -*-
import streamlit as st
import os
import sys
import json
from dotenv import load_dotenv
from datetime import datetime

# Fix Windows console encoding issues
if sys.platform == "win32":
    import codecs
    # Set console encoding to UTF-8 for Windows
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')
    # Set environment variable for Python UTF-8 mode
    os.environ["PYTHONIOENCODING"] = "utf-8"

# Load environment variables
load_dotenv()

# Import our enhanced modules
# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.chatbot.dual_ai_client import DualAIClient
from src.chatbot.nlp import NLPProcessor
from src.chatbot.finance_advisor import FinanceAdvisor
from src.utils.demographics import DemographicsManager

# Page configuration
st.set_page_config(
    page_title="Personal Finance AI",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'user_id' not in st.session_state:
    st.session_state.user_id = "default_user"
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'user_profile_complete' not in st.session_state:
    st.session_state.user_profile_complete = False
if 'show_app' not in st.session_state:
    st.session_state.show_app = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = "chat"
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

# Initialize components
@st.cache_resource
def initialize_components():
    """Initialize all chatbot components"""
    # Get Gemini API key from environment
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    granite_timeout = int(os.getenv('MODEL_TIMEOUT_SECONDS', 30))
    
    # Initialize Dual AI client (Gemini + Granite)
    ai_client = DualAIClient(gemini_api_key, granite_timeout)
    nlp_processor = NLPProcessor()
    finance_advisor = FinanceAdvisor()
    demographics_manager = DemographicsManager()
    
    return ai_client, nlp_processor, finance_advisor, demographics_manager

ai_client, nlp_processor, finance_advisor, demographics_manager = initialize_components()

def main():
    """Main application function"""
    st.title("💰 Personal Finance AI")
    st.write("Welcome to your personal finance assistant! How can I help you today?")
    
    # User input
    user_input = st.text_input("Ask me about your finances:", placeholder="e.g., How can I save more money this month?")
    
    if st.button("Send"):
        if user_input:
            with st.spinner("🤖 AI is thinking..."):
                try:
                    # Process input with NLP
                    nlp_result = nlp_processor.process_input(user_input)
                    
                    # Get user profile for personalized response
                    user_profile = demographics_manager.get_user_profile(st.session_state.user_id)
                    user_type = demographics_manager.determine_user_type(st.session_state.user_id)
                    
                    # Create enhanced user context for AI
                    user_context = {**user_profile, 'user_type': user_type} if user_profile else {'user_type': 'general'}
                    
                    # Generate response using Dual AI (Gemini + Granite)
                    response = ai_client.get_response(user_input, user_context)
                    
                    # Store in conversation history
                    st.session_state.conversation_history.append((user_input, response))
                    
                    # Display response
                    st.success("💡 **AI Financial Assistant Response:**")
                    st.write(response)
                    
                except Exception as e:
                    st.error(f"❌ System Error: {str(e)}")
                    st.info("🔄 Please try your question again.")
    
    # Display recent chat history
    if st.session_state.conversation_history:
        st.subheader("💬 Recent Conversations")
        for i, (question, answer) in enumerate(reversed(st.session_state.conversation_history[-3:])):
            with st.expander(f"Q: {question[:50]}..."):
                st.write("**You:** " + question)
                st.write("**Assistant:** " + answer)

if __name__ == "__main__":
    main()