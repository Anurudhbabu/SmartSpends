#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test the full app flow to identify the issue
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(project_root, 'src'))

def test_full_flow():
    """Test the complete flow that the app uses"""
    try:
        print("🧪 Testing Full App Flow")
        print("=" * 50)
        
        # Import components
        from chatbot.dual_ai_client import DualAIClient
        from chatbot.nlp import NLPProcessor
        from chatbot.finance_advisor import FinanceAdvisor
        from utils.demographics import DemographicsManager
        
        # Initialize components (same as app.py)
        gemini_api_key = os.getenv('GEMINI_API_KEY')
        granite_timeout = int(os.getenv('MODEL_TIMEOUT_SECONDS', 30))
        
        print(f"🔑 API Key (first 10): {gemini_api_key[:10]}...")
        print(f"⏱️ Timeout: {granite_timeout}s")
        
        # Initialize AI client
        print("\n🤖 Initializing Dual AI Client...")
        ai_client = DualAIClient(gemini_api_key, granite_timeout)
        
        print("\n📊 AI Client Info:")
        model_info = ai_client.get_model_info()
        print(f"  Model: {model_info.get('model_name')}")
        print(f"  System: {model_info.get('system')}")
        print(f"  Initialized: {model_info.get('initialized')}")
        
        # Initialize other components
        nlp_processor = NLPProcessor()
        demographics_manager = DemographicsManager()
        
        # Test user profile
        print("\n👤 Setting up test user...")
        user_id = "test_user"
        user_data = {
            'age': 25,
            'occupation': 'student',
            'income': 500,
            'experience_level': 'beginner',
            'goals': ['Build Emergency Fund'],
            'risk_tolerance': 'moderate'
        }
        
        demographics_manager.add_user_profile(user_id, user_data)
        user_profile = demographics_manager.get_user_profile(user_id)
        user_type = demographics_manager.determine_user_type(user_id)
        
        print(f"  User Type: {user_type}")
        print(f"  Profile: {user_profile}")
        
        # Test the full flow
        print("\n💬 Testing Question Flow...")
        user_input = "How can I start saving money?"
        
        # Step 1: NLP Processing
        print("  1️⃣ Processing with NLP...")
        nlp_result = nlp_processor.process_input(user_input)
        print(f"     Intent: {nlp_result.get('intent')}")
        print(f"     Confidence: {nlp_result.get('confidence')}")
        
        # Step 2: Create user context
        print("  2️⃣ Creating user context...")
        user_context = {**user_profile, 'user_type': user_type}
        print(f"     Context keys: {list(user_context.keys())}")
        
        # Step 3: Get AI response
        print("  3️⃣ Getting AI response...")
        response = ai_client.get_response(user_input, user_context)
        print(f"     Response length: {len(response)} characters")
        print(f"     Response preview: {response[:100]}...")
        
        # Step 4: Adapt communication style
        print("  4️⃣ Adapting communication style...")
        adapted_response = demographics_manager.adapt_communication_style(
            user_id, response
        )
        print(f"     Adapted length: {len(adapted_response)} characters")
        print(f"     Adapted preview: {adapted_response[:100]}...")
        
        # Check if the issue is here
        if "I'm having trouble processing your request" in response:
            print("❌ ERROR FOUND: Gemini is returning error message!")
            print(f"Full response: {response}")
        elif "I'm having trouble processing your request" in adapted_response:
            print("❌ ERROR FOUND: Communication adapter is corrupting response!")
            print(f"Original: {response}")
            print(f"Adapted: {adapted_response}")
        else:
            print("✅ Flow completed successfully!")
            print(f"\n📝 Final Response:")
            print(adapted_response)
        
        return True
        
    except Exception as e:
        print(f"❌ Error in flow test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_full_flow()