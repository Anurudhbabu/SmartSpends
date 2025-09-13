#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integration test for the Granite-only Personal Finance Chatbot
Tests basic functionality without requiring browser automation
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from chatbot.granite_client import GraniteClient
from chatbot.nlp import NLPProcessor
from utils.demographics import DemographicsManager

def test_granite_client():
    """Test Granite client initialization and basic functionality"""
    print("Testing Granite Client...")
    
    try:
        client = GraniteClient()
        print(f"✅ Granite client initialized")
        print(f"   Model initialized: {client.initialized}")
        
        # Test response generation
        response = client.generate_financial_advice("What's a good savings rate?", "general")
        print(f"✅ Generated response: {response[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Granite client test failed: {e}")
        return False

def test_nlp_processor():
    """Test NLP processor without array boolean issues"""
    print("\nTesting NLP Processor...")
    
    try:
        nlp = NLPProcessor()
        print("✅ NLP processor initialized")
        
        # Test intent recognition
        intent, confidence = nlp.recognize_intent("How can I save money?")
        print(f"✅ Intent recognition: {intent} (confidence: {confidence:.2f})")
        
        # Test entity extraction
        entities = nlp.extract_entities("I earn $50000 per year")
        print(f"✅ Entity extraction: {entities}")
        
        return True
        
    except Exception as e:
        print(f"❌ NLP processor test failed: {e}")
        return False

def test_demographics_manager():
    """Test demographics manager"""
    print("\nTesting Demographics Manager...")
    
    try:
        demo = DemographicsManager()
        print("✅ Demographics manager initialized")
        
        # Test user profile creation
        test_profile = {
            'age': 25,
            'occupation': 'student',
            'income': 20000,
            'experience_level': 'beginner',
            'goals': ['save_money'],
            'risk_tolerance': 'conservative'
        }
        
        demo.add_user_profile("test_user", test_profile)
        user_type = demo.determine_user_type("test_user")
        print(f"✅ User type determination: {user_type}")
        
        return True
        
    except Exception as e:
        print(f"❌ Demographics manager test failed: {e}")
        return False

def main():
    """Run all integration tests"""
    print("🚀 Running Granite-Only Finance Chatbot Integration Tests\n")
    
    tests = [
        test_granite_client,
        test_nlp_processor, 
        test_demographics_manager
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The Granite integration is working correctly.")
        print("✅ Application should be running without errors at http://localhost:8503")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    main()