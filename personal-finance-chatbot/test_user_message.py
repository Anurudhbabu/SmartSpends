#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test exactly what happens when a user sends a message
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(project_root, 'src'))

def test_multiple_messages():
    """Test multiple messages to see if rate limiting is the issue"""
    try:
        from chatbot.dual_ai_client import DualAIClient
        from utils.demographics import DemographicsManager
        
        # Initialize components
        gemini_api_key = os.getenv('GEMINI_API_KEY')
        ai_client = DualAIClient(gemini_api_key, 30)
        demographics_manager = DemographicsManager()
        
        # Set up user
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
        user_context = {**user_profile, 'user_type': user_type}
        
        # Test different messages
        test_messages = [
            "How can I save money?",
            "What is the best investment strategy?",
            "How do I budget my money?",
            "Should I pay off debt first?",
            "What is compound interest?"
        ]
        
        print("🧪 Testing Multiple Messages")
        print("=" * 50)
        
        for i, message in enumerate(test_messages, 1):
            print(f"\n📝 Test {i}: '{message}'")
            
            try:
                response = ai_client.get_response(message, user_context)
                
                if "I'm having trouble processing your request" in response:
                    print(f"❌ ERROR RESPONSE: {response}")
                elif "Sorry, I'm currently unavailable" in response:
                    print(f"⚠️ UNAVAILABLE: {response}")
                elif len(response) < 50:
                    print(f"⚠️ SHORT RESPONSE: {response}")
                else:
                    print(f"✅ SUCCESS: {len(response)} chars")
                    print(f"   Preview: {response[:100]}...")
                    
            except Exception as e:
                print(f"❌ EXCEPTION: {e}")
                
        # Test connection status
        print(f"\n🔗 Connection Status:")
        connections = ai_client.test_connections()
        print(f"  Gemini: {'✅' if connections.get('gemini') else '❌'}")
        print(f"  Granite: {'✅' if connections.get('granite') else '❌'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Setup error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_multiple_messages()