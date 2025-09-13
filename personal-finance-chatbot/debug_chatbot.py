#!/usr/bin/env python3
"""
Quick debug script to test chatbot functionality
"""

import sys
import os

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def test_granite_client():
    """Test the Granite client directly"""
    print("=" * 50)
    print("Testing Granite Smart Client")
    print("=" * 50)
    
    try:
        from src.chatbot.granite_smart_client import GraniteSmartClient
        
        print("1. Initializing GraniteSmartClient...")
        client = GraniteSmartClient(timeout_seconds=10, prefer_lite=False)
        
        print("2. Getting model info...")
        model_info = client.get_model_info()
        print(f"Model: {model_info}")
        
        print("3. Testing basic response...")
        test_input = "How can I save more money?"
        response = client.get_response(test_input, "professional")
        print(f"Input: {test_input}")
        print(f"Response: {response}")
        
        return True
        
    except Exception as e:
        print(f"Error testing Granite client: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_demographics():
    """Test demographics manager"""
    print("\n" + "=" * 50)
    print("Testing Demographics Manager")
    print("=" * 50)
    
    try:
        from src.utils.demographics import DemographicsManager
        
        demographics = DemographicsManager()
        
        # Test adding a user profile
        user_data = {
            'age': 25,
            'occupation': 'professional',
            'income': 50000,
            'experience_level': 'intermediate',
            'goals': ['Save for Retirement', 'Build Emergency Fund'],
            'risk_tolerance': 'moderate'
        }
        
        print("1. Adding user profile...")
        demographics.add_user_profile("test_user", user_data)
        
        print("2. Getting user profile...")
        profile = demographics.get_user_profile("test_user")
        print(f"Profile: {profile}")
        
        print("3. Determining user type...")
        user_type = demographics.determine_user_type("test_user")
        print(f"User type: {user_type}")
        
        return True
        
    except Exception as e:
        print(f"Error testing demographics: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_nlp():
    """Test NLP processor"""
    print("\n" + "=" * 50)
    print("Testing NLP Processor")
    print("=" * 50)
    
    try:
        from src.chatbot.nlp import NLPProcessor
        
        nlp = NLPProcessor()
        
        test_input = "How can I save more money?"
        print(f"Processing: {test_input}")
        
        result = nlp.process_input(test_input)
        print(f"Result: {result}")
        
        return True
        
    except Exception as e:
        print(f"Error testing NLP: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Starting chatbot debugging...")
    
    success_count = 0
    
    if test_granite_client():
        success_count += 1
    
    if test_demographics():
        success_count += 1
    
    if test_nlp():
        success_count += 1
    
    print("\n" + "=" * 50)
    print(f"Debug Summary: {success_count}/3 components working")
    print("=" * 50)
    
    if success_count == 3:
        print("✅ All components working - issue might be in Streamlit integration")
    else:
        print("❌ Some components have issues - check error messages above")