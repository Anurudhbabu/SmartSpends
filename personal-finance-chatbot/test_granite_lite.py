#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to demonstrate Granite Lite mode functionality.
This shows the enhanced rule-based system working immediately.
"""

from src.chatbot.granite_smart_client import GraniteSmartClient

def test_granite_lite():
    """Test the Granite Lite mode functionality"""
    print("=" * 60)
    print("GRANITE LITE MODE DEMONSTRATION")
    print("=" * 60)
    
    # Force Lite mode for immediate demonstration
    client = GraniteSmartClient(timeout_seconds=1, prefer_lite=True)
    
    print(f"📊 Client type: {type(client.client).__name__}")
    
    # Get model info
    print("\n📋 Model Information:")
    print("-" * 50)
    model_info = client.get_model_info()
    for key, value in model_info.items():
        if isinstance(value, list):
            print(f"• {key}:")
            for item in value:
                print(f"  - {item}")
        else:
            print(f"• {key}: {value}")
    
    # Test financial advice
    print("\n💡 Financial Advice Examples:")
    print("-" * 50)
    
    test_cases = [
        ("How do I start budgeting as a student?", "student"),
        ("I need help with emergency fund planning", "professional"),
        ("What's the best investment strategy?", "young_adult"),
        ("How do I pay off debt faster?", "general")
    ]
    
    for question, user_type in test_cases:
        print(f"\n❓ Question ({user_type}):")
        print(f"   {question}")
        print("💬 Response:")
        
        response = client.get_response(question, user_type)
        
        # Format the response nicely
        lines = response.split('\n')
        for line in lines:
            if line.strip():
                print(f"   {line}")
        print()
    
    print("=" * 60)
    print("✅ GRANITE LITE MODE TEST COMPLETE")
    print("All responses generated instantly using enhanced rules!")
    print("=" * 60)

if __name__ == "__main__":
    test_granite_lite()