# -*- coding: utf-8 -*-
import os
from typing import Dict, Any, Optional
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import threading
import time


class GraniteClient:
    """
    Granite 3.3 Client for local inference using Hugging Face transformers.
    Compatible with the Watson client interface for seamless integration.
    """
    
    def __init__(self, timeout_seconds: int = 60):
        self.model_path = "ibm-granite/granite-3.3-2b-base"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = None
        self.tokenizer = None
        self.max_length = 2048  # Reasonable limit for responses
        self.initialized = False
        self.download_timeout = timeout_seconds
        
        # Initialize model and tokenizer with timeout
        self._init_granite_with_timeout()
    
    def _init_granite_with_timeout(self):
        """Initialize Granite with a timeout for downloads"""
        # Check if model is already cached to skip timeout for cached models
        if self._is_model_cached():
            print("📁 Model found in cache - loading...")
            self._init_granite()
            return
        
        print(f"📥 Model not cached - downloading with {self.download_timeout}s timeout...")
        def init_worker():
            self._init_granite()
        
        init_thread = threading.Thread(target=init_worker)
        init_thread.daemon = True
        init_thread.start()
        init_thread.join(timeout=self.download_timeout)
        
        if init_thread.is_alive():
            print(f"⏱️  Download timeout ({self.download_timeout}s) - continuing with fallback responses")
            print("💡 To download the full model, run: python -c \"from src.chatbot.granite_client import GraniteClient; GraniteClient(timeout_seconds=3600)\"")
            self.initialized = False
        elif not self.initialized:
            print("🔄 Model download may still be in progress - using fallback responses for now")
    
    def _is_model_cached(self) -> bool:
        """Check if the model is already cached locally"""
        try:
            from huggingface_hub import snapshot_download
            cache_dir = snapshot_download(self.model_path, local_files_only=True)
            return True
        except:
            return False

    def _init_granite(self):
        """Initialize Granite model and tokenizer"""
        try:
            print(f"Loading Granite model on {self.device}...")
            
            # Load tokenizer with force_download to handle corrupted files
            print("Loading tokenizer...")
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_path, 
                force_download=True
            )
            
            # Load model with appropriate device mapping and force_download
            print("Loading model...")
            if self.device == "cuda":
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_path, 
                    device_map="auto",
                    torch_dtype=torch.bfloat16,
                    force_download=True
                )
            else:
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_path,
                    torch_dtype=torch.float32,
                    force_download=True
                )
                self.model = self.model.to(self.device)
            
            self.model.eval()
            self.initialized = True
            print("Granite model loaded successfully!")
            
        except Exception as e:
            print(f"Error initializing Granite model: {e}")
            print("This could be due to:")
            print("1. Network issues during download - retrying may help")
            print("2. Missing dependencies: pip install torch transformers accelerate")
            print("3. Insufficient disk space for the model (~5GB)")
            print("4. GPU memory issues (if using CUDA)")
            print("\nFalling back to rule-based responses...")
            self.initialized = False

    def create_session(self) -> Optional[str]:
        """Create a session (compatibility method - Granite doesn't need sessions)"""
        return "granite_session_local" if self.initialized else None

    def send_message_to_assistant(self, message: str) -> Dict[str, Any]:
        """Send message (compatibility method - returns simple success response)"""
        if not self.initialized:
            return {"error": "Granite model not initialized"}
        
        return {
            "output": {
                "generic": [{
                    "response_type": "text",
                    "text": "Message received by Granite client."
                }]
            }
        }

    def generate_financial_advice(self, prompt: str, user_type: str = "general") -> str:
        """Generate personalized financial advice using Granite model"""
        if not self.initialized:
            return self._fallback_financial_advice(prompt, user_type)
        
        # Create demographic-aware system prompt
        system_prompt = self._create_financial_system_prompt(user_type)
        full_prompt = f"{system_prompt}\n\nUser Query: {prompt}\n\nFinancial Advice:"
        
        try:
            # Tokenize input
            inputs = self.tokenizer(full_prompt, return_tensors="pt").to(self.device)
            
            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_length=min(inputs.input_ids.shape[1] + 400, self.max_length),
                    min_length=inputs.input_ids.shape[1] + 50,
                    temperature=0.3,
                    top_p=0.9,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    repetition_penalty=1.1
                )
            
            # Decode and extract new tokens only
            full_response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            advice = full_response[len(full_prompt):].strip()
            
            # Clean up the response
            advice = self._clean_response(advice)
            
            return advice if advice else self._fallback_financial_advice(prompt, user_type)
            
        except Exception as e:
            print(f"Error generating advice with Granite: {e}")
            return self._fallback_financial_advice(prompt, user_type)

    def _create_financial_system_prompt(self, user_type: str) -> str:
        """Create system prompt based on user demographics"""
        base_prompt = """You are a knowledgeable and helpful financial advisor. Provide clear, practical, and actionable financial advice. Keep responses concise but informative, focusing on specific steps the user can take."""
        
        if user_type == "student":
            return f"{base_prompt} You are speaking to a college student with limited income. Focus on budgeting basics, student discounts, building credit responsibly, and starting small emergency funds. Use encouraging, accessible language."
        
        elif user_type == "professional":
            return f"{base_prompt} You are advising a working professional. Include advice on maximizing employer benefits (401k matching, HSA), tax optimization strategies, investment diversification, and career-related financial planning."
        
        elif user_type == "young_adult":
            return f"{base_prompt} You are helping a young adult establish financial independence. Focus on emergency funds, debt management strategies, first-time home buying preparation, and building long-term wealth through consistent investing."
        
        elif user_type == "senior":
            return f"{base_prompt} You are assisting someone in or near retirement. Emphasize capital preservation, healthcare cost planning, estate planning considerations, and generating steady income from investments."
        
        return f"{base_prompt} Provide balanced financial advice suitable for someone seeking to improve their financial situation."

    def _clean_response(self, response: str) -> str:
        """Clean up the generated response"""
        # Remove common artifacts and repetitions
        response = response.strip()
        
        # Stop at common ending patterns
        stop_patterns = [
            "\n\nUser Query:",
            "\n\nFinancial Advice:",
            "\nUser:",
            "\nAssistant:",
            "\n---",
        ]
        
        for pattern in stop_patterns:
            if pattern in response:
                response = response.split(pattern)[0]
        
        # Remove excessive repetition at the end
        lines = response.split('\n')
        cleaned_lines = []
        for line in lines:
            line = line.strip()
            if line and (not cleaned_lines or line != cleaned_lines[-1]):
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines[:10])  # Limit to 10 lines for conciseness

    def _fallback_financial_advice(self, prompt: str, user_type: str) -> str:
        """Provide fallback advice when Granite is unavailable"""
        advice_templates = {
            "budget": f"Creating a budget is essential for financial health. {'As a student, start with tracking basic expenses like textbooks, food, and entertainment. Many banks offer free budgeting tools.' if user_type == 'student' else 'Consider using the 50/30/20 rule: 50% for needs, 30% for wants, 20% for savings and debt repayment.'}",
            
            "savings": f"Building an emergency fund is your first priority. {'Even saving $25-50 per month as a student builds excellent habits and provides a safety net.' if user_type == 'student' else 'Aim to save 3-6 months of expenses in a high-yield savings account before focusing on investments.'}",
            
            "investment": f"Investing helps build long-term wealth through compound growth. {'Start with low-cost index funds once you have steady income and an emergency fund.' if user_type == 'student' else 'Consider a diversified portfolio with domestic and international stock index funds, plus some bonds based on your risk tolerance.'}",
            
            "debt": f"Managing debt strategically is crucial for financial freedom. {'Focus on paying off high-interest debt like credit cards first, while making minimum payments on student loans.' if user_type == 'student' else 'Use the debt avalanche method (highest interest first) or debt snowball method (smallest balance first) - choose what motivates you most.'}",
            
            "retirement": f"Starting early with retirement planning gives you a huge advantage. {'Even small contributions to a Roth IRA in your 20s can grow to hundreds of thousands by retirement.' if user_type in ['student', 'young_adult'] else 'Maximize employer 401(k) matching - it is free money. Consider increasing contributions by 1% each year.'}"
        }
        
        # Enhanced keyword matching
        prompt_lower = prompt.lower()
        for topic, advice in advice_templates.items():
            if any(keyword in prompt_lower for keyword in [topic, topic + 'ing']):
                return advice
        
        # General advice based on user type
        if user_type == "student":
            return "Great question! As a student, focus on building good financial habits: track spending, take advantage of student discounts, start building credit with a student card (pay it off monthly), and save even small amounts regularly."
        elif user_type == "professional":
            return "Excellent question! Key priorities should be: maximize employer benefits (especially 401k matching), build an emergency fund, optimize your tax situation, and create a diversified investment strategy aligned with your timeline and risk tolerance."
        
        return "That's a smart financial question! The key is to start with the basics: create a budget, build an emergency fund, and then focus on your specific goals like debt payoff or investing. Every small step counts toward financial security."

    def delete_session(self):
        """Delete session (compatibility method - no action needed for local model)"""
        pass

    def get_response(self, user_input: str, user_type: str = "general") -> str:
        """
        Get response using Granite model (main interface method)
        """
        # For Granite, we primarily use the generative model
        return self.generate_financial_advice(user_input, user_type)

    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model"""
        return {
            "model_name": "IBM Granite 3.3 2B Base",
            "model_path": self.model_path,
            "device": self.device,
            "initialized": self.initialized,
            "capabilities": [
                "Financial advice generation",
                "Personalized responses by user type", 
                "Local inference (no API calls)",
                "Privacy-focused processing"
            ]
        }