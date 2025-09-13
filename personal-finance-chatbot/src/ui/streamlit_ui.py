import streamlit as st
import sys
import os

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.chatbot.granite_smart_client import GraniteSmartClient
from src.chatbot.nlp import NLPProcessor
from src.chatbot.finance_advisor import FinanceAdvisor
from src.utils.demographics import DemographicsManager

# Initialize the Granite client, NLP processor, finance advisor, and demographics manager
granite_client = GraniteSmartClient()
nlp_processor = NLPProcessor()
finance_advisor = FinanceAdvisor()
demographics_manager = DemographicsManager()

# Streamlit UI layout
st.title("Personal Finance Chatbot")
st.write("Welcome to your personal finance assistant! How can I help you today?")

# User input
user_input = st.text_input("You:", "")

if st.button("Send"):
    if user_input:
        # Process user input with NLP
        intent, entities = nlp_processor.process_input(user_input)
        
        # Get demographic information (if any)
        user_demographics = demographics_manager.get_user_demographics()
        
        # Generate response based on intent and demographics
        if intent == "financial_advice":
            response = finance_advisor.provide_advice(entities, user_demographics)
        else:
            response = granite_client.get_response(user_input)
        
        # Display the chatbot response
        st.write("Chatbot:", response)
    else:
        st.write("Please enter a message.")