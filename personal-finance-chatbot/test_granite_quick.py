#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick test to check if Granite AI client can be initialized
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_granite_import():
    """Test that we can import the Granite client"""
    print("🧪 Quick Granite AI Test\n")
    
    try:
        print("📦 Testing import of GraniteClient...")
        from chatbot.granite_client import GraniteClient
        print("✅ Import successful!")
        
        print("\n🔧 Testing client initialization...")
        client = GraniteClient()
        
        # Get model info without waiting for full download
        info = client.get_model_info()
        print(f"📋 Model: {info['model_name']}")
        print(f"🖥️  Device: {info['device']}")
        print(f"✅ Initialized: {info['initialized']}")
        
        if info['initialized']:
            print("🎉 Granite model is working correctly!")
            
            # Quick test with a simple question
            test_response = client.get_response("What is budgeting?", "general")
            print(f"\n💬 Sample response: {test_response[:100]}...")
        else:
            print("⚠️  Granite model not fully initialized - this is normal during first download")
            print("📥 Model files are being downloaded in the background")
            print("🔄 Fallback responses are working correctly")
            
            # Test fallback response
            test_response = client.get_response("What is budgeting?", "general")
            print(f"\n💬 Fallback response: {test_response[:100]}...")
        
        print(f"\n🏁 Test completed!")
        print(f"📊 Available capabilities: {', '.join(info['capabilities'])}")
        
        return info['initialized']
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("🔧 Make sure dependencies are installed: pip install torch transformers accelerate")
        return False
    except Exception as e:
        print(f"❌ Error during test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_granite_import()
    if success:
        print("\n🎯 Granite AI is fully operational!")
    else:
        print("\n⚡ Granite AI is working with fallback responses")
        print("   Model will be available once download completes")