# -*- coding: utf-8 -*-
"""
Dual AI Client: Gemini Primary + Granite Fallback
"""

import os
from typing import Dict, Any, Optional
from .gemini_client import GeminiClient
from .granite_smart_client import GraniteSmartClient

class DualAIClient:
    """
    Smart AI client that uses Gemini as primary and Granite as fallback
    """
    
    def __init__(self, gemini_api_key: str, granite_timeout: int = 30):
        """
        Initialize the dual AI client
        
        Args:
            gemini_api_key: Google Gemini API key
            granite_timeout: Timeout for Granite model loading
        """
        self.gemini_api_key = gemini_api_key
        self.granite_timeout = granite_timeout
        
        # Initialize both clients
        self.gemini_client = None
        self.granite_client = None
        self.active_ai = None
        
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize both AI clients"""
        print("🤖 Initializing Dual AI System...")
        
        # Try to initialize Gemini first
        try:
            print("🔮 Initializing Gemini AI (Primary)...")
            self.gemini_client = GeminiClient(self.gemini_api_key)
            
            if self.gemini_client.initialized:
                self.active_ai = "gemini"
                print("✅ Gemini AI is active as primary AI")
            else:
                print("⚠️ Gemini initialization failed, falling back to Granite...")
                
        except Exception as e:
            print(f"❌ Gemini initialization error: {e}")
            print("🔄 Falling back to Granite AI...")
        
        # Initialize Granite as fallback
        try:
            print("🔧 Initializing Granite AI (Fallback)...")
            self.granite_client = GraniteSmartClient(
                timeout_seconds=self.granite_timeout, 
                prefer_lite=True  # Use Lite for fast fallback
            )
            
            if not self.active_ai:  # If Gemini failed
                self.active_ai = "granite"
                print("✅ Granite AI is active as primary (Gemini unavailable)")
            else:
                print("✅ Granite AI ready as fallback")
                
        except Exception as e:
            print(f"❌ Granite initialization error: {e}")
    
    def get_response(self, user_input: str, user_context: Dict[str, Any]) -> str:
        """
        Get AI response with smart fallback
        
        Args:
            user_input: User's question
            user_context: User demographics and context
            
        Returns:
            AI-generated response
        """
        # Try Gemini first if available
        if self.active_ai == "gemini" and self.gemini_client and self.gemini_client.initialized:
            try:
                print("🔮 Using Gemini AI...")
                response = self.gemini_client.get_response(user_input, user_context)
                if response and len(response.strip()) > 10:  # Valid response
                    return f"🔮 **Gemini AI Response:**\n\n{response}"
                else:
                    print("⚠️ Gemini returned empty response, trying Granite...")
                    
            except Exception as e:
                print(f"❌ Gemini error: {e}, falling back to Granite...")
        
        # Fallback to Granite
        if self.granite_client:
            try:
                print("🔧 Using Granite AI (fallback)...")
                response = self.granite_client.get_response(user_input, user_context)
                if response and len(response.strip()) > 10:
                    granite_info = self.granite_client.get_model_info()
                    model_name = granite_info.get('model_name', 'Granite AI')
                    return f"🔧 **{model_name} Response:**\n\n{response}"
                    
            except Exception as e:
                print(f"❌ Granite error: {e}")
        
        # Ultimate fallback
        return """🤖 **System Message:**

I apologize, but I'm experiencing technical difficulties with both AI systems right now. Here are some general financial tips:

💡 **Quick Financial Advice:**
- Follow the 50/30/20 budgeting rule (50% needs, 30% wants, 20% savings)
- Build an emergency fund with 3-6 months of expenses
- Start investing early, even small amounts compound over time
- Pay off high-interest debt first
- Consider your risk tolerance when investing

Please try asking your question again in a moment, or check your internet connection."""
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the active AI model"""
        if self.active_ai == "gemini" and self.gemini_client:
            info = self.gemini_client.get_model_info()
            info['system'] = 'Dual AI (Gemini Primary)'
            info['fallback'] = 'Granite AI available'
            return info
            
        elif self.granite_client:
            info = self.granite_client.get_model_info()
            info['system'] = 'Dual AI (Granite Active)'
            info['primary_status'] = 'Gemini unavailable'
            return info
            
        else:
            return {
                'model_name': 'No AI Available',
                'system': 'Dual AI (Both Failed)',
                'initialized': False,
                'capabilities': ['Basic responses only']
            }
    
    def test_connections(self) -> Dict[str, bool]:
        """Test both AI connections"""
        results = {}
        
        # Test Gemini
        if self.gemini_client:
            results['gemini'] = self.gemini_client.test_connection()
        else:
            results['gemini'] = False
            
        # Test Granite
        if self.granite_client:
            try:
                test_response = self.granite_client.get_response("Hello", {})
                results['granite'] = len(test_response.strip()) > 5
            except:
                results['granite'] = False
        else:
            results['granite'] = False
            
        return results
    
    def switch_to_granite(self):
        """Manually switch to Granite AI"""
        if self.granite_client:
            self.active_ai = "granite"
            print("🔧 Switched to Granite AI")
        else:
            print("❌ Granite AI not available")
    
    def switch_to_gemini(self):
        """Manually switch to Gemini AI"""
        if self.gemini_client and self.gemini_client.initialized:
            self.active_ai = "gemini"
            print("🔮 Switched to Gemini AI")
        else:
            print("❌ Gemini AI not available")
    
    def get_gemini_response(self, user_input: str, user_context: Dict[str, Any]) -> str:
        """Get response specifically from Gemini AI"""
        if self.gemini_client and self.gemini_client.initialized:
            try:
                response = self.gemini_client.get_response(user_input, user_context)
                return response if response else "Sorry, I couldn't generate a response right now."
            except Exception as e:
                return f"Gemini AI is currently unavailable. Error: {str(e)}"
        return "Gemini AI is not available. Please try Granite AI."
    
    def get_granite_response(self, user_input: str, user_context: Dict[str, Any]) -> str:
        """Get response specifically from Granite AI"""
        if self.granite_client:
            try:
                # Enhanced prompt for better financial advice
                enhanced_prompt = f"As a financial advisor, provide specific actionable advice for: {user_input}"
                response = self.granite_client.get_response(enhanced_prompt, user_context)
                return response if response else "Sorry, I couldn't generate a response right now."
            except Exception as e:
                return f"Granite AI is currently unavailable. Error: {str(e)}"
        return "Granite AI is not available. Please try Gemini AI."
    
    def get_status(self) -> str:
        """Get current system status"""
        gemini_status = "✅ Ready" if (self.gemini_client and self.gemini_client.initialized) else "❌ Unavailable"
        granite_status = "✅ Ready" if self.granite_client else "❌ Unavailable"
        
        return f"""🤖 **Dual AI System Status:**

🔮 **Gemini AI (Primary):** {gemini_status}
🔧 **Granite AI (Fallback):** {granite_status}
🎯 **Currently Active:** {self.active_ai.title() if self.active_ai else 'None'}

The system automatically uses the best available AI for your queries."""