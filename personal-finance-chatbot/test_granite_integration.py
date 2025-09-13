#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to demonstrate Granite model integration.
This script shows how the smart client automatically falls back to Lite mode
when the full model isn't immediately available.
"""

import time
from src.chatbot.granite_smart_client import GraniteSmartClient

def test_granite_integration():
    """Test the Granite integration with smart fallback"""
    print("=" * 60)
    print("GRANITE MODEL INTEGRATION TEST")
    print("=" * 60)
    
    # Test 1: Quick initialization (should use Lite mode)
    print("\n🔍 Test 1: Quick initialization (5 second timeout)")
    print("-" * 50)
    
    start_time = time.time()
    client = GraniteSmartClient(timeout_seconds=5)
    init_time = time.time() - start_time
    
    print(f"⏱️  Initialization time: {init_time:.2f} seconds")
    print(f"📊 Client type: {type(client.client).__name__}")
    print(f"🚀 Initialized status: {getattr(client.client, 'initialized', 'N/A')}")
    
    # Test 2: Get model info
    print("\n📋 Test 2: Model Information")
    print("-" * 50)
    model_info = client.get_model_info()
    for key, value in model_info.items():
        if isinstance(value, list):
            print(f"• {key}:")
            for item in value:
                print(f"  - {item}")
        else:
            print(f"• {key}: {value}")
    
    # Test 3: Test financial advice generation
    print("\n💡 Test 3: Financial Advice Generation")
    print("-" * 50)
    
    test_questions = [
        ("How do I start budgeting as a student?", "student"),
        ("What should I do with my 401k?", "professional"),
        ("Emergency fund advice", "general")
    ]
    
    for question, user_type in test_questions:
        print(f"\n❓ Question ({user_type}): {question}")
        print("💬 Response:")
        
        start_time = time.time()
        response = client.get_response(question, user_type)
        response_time = time.time() - start_time
        
        # Show first few lines of response
        lines = response.split('\n')
        for i, line in enumerate(lines[:5]):  # Show first 5 lines
            print(f"   {line}")
        if len(lines) > 5:
            print(f"   ... ({len(lines)-5} more lines)")
        
        print(f"⏱️  Response time: {response_time:.2f} seconds")
    
    # Test 4: Show download instructions for full model
    print("\n📥 Test 4: Full Model Download Instructions")
    print("-" * 50)
    
    if not getattr(client.client, 'initialized', False):
        print("🔄 Full Granite model is not currently loaded.")
        print("📋 To download and enable the full AI model (~5GB):")
        print()
        print("   python -c \"from src.chatbot.granite_client import GraniteClient; GraniteClient(timeout_seconds=3600)\"")
        print()
        print("💡 Benefits of full model:")
        print("   • More natural, conversational responses")
        print("   • Better context understanding")
        print("   • Personalized advice generation")
        print("   • Advanced financial reasoning")
        print()
        print("⚡ Current Lite mode benefits:")
        print("   • Instant responses (no download wait)")
        print("   • Comprehensive rule-based advice")
        print("   • Privacy-focused (all local)")
        print("   • No internet required after initial setup")
    else:
        print("✅ Full Granite model is loaded and ready!")
    
    print("\n" + "=" * 60)
    print("✅ GRANITE INTEGRATION TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    test_granite_integration()