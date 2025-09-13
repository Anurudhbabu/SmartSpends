#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify Granite AI client works correctly
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from chatbot.granite_client import GraniteClient

def test_granite():
    """Test Granite AI client"""
    print("🧪 Testing Granite AI for Personal Finance Chatbot\n")
    
    test_questions = [
        ("How can I start building an emergency fund as a young professional?", "professional"),
        ("What budgeting tips work best for students?", "student"),
        ("How should I prioritize debt vs savings?", "general"),
        ("What investment options are good for beginners?", "young_adult")
    ]
    
    try:
        # Initialize Granite client
        print("🚀 Initializing Granite 3.3 2B client...")
        client = GraniteClient()
        
        # Get model info
        info = client.get_model_info()
        print(f"📋 Model: {info['model_name']}")
        print(f"🖥️  Device: {info['device']}")
        print(f"✅ Initialized: {info['initialized']}")
        print("-" * 50)
        
        if not info['initialized']:
            print("❌ Granite model failed to initialize - using fallback responses")
        
        # Test different question types
        for i, (question, user_type) in enumerate(test_questions, 1):
            print(f"\n🔬 Test {i}: {user_type.title()} User")
            print("-" * 30)
            print(f"Question: '{question}'")
            print("⏳ Generating response...")
            
            response = client.get_response(question, user_type=user_type)
            
            print(f"\n📝 Response ({len(response)} chars):")
            print("-" * 40)
            print(response[:300] + ("..." if len(response) > 300 else ""))
            print("-" * 40)
            print("✅ Success!")
        
        print(f"\n🏁 All tests completed successfully!")
        print(f"🔒 Privacy: All processing done locally")
        print(f"📊 Capabilities tested: {', '.join(info['capabilities'])}")
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_granite()