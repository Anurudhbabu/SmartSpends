#!/usr/bin/env python3
"""
Test the Dual AI System (Gemini + Granite)
"""

import os
import sys
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.chatbot.dual_ai_client import DualAIClient

def test_dual_ai():
    """Test both Gemini and Granite AI systems"""
    print("🧪 Testing Dual AI System...")
    print("=" * 50)
    
    # Get API key
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    if not gemini_api_key:
        print("❌ GEMINI_API_KEY not found in environment")
        return
        
    print(f"🔑 Using Gemini API Key: {gemini_api_key[:10]}...")
    
    # Initialize dual client
    print("\n🚀 Initializing Dual AI Client...")
    start_time = time.time()
    
    ai_client = DualAIClient(gemini_api_key, granite_timeout=10)
    init_time = time.time() - start_time
    
    print(f"✅ Initialization completed in {init_time:.2f} seconds")
    
    # Show system status
    print("\n" + ai_client.get_status())
    
    # Test connections
    print("\n🔧 Testing AI Connections...")
    connections = ai_client.test_connections()
    print(f"🔮 Gemini Connection: {'✅ Working' if connections['gemini'] else '❌ Failed'}")
    print(f"🔧 Granite Connection: {'✅ Working' if connections['granite'] else '❌ Failed'}")
    
    # Test financial query
    print("\n💬 Testing Financial Query...")
    test_question = "How should a 25-year-old professional making $60,000 start investing?"
    
    user_context = {
        'age': 25,
        'occupation': 'professional',
        'income': 5000,
        'experience_level': 'beginner',
        'goals': ['Save for Retirement', 'Build Emergency Fund'],
        'risk_tolerance': 'moderate'
    }
    
    print(f"Question: {test_question}")
    print("User Context:", user_context)
    
    print("\n⏱️ Generating response...")
    start_time = time.time()
    
    response = ai_client.get_response(test_question, user_context)
    response_time = time.time() - start_time
    
    print(f"\n⚡ Response time: {response_time:.2f} seconds")
    print("\n" + "="*50)
    print("🤖 AI RESPONSE:")
    print("="*50)
    print(response)
    print("="*50)
    
    # Get model info
    print("\n📊 Active Model Info:")
    model_info = ai_client.get_model_info()
    for key, value in model_info.items():
        print(f"• {key}: {value}")

if __name__ == "__main__":
    test_dual_ai()