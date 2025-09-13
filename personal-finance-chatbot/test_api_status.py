#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test API status and check for any rate limiting or issues
"""

import os
import sys
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_api_status():
    """Test API status and rate limits"""
    try:
        import google.generativeai as genai
        
        # Get API key
        api_key = os.getenv('GEMINI_API_KEY')
        print(f"🔑 Testing API Key: {api_key[:10]}...{api_key[-4:]}")
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Test with different models
        models_to_test = [
            'gemini-1.5-flash',
            'gemini-1.5-pro'
        ]
        
        for model_name in models_to_test:
            print(f"\n🧪 Testing {model_name}...")
            try:
                model = genai.GenerativeModel(model_name)
                
                # Quick test
                start_time = time.time()
                response = model.generate_content("Hello")
                end_time = time.time()
                
                print(f"✅ {model_name}: {response.text[:50]}... ({end_time-start_time:.2f}s)")
                
            except Exception as e:
                print(f"❌ {model_name}: {e}")
        
        # Test rate limiting by sending multiple requests
        print(f"\n⚡ Testing rate limits with gemini-1.5-flash...")
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        for i in range(5):
            try:
                start_time = time.time()
                response = model.generate_content(f"Test request {i+1}: What is {i+1} + {i+1}?")
                end_time = time.time()
                
                print(f"   Request {i+1}: ✅ ({end_time-start_time:.2f}s) - {response.text.strip()}")
                
            except Exception as e:
                print(f"   Request {i+1}: ❌ - {e}")
                break
                
        return True
        
    except Exception as e:
        print(f"❌ API Test Failed: {e}")
        return False

def test_quota_info():
    """Try to get quota information"""
    try:
        import google.generativeai as genai
        
        api_key = os.getenv('GEMINI_API_KEY')
        genai.configure(api_key=api_key)
        
        print(f"\n📊 Checking API usage...")
        
        # List available models
        models = list(genai.list_models())
        print(f"Available models: {len(models)}")
        
        for model in models[:3]:  # Show first 3
            print(f"  - {model.name}")
            
        return True
        
    except Exception as e:
        print(f"❌ Quota check failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Google Gemini API Status Check")
    print("=" * 50)
    
    api_test = test_api_status()
    quota_test = test_quota_info()
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results:")
    print(f"  API Functionality: {'✅ PASS' if api_test else '❌ FAIL'}")
    print(f"  Quota Information: {'✅ PASS' if quota_test else '❌ FAIL'}")
    
    if api_test:
        print("\n💡 The API is working correctly. The issue might be in the app logic.")
    else:
        print("\n⚠️ There's an issue with the API. Check your API key and quota.")