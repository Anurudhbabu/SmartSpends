#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug script to test Gemini API integration
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(project_root, 'src'))

def test_gemini_api():
    """Test Gemini API directly"""
    try:
        import google.generativeai as genai
        
        # Get API key
        api_key = os.getenv('GEMINI_API_KEY')
        print(f"API Key (first 10 chars): {api_key[:10]}...")
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Test with simple model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Simple test
        print("\n🔮 Testing Gemini API...")
        response = model.generate_content("Hello, please respond with 'Gemini is working correctly'")
        
        print(f"✅ Raw Response: {response}")
        print(f"✅ Response Text: {response.text}")
        
        # Test with financial question
        print("\n💰 Testing financial advice...")
        financial_response = model.generate_content("""
        You are a financial advisor. A 25-year-old student with $500 monthly income asks:
        "How can I start saving money?"
        
        Provide a brief, helpful response.
        """)
        
        print(f"✅ Financial Response: {financial_response.text}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing Gemini API: {e}")
        print(f"❌ Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

def test_gemini_client():
    """Test our GeminiClient class"""
    try:
        from chatbot.gemini_client import GeminiClient
        
        api_key = os.getenv('GEMINI_API_KEY')
        client = GeminiClient(api_key)
        
        print(f"\n🤖 GeminiClient initialized: {client.initialized}")
        
        if client.initialized:
            # Test connection
            connection_test = client.test_connection()
            print(f"🔗 Connection test: {connection_test}")
            
            # Test response
            user_context = {
                'age': 25,
                'occupation': 'student',
                'income': 500,
                'experience_level': 'beginner',
                'goals': ['Build Emergency Fund'],
                'risk_tolerance': 'moderate'
            }
            
            response = client.get_response("How can I start saving money?", user_context)
            print(f"💬 Response: {response}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing GeminiClient: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Debugging Gemini Integration")
    print("=" * 50)
    
    # Test 1: Direct API
    print("\n1️⃣ Testing Gemini API directly...")
    api_test = test_gemini_api()
    
    # Test 2: Our client
    print("\n2️⃣ Testing our GeminiClient...")
    client_test = test_gemini_client()
    
    print("\n" + "=" * 50)
    print(f"📊 Results:")
    print(f"  Direct API: {'✅ PASS' if api_test else '❌ FAIL'}")
    print(f"  GeminiClient: {'✅ PASS' if client_test else '❌ FAIL'}")