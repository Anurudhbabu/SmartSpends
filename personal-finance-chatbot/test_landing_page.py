#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify the landing page is working correctly
"""

import requests
import time

def test_landing_page():
    """Test if the landing page loads correctly"""
    try:
        print("🧪 Testing SMARTSPENDS Landing Page")
        print("=" * 50)
        
        # Test the landing page
        url = "http://localhost:8502"
        
        print(f"📡 Testing connection to {url}...")
        
        # Wait a moment for the server to be fully ready
        time.sleep(3)
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            print("✅ Landing page is accessible!")
            print(f"   Status Code: {response.status_code}")
            print(f"   Content Length: {len(response.text)} bytes")
            
            # Check for key elements
            content = response.text.lower()
            
            checks = [
                ("smartspends", "SMARTSPENDS branding"),
                ("intelligent money companion", "Hero subtitle"),
                ("gemini", "AI technology mention"),
                ("get started", "CTA button"),
                ("features", "Features section"),
                ("why choose", "Why choose section")
            ]
            
            print("\n🔍 Content Verification:")
            for keyword, description in checks:
                if keyword in content:
                    print(f"   ✅ {description}")
                else:
                    print(f"   ⚠️ {description} - Not found")
            
            return True
            
        else:
            print(f"❌ Landing page returned status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the landing page")
        print("   Make sure the Streamlit app is running on port 8502")
        return False
        
    except Exception as e:
        print(f"❌ Error testing landing page: {e}")
        return False

if __name__ == "__main__":
    success = test_landing_page()
    
    if success:
        print("\n🎉 SMARTSPENDS Landing Page Test: PASSED")
        print("🌐 Access your new landing page at: http://localhost:8502")
        print("📱 Or on network: http://192.168.1.6:8502")
    else:
        print("\n❌ SMARTSPENDS Landing Page Test: FAILED")
        print("🔧 Check the Streamlit console for errors")