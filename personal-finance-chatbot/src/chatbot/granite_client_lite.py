# -*- coding: utf-8 -*-
import os
from typing import Dict, Any, Optional

class GraniteClientLite:
    """
    Lightweight version of Granite client that uses rule-based responses
    until the full model is available. Provides the same interface as GraniteClient.
    """
    
    def __init__(self):
        self.model_path = "ibm-granite/granite-3.3-2b-base"
        self.device = "cpu"  # Fallback mode
        self.model = None
        self.tokenizer = None
        self.max_length = 2048
        self.initialized = False  # Always False for lite version
        
        print("🔧 Granite Lite Mode: Using enhanced rule-based responses")
        print("💡 For AI-powered responses, ensure the full Granite model is downloaded")

    def create_session(self) -> Optional[str]:
        """Create a session (compatibility method)"""
        return "granite_lite_session"

    def send_message_to_assistant(self, message: str) -> Dict[str, Any]:
        """Send message (compatibility method)"""
        return {
            "output": {
                "generic": [{
                    "response_type": "text",
                    "text": "Message received by Granite Lite client."
                }]
            }
        }

    def generate_financial_advice(self, prompt: str, user_type: str = "general") -> str:
        """Generate personalized financial advice using dynamic analysis"""
        # This method is kept for backward compatibility but should use get_response with context
        return f"Please use the chat interface for personalized advice based on your profile data. Your question: '{prompt}' requires your financial information for accurate guidance."


    
    def _generate_dynamic_response(self, prompt: str, user_type: str, income: int, balance: int, spending: int, age: int) -> str:
        """Analyze input and generate specific response"""
        # Parse the question to understand intent and context
        question_analysis = self._analyze_question_intent(prompt)
        
        # Generate response based on analysis
        return self._create_contextual_response(prompt, question_analysis, user_type, income, balance, spending, age)
    

    

    
    def _analyze_question_intent(self, prompt: str) -> dict:
        """Analyze user question to understand intent and extract key information"""
        prompt_lower = prompt.lower()
        words = prompt_lower.split()
        
        analysis = {
            'question_type': 'general',
            'topic': 'general',
            'specific_amount': None,
            'time_frame': None,
            'action_needed': False
        }
        
        # Detect question type
        if any(q in prompt_lower for q in ['how much', 'how many']):
            analysis['question_type'] = 'quantity'
        elif any(q in prompt_lower for q in ['should i', 'can i', 'is it good']):
            analysis['question_type'] = 'decision'
        elif any(q in prompt_lower for q in ['what', 'which']):
            analysis['question_type'] = 'options'
        elif any(q in prompt_lower for q in ['when', 'timing']):
            analysis['question_type'] = 'timing'
        elif any(q in prompt_lower for q in ['why', 'reason']):
            analysis['question_type'] = 'explanation'
        elif any(q in prompt_lower for q in ['how to', 'how can']):
            analysis['question_type'] = 'method'
        
        # Detect financial topic
        if any(t in prompt_lower for t in ['save', 'saving', 'savings']):
            analysis['topic'] = 'savings'
        elif any(t in prompt_lower for t in ['invest', 'investment', 'mutual fund', 'sip', 'stocks']):
            analysis['topic'] = 'investment'
        elif any(t in prompt_lower for t in ['budget', 'budgeting', 'expense', 'spending']):
            analysis['topic'] = 'budget'
        elif any(t in prompt_lower for t in ['debt', 'loan', 'emi', 'credit']):
            analysis['topic'] = 'debt'
        elif any(t in prompt_lower for t in ['emergency', 'emergency fund']):
            analysis['topic'] = 'emergency'
        elif any(t in prompt_lower for t in ['insurance', 'health insurance', 'term insurance']):
            analysis['topic'] = 'insurance'
        
        # Extract specific amounts if mentioned
        import re
        amounts = re.findall(r'[₹]?\s*(\d+(?:,\d+)*(?:\.\d+)?)', prompt)
        if amounts:
            analysis['specific_amount'] = int(amounts[0].replace(',', ''))
        
        # Detect time frames
        if any(t in prompt_lower for t in ['month', 'monthly']):
            analysis['time_frame'] = 'monthly'
        elif any(t in prompt_lower for t in ['year', 'yearly', 'annual']):
            analysis['time_frame'] = 'yearly'
        elif any(t in prompt_lower for t in ['week', 'weekly']):
            analysis['time_frame'] = 'weekly'
        
        return analysis
    
    def _create_contextual_response(self, prompt: str, analysis: dict, user_type: str, income: int, balance: int, spending: int, age: int) -> str:
        """Create specific response based on question analysis"""
        topic = analysis['topic']
        q_type = analysis['question_type']
        amount = analysis['specific_amount']
        
        # Generate topic-specific response based on question type
        if topic == 'savings':
            return self._handle_savings_question(prompt, q_type, amount, income, spending, user_type)
        elif topic == 'investment':
            return self._handle_investment_question(prompt, q_type, amount, balance, income, age, user_type)
        elif topic == 'budget':
            return self._handle_budget_question(prompt, q_type, income, spending, user_type)
        elif topic == 'debt':
            return self._handle_debt_question(prompt, q_type, amount, income, user_type)
        elif topic == 'emergency':
            return self._handle_emergency_question(prompt, q_type, spending, income, user_type)
        else:
            return self._handle_general_question(prompt, q_type, income, balance, spending, user_type)
    
    def _handle_savings_question(self, prompt: str, q_type: str, amount: int, income: int, spending: int, user_type: str) -> str:
        """Handle savings-related questions"""
        if income <= 0:
            return "Please update your income in your profile to get personalized savings advice. Generally, aim to save 20% of your income."
        
        current_surplus = income - spending if spending > 0 else income * 0.8
        recommended_savings = max(income * 0.2, current_surplus * 0.5)
        
        if q_type == 'quantity':
            return f"Based on your ₹{income:,} monthly income and ₹{spending:,} expenses, you should save ₹{int(recommended_savings):,}/month. This represents {recommended_savings/income*100:.0f}% of your income."
        elif q_type == 'decision' and amount:
            percentage = (amount / income) * 100
            return f"Saving ₹{amount:,} from your ₹{income:,} income ({percentage:.1f}%) is {'excellent' if percentage >= 20 else 'good' if percentage >= 10 else 'a start'}. {'Keep it up!' if percentage >= 20 else f'Try to reach ₹{int(income*0.2):,}/month (20% target).'}"
        elif q_type == 'method':
            return f"With your current finances (₹{income:,} income, ₹{spending:,} expenses): 1) Automate ₹{int(recommended_savings):,}/month transfer 2) Review your ₹{spending:,} monthly expenses for cuts 3) Use high-yield savings account 4) Track spending weekly 5) Set up separate goal-based accounts."
        return f"Focus on saving ₹{int(recommended_savings):,}/month from your ₹{income:,} income. Start with ₹{int(recommended_savings//2):,} if needed."
    
    def _handle_investment_question(self, prompt: str, q_type: str, amount: int, balance: int, income: int, age: int, user_type: str) -> str:
        """Handle investment-related questions"""
        if income <= 0:
            return "Please update your income in your profile to get personalized investment advice."
        
        emergency_needed = income * 6
        investment_capacity = max(income * 0.15, (income - (income * 0.5) - (income * 0.2)))
        
        if q_type == 'decision' and amount:
            if balance >= emergency_needed:
                risk_percentage = min(100 - age, 80)
                return f"Yes, invest ₹{amount:,}. With ₹{balance:,} emergency fund (target: ₹{emergency_needed:,}) and age {age}, allocate {risk_percentage}% equity, {100-risk_percentage}% debt. Your monthly investment capacity is ₹{int(investment_capacity):,}."
            else:
                shortfall = emergency_needed - balance
                return f"Build emergency fund first. You need ₹{shortfall:,} more (current: ₹{balance:,}, target: ₹{emergency_needed:,}), then invest ₹{amount:,}."
        elif q_type == 'options':
            return f"Based on your ₹{income:,} income and age {age}: 1) Index funds: ₹{int(investment_capacity*0.4):,}/month 2) Large cap funds: ₹{int(investment_capacity*0.3):,}/month 3) ELSS funds: ₹{int(investment_capacity*0.2):,}/month 4) Debt funds: ₹{int(investment_capacity*0.1):,}/month."
        elif q_type == 'quantity':
            return f"Invest ₹{int(investment_capacity):,}/month through SIP from your ₹{income:,} income. This is {investment_capacity/income*100:.0f}% allocation for wealth building."
        return f"At age {age} with ₹{income:,} income, start SIP of ₹{int(investment_capacity):,}/month in diversified equity funds."
    
    def _handle_budget_question(self, prompt: str, q_type: str, income: int, spending: int, user_type: str) -> str:
        """Handle budget-related questions"""
        if income <= 0:
            return "Please update your income in your profile to get personalized budget advice."
        
        if q_type == 'method':
            return f"Personalized budget for ₹{income:,} income: Housing ₹{int(income*0.3):,} (30%), Food ₹{int(income*0.15):,} (15%), Transport ₹{int(income*0.1):,} (10%), Savings ₹{int(income*0.2):,} (20%), Others ₹{int(income*0.25):,} (25%). Current spending: ₹{spending:,}."
        elif spending > 0:
            surplus = income - spending
            spending_ratio = (spending / income) * 100
            return f"Your actual budget: ₹{income:,} income - ₹{spending:,} expenses ({spending_ratio:.0f}% of income) = ₹{surplus:,} surplus. {'Excellent financial discipline!' if surplus > income*0.2 else 'Good surplus for investing!' if surplus > 0 else f'Overspending by ₹{abs(surplus):,}. Reduce expenses in non-essential categories.'}"
        else:
            return f"With ₹{income:,} monthly income, target: Housing ₹{int(income*0.3):,}, Food ₹{int(income*0.15):,}, Transport ₹{int(income*0.1):,}, Savings ₹{int(income*0.2):,}. Track your actual spending first."
    
    def _handle_debt_question(self, prompt: str, q_type: str, amount: int, income: int, user_type: str) -> str:
        """Handle debt-related questions"""
        if income <= 0:
            return "Please update your income in your profile to get personalized debt payoff advice."
        
        max_debt_payment = income * 0.3  # 30% of income for debt
        
        if q_type == 'method':
            return f"With ₹{income:,} income, allocate up to ₹{int(max_debt_payment):,}/month for debt: 1) List all debts with rates 2) Pay minimums on all 3) Extra ₹{int(max_debt_payment*0.7):,} on highest rate debt 4) Avoid new debt 5) Track progress monthly."
        elif amount and income > 0:
            optimal_payment = min(amount // 12, max_debt_payment)
            months_to_clear = amount // optimal_payment if optimal_payment > 0 else 999
            return f"To pay off ₹{amount:,} debt with ₹{income:,} income: Pay ₹{int(optimal_payment):,}/month ({optimal_payment/income*100:.0f}% of income). Debt-free in {months_to_clear:.0f} months. Interest saved: significant!"
        return f"With ₹{income:,} income, dedicate ₹{int(max_debt_payment):,}/month to debt elimination. Prioritize credit cards (20%+ interest) first."
    
    def _handle_emergency_question(self, prompt: str, q_type: str, spending: int, income: int, user_type: str) -> str:
        """Handle emergency fund questions"""
        if income <= 0:
            return "Please update your income and expenses in your profile to get personalized emergency fund advice."
        
        target = spending * 6 if spending > 0 else income * 3  # 6 months expenses or 3 months income
        monthly_save = min(target // 12, income * 0.1)  # Save over 12 months or 10% of income
        
        if q_type == 'quantity':
            return f"Emergency fund target: ₹{target:,} (6 months of your ₹{spending:,} expenses). Save ₹{int(monthly_save):,}/month from ₹{income:,} income to build it in {target//monthly_save:.0f} months."
        elif q_type == 'method':
            return f"Build ₹{target:,} emergency fund: 1) Current expenses: ₹{spending:,}/month 2) High-yield savings (6-7% interest) 3) Automate ₹{int(monthly_save):,}/month from ₹{income:,} income 4) Separate from investments 5) Only for job loss, medical emergencies."
        return f"Your emergency target: ₹{target:,} based on ₹{spending:,} monthly expenses. Save ₹{int(monthly_save):,}/month from your ₹{income:,} income."
    
    def _handle_general_question(self, prompt: str, q_type: str, income: int, balance: int, spending: int, user_type: str) -> str:
        """Handle general financial questions"""
        if income > 0:
            emergency_target = spending * 6 if spending > 0 else income * 3
            surplus = income - spending if spending > 0 else income * 0.8
            return f"Your financial snapshot: Income ₹{income:,}, Expenses ₹{spending:,}, Balance ₹{balance:,}. Priorities: 1) Emergency fund: ₹{emergency_target:,} (current gap: ₹{max(0, emergency_target-balance):,}) 2) Monthly savings: ₹{int(surplus*0.6):,} 3) Investment SIP: ₹{int(surplus*0.4):,} 4) Review monthly. What specific area needs attention?"
        return "Please update your financial profile (income, expenses, balance) to get personalized advice. Start with: 1) Track all expenses 2) Set realistic budget 3) Build emergency fund 4) Begin investing."
    
    def _enhanced_financial_advice(self, prompt: str, user_type: str) -> str:
        """Fallback for unmatched questions"""
        return f"I understand you're asking about '{prompt}'. Let me provide relevant financial guidance based on your profile as a {user_type}. Could you be more specific about what aspect of personal finance you'd like help with?"

    def delete_session(self):
        """Delete session (compatibility method)"""
        pass

    def get_response(self, user_input: str, user_context: Dict[str, Any] = None) -> str:
        """Get response using enhanced rules with user context"""
        if user_context is None:
            user_context = {}
        
        # Extract user data from context
        user_type = user_context.get('user_type', 'general')
        occupation = user_context.get('occupation', '').lower()
        age = user_context.get('age', 25)
        income = user_context.get('income', 0)
        balance = user_context.get('current_balance', 0)
        spending = user_context.get('monthly_spending', 0)
        
        # Determine user type if not provided
        if user_type == 'general':
            if occupation == 'student' or age < 25:
                user_type = 'student'
            elif occupation in ['professional', 'self-employed'] or age >= 25:
                user_type = 'professional'
        
        # Generate direct response based on user input and context
        return self._generate_dynamic_response(user_input, user_type, income, balance, spending, age)

    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the lite client"""
        return {
            "model_name": "Granite Lite (Enhanced Rule-Based)",
            "model_path": self.model_path,
            "device": self.device,
            "initialized": self.initialized,
            "capabilities": [
                "Rule-based financial advice",
                "Personalized responses by user type", 
                "Instant responses (no download required)",
                "Privacy-focused processing",
                "Educational content delivery"
            ]
        }