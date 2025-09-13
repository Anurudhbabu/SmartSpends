#!/usr/bin/env python3
"""
Quick speed test for the chatbot response time
"""

import time
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.chatbot.granite_smart_client import GraniteSmartClient

def test_response_speed():
    """Test how fast the chatbot responds"""
    print("🧪 Testing chatbot response speed...")
    
    # Initialize with Full AI mode preference
    print("⚡ Initializing Granite client (Full AI mode preferred)...")
    start_time = time.time()
    
    granite_client = GraniteSmartClient(timeout_seconds=300, prefer_lite=False)
    init_time = time.time() - start_time
    
    print(f"✅ Initialization took: {init_time:.2f} seconds")
    
    # Test a simple query
    print("\n💬 Testing response to: 'How should I budget my money?'")
    start_time = time.time()
    
    response = granite_client.get_response("How should I budget my money?", {
        'age': 25,
        'occupation': 'Professional',
        'income': 5000,
        'experience_level': 'Beginner'
    })
    
    response_time = time.time() - start_time
    
    print(f"⚡ Response took: {response_time:.2f} seconds")
    print(f"📝 Response preview: {response[:100]}...")
    
    # Check model info
    model_info = granite_client.get_model_info()
    print(f"\n🤖 Model Status: {model_info}")
    
    if response_time < 2.0:
        print("🎉 EXCELLENT! Response time under 2 seconds - Granite Lite is working perfectly!")
    elif response_time < 5.0:
        print("✅ GOOD! Response time under 5 seconds")
    else:
        print("⚠️  SLOW! Response time over 5 seconds - may still be trying to load full model")

if __name__ == "__main__":
    test_response_speed()