# -*- coding: utf-8 -*-
"""
Google Gemini AI Client for Personal Finance Chatbot
"""

import os
import google.generativeai as genai
from typing import Dict, Any, Optional

class GeminiClient:
    """
    Google Gemini AI client for generating personalized financial advice
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the Gemini client
        
        Args:
            api_key: Google Gemini API key
        """
        self.api_key = api_key
        self.initialized = False
        self.model = None
        
        try:
            # Configure Gemini API
            genai.configure(api_key=api_key)
            
            # Initialize the model (using Gemini 1.5 Flash for speed and efficiency)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            self.initialized = True
            print("✅ Gemini AI client initialized successfully!")
            
        except Exception as e:
            print(f"❌ Failed to initialize Gemini client: {e}")
            self.initialized = False
    
    def get_response(self, user_input: str, user_context: Dict[str, Any]) -> str:
        """
        Generate a response using Gemini AI
        
        Args:
            user_input: User's question or query
            user_context: User demographics and context
            
        Returns:
            AI-generated response
        """
        if not self.initialized:
            return "Sorry, I'm currently unavailable. Please try again later."
        
        # Sanitize input
        if not user_input or len(user_input.strip()) == 0:
            return "Please ask me a financial question!"
        
        # Clean and limit input length
        user_input = user_input.strip()
        if len(user_input) > 500:
            user_input = user_input[:500] + "..."
        
        try:
            # Create a detailed prompt for financial advice
            prompt = self._create_financial_prompt(user_input, user_context)
            
            # Generate response with timeout and safety settings
            generation_config = genai.types.GenerationConfig(
                max_output_tokens=800,  # Limit response length
                temperature=0.7,        # Balance creativity and accuracy
                top_p=0.9
            )
            
            response = self.model.generate_content(
                prompt, 
                generation_config=generation_config,
                request_options={'timeout': 15}  # 15 second timeout
            )
            
            if response.text and len(response.text.strip()) > 10:
                return response.text.strip()
            else:
                print(f"⚠️ Gemini returned empty or very short response: '{response.text}'")
                return "I couldn't generate a detailed response right now. Please rephrase your question or try again."
                
        except Exception as e:
            error_msg = str(e).lower()
            print(f"❌ Error generating Gemini response: {e}")
            
            # Provide more specific error messages
            if "quota" in error_msg or "limit" in error_msg:
                return "The AI service has reached its usage limit. Please try again in a few minutes."
            elif "network" in error_msg or "connection" in error_msg:
                return "Network connection issue. Please check your internet connection and try again."
            elif "api" in error_msg or "key" in error_msg:
                return "API configuration issue. Please contact support."
            elif "safety" in error_msg or "blocked" in error_msg:
                return "Your request was blocked by content filters. Please rephrase your question."
            else:
                return f"I encountered a technical issue ({type(e).__name__}). Please try again or use simpler terms."
    
    def _create_financial_prompt(self, user_input: str, user_context: Dict[str, Any]) -> str:
        """
        Create a detailed prompt for financial advice
        """
        # Extract user context
        age = user_context.get('age', 'Not specified')
        occupation = user_context.get('occupation', 'Not specified')
        income = user_context.get('income', 'Not specified')
        experience_level = user_context.get('experience_level', 'beginner')
        goals = user_context.get('goals', [])
        risk_tolerance = user_context.get('risk_tolerance', 'moderate')
        
        # Create comprehensive prompt
        prompt = f"""You are a professional financial advisor AI assistant focusing on Indian financial context. Provide personalized, actionable financial advice.

USER PROFILE:
- Age: {age}
- Occupation: {occupation}
- Monthly Income: ₹{income} (if specified)
- Financial Experience: {experience_level}
- Financial Goals: {', '.join(goals) if goals else 'General financial wellness'}
- Risk Tolerance: {risk_tolerance}

USER QUESTION: {user_input}

INSTRUCTIONS:
1. Provide specific, actionable financial advice tailored to their profile and Indian financial context
2. Consider their age, income level, and experience when giving recommendations
3. Include concrete numbers, percentages, or rupee amounts when relevant
4. Use Indian financial instruments (PPF, EPF, SIP, NSC, etc.) when suggesting investments
5. Keep the response concise but comprehensive (3-4 paragraphs max)
6. Use a friendly, professional tone
7. If asking about specific investments, include appropriate disclaimers
8. Focus on practical steps they can take immediately
9. Use ₹ (INR) currency throughout your response

Please provide your personalized financial advice:"""

        return prompt
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the current model
        """
        return {
            'model_name': 'Google Gemini 1.5 Flash',
            'model_path': 'gemini-1.5-flash',
            'device': 'cloud',
            'initialized': self.initialized,
            'capabilities': [
                'Advanced conversational AI',
                'Real-time financial knowledge',
                'Personalized advice generation',
                'Context-aware responses',
                'Current market awareness'
            ]
        }
    
    def test_connection(self) -> bool:
        """
        Test if the Gemini connection is working
        """
        if not self.initialized:
            return False
            
        try:
            # Simple test query
            test_response = self.model.generate_content("Hello, please respond with 'Connection successful'")
            return test_response.text is not None
        except:
            return False