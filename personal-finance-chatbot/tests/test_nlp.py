"""
Unit tests for NLP Processor
Tests intent recognition, entity extraction, and confidence scoring
"""

import pytest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from chatbot.nlp import NLPProcessor


class TestNLPProcessor:
    """Test NLP processing functionality"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.nlp_processor = NLPProcessor()
    
    def test_intent_recognition_budget(self):
        """Test budget intent recognition with various phrasings"""
        budget_queries = [
            "I need help with my budget",
            "How should I manage my monthly expenses?",
            "Can you help me create a spending plan?",
            "I want to track my expenses better",
            "Help me organize my monthly finances",
            "I need a budget breakdown",
            "How can I plan my monthly spending?",
            "I need expense management advice"
        ]
        
        for query in budget_queries:
            result = self.nlp_processor.process_input(query)
            assert result['intent'] == 'budget', f"Failed to recognize budget intent in: {query}"
            assert result['confidence'] > 0.3, f"Low confidence for budget query: {query}"
    
    def test_intent_recognition_savings(self):
        """Test savings intent recognition"""
        savings_queries = [
            "How can I save more money?",
            "What's the best way to build an emergency fund?",
            "I want to start saving for retirement",
            "Help me increase my savings rate",
            "I need advice on saving strategies",
            "How much should I save each month?",
            "What are good ways to put money aside?",
            "I want to build up my savings account"
        ]
        
        for query in savings_queries:
            result = self.nlp_processor.process_input(query)
            assert result['intent'] == 'savings', f"Failed to recognize savings intent in: {query}"
            assert result['confidence'] > 0.3
    
    def test_intent_recognition_investment(self):
        """Test investment intent recognition"""
        investment_queries = [
            "Should I invest in stocks?",
            "What's a good investment strategy?",
            "Tell me about mutual funds",
            "I want to start investing",
            "What are the best investment options?",
            "How should I diversify my portfolio?",
            "I'm interested in ETFs",
            "Should I invest in bonds or stocks?"
        ]
        
        for query in investment_queries:
            result = self.nlp_processor.process_input(query)
            assert result['intent'] == 'investment', f"Failed to recognize investment intent in: {query}"
            assert result['confidence'] > 0.3
    
    def test_intent_recognition_debt(self):
        """Test debt management intent recognition"""
        debt_queries = [
            "How can I pay off my credit card debt?",
            "What's the best strategy for student loans?",
            "I'm struggling with debt payments",
            "Help me get out of debt",
            "I need a debt consolidation plan",
            "How can I reduce my monthly debt payments?",
            "What's the snowball method for debt?",
            "I have too much credit card debt"
        ]
        
        for query in debt_queries:
            result = self.nlp_processor.process_input(query)
            assert result['intent'] == 'debt', f"Failed to recognize debt intent in: {query}"
            assert result['confidence'] > 0.3
    
    def test_intent_recognition_retirement(self):
        """Test retirement planning intent recognition"""
        retirement_queries = [
            "How much should I save for retirement?",
            "I need help with retirement planning",
            "What's a 401k and how does it work?",
            "Should I contribute to an IRA?",
            "I want to plan for my retirement",
            "How can I maximize my retirement savings?",
            "What are good retirement investment options?",
            "I'm thinking about early retirement"
        ]
        
        for query in retirement_queries:
            result = self.nlp_processor.process_input(query)
            assert result['intent'] == 'retirement', f"Failed to recognize retirement intent in: {query}"
            assert result['confidence'] > 0.3
    
    def test_intent_recognition_taxes(self):
        """Test tax-related intent recognition"""
        tax_queries = [
            "How can I reduce my tax burden?",
            "What tax deductions am I eligible for?",
            "I need help with tax planning",
            "Should I itemize or take standard deduction?",
            "How do I maximize my tax refund?",
            "What are tax-advantaged accounts?",
            "I need advice on tax-efficient investing",
            "How do taxes affect my retirement savings?"
        ]
        
        for query in tax_queries:
            result = self.nlp_processor.process_input(query)
            assert result['intent'] == 'taxes', f"Failed to recognize tax intent in: {query}"
            assert result['confidence'] > 0.3
    
    def test_intent_recognition_insurance(self):
        """Test insurance intent recognition"""
        insurance_queries = [
            "What type of life insurance do I need?",
            "Should I get disability insurance?",
            "How much car insurance coverage should I have?",
            "I need help choosing health insurance",
            "What's the difference between term and whole life insurance?",
            "Do I need umbrella insurance?",
            "How can I save money on insurance premiums?",
            "What insurance do I need as a young adult?"
        ]
        
        for query in insurance_queries:
            result = self.nlp_processor.process_input(query)
            assert result['intent'] == 'insurance', f"Failed to recognize insurance intent in: {query}"
            assert result['confidence'] > 0.3
    
    def test_intent_recognition_credit(self):
        """Test credit-related intent recognition"""
        credit_queries = [
            "How can I improve my credit score?",
            "What affects my credit rating?",
            "I need help building credit history",
            "Should I get a credit card?",
            "How do I check my credit report?",
            "What's a good credit utilization ratio?",
            "How long does it take to build good credit?",
            "I have bad credit, what can I do?"
        ]
        
        for query in credit_queries:
            result = self.nlp_processor.process_input(query)
            assert result['intent'] == 'credit', f"Failed to recognize credit intent in: {query}"
            assert result['confidence'] > 0.3
    
    def test_intent_recognition_income(self):
        """Test income-related intent recognition"""
        income_queries = [
            "How can I increase my income?",
            "Should I ask for a raise?",
            "What are good side hustles?",
            "I want to make more money",
            "How can I negotiate my salary?",
            "What skills should I develop to earn more?",
            "Should I look for a higher paying job?",
            "How can I create passive income streams?"
        ]
        
        for query in income_queries:
            result = self.nlp_processor.process_input(query)
            assert result['intent'] == 'income', f"Failed to recognize income intent in: {query}"
            assert result['confidence'] > 0.3
    
    def test_entity_extraction_amounts(self):
        """Test extraction of monetary amounts"""
        test_cases = [
            ("I make $5000 per month", ["$5000"]),
            ("I earn 75000 dollars annually", ["75000"]),
            ("My rent is $1,200", ["$1,200"]),
            ("I have $50K in savings", ["$50K"]),
            ("I need to save 10000 for a house", ["10000"]),
            ("My car payment is $350 monthly", ["$350"]),
        ]
        
        for query, expected_amounts in test_cases:
            result = self.nlp_processor.process_input(query)
            entities = result.get('entities', {})
            
            if 'amount' in entities:
                found_amounts = entities['amount']
                for expected in expected_amounts:
                    assert expected in found_amounts, f"Expected amount {expected} not found in {found_amounts}"
    
    def test_entity_extraction_percentages(self):
        """Test extraction of percentages"""
        test_cases = [
            ("I have a 15% interest rate", ["15%"]),
            ("My savings rate is 20 percent", ["20"]),
            ("I want to save 10% of my income", ["10%"]),
            ("The APR is 4.5%", ["4.5%"]),
            ("I need 25% for a down payment", ["25%"]),
        ]
        
        for query, expected_percentages in test_cases:
            result = self.nlp_processor.process_input(query)
            entities = result.get('entities', {})
            
            if 'percentage' in entities:
                found_percentages = entities['percentage']
                for expected in expected_percentages:
                    assert any(expected in found for found in found_percentages), \
                        f"Expected percentage {expected} not found in {found_percentages}"
    
    def test_entity_extraction_time_periods(self):
        """Test extraction of time periods"""
        test_cases = [
            ("I need to save for 5 years", ["5 years"]),
            ("My loan term is 30 years", ["30 years"]),
            ("I'll retire in 20 years", ["20 years"]),
            ("I want to pay this off in 2 years", ["2 years"]),
            ("The CD is for 18 months", ["18 months"]),
        ]
        
        for query, expected_periods in test_cases:
            result = self.nlp_processor.process_input(query)
            entities = result.get('entities', {})
            
            if 'time_period' in entities:
                found_periods = entities['time_period']
                for expected in expected_periods:
                    assert expected in found_periods, f"Expected time period {expected} not found in {found_periods}"
    
    def test_entity_extraction_ages(self):
        """Test extraction of ages"""
        test_cases = [
            ("I'm 25 years old", ["25"]),
            ("My age is 35", ["35"]),
            ("I am 42 and want to retire", ["42"]),
            ("At age 30, should I invest?", ["30"]),
        ]
        
        for query, expected_ages in test_cases:
            result = self.nlp_processor.process_input(query)
            entities = result.get('entities', {})
            
            if 'age' in entities:
                found_ages = entities['age']
                for expected in expected_ages:
                    assert expected in found_ages, f"Expected age {expected} not found in {found_ages}"
    
    def test_entity_extraction_professions(self):
        """Test extraction of professions"""
        test_cases = [
            ("I'm a teacher and need financial advice", ["teacher"]),
            ("As a doctor, what should I invest in?", ["doctor"]),
            ("I work as an engineer", ["engineer"]),
            ("I'm a student looking for budget help", ["student"]),
            ("As a nurse, how much should I save?", ["nurse"]),
        ]
        
        for query, expected_professions in test_cases:
            result = self.nlp_processor.process_input(query)
            entities = result.get('entities', {})
            
            if 'profession' in entities:
                found_professions = entities['profession']
                for expected in expected_professions:
                    assert expected in found_professions, f"Expected profession {expected} not found in {found_professions}"
    
    def test_confidence_scoring(self):
        """Test confidence scoring for different query types"""
        # High confidence queries (exact keyword matches)
        high_confidence_queries = [
            "I need budget help",
            "How can I save money?",
            "Should I invest in stocks?",
            "Help me pay off debt"
        ]
        
        for query in high_confidence_queries:
            result = self.nlp_processor.process_input(query)
            assert result['confidence'] > 0.7, f"Expected high confidence for: {query}"
        
        # Medium confidence queries (related terms)
        medium_confidence_queries = [
            "I need financial advice",
            "Help me with money management",
            "What should I do with my paycheck?",
            "I'm worried about my finances"
        ]
        
        for query in medium_confidence_queries:
            result = self.nlp_processor.process_input(query)
            assert 0.3 <= result['confidence'] <= 0.8, f"Expected medium confidence for: {query}"
        
        # Low confidence queries (ambiguous or off-topic)
        low_confidence_queries = [
            "What's the weather like?",
            "How are you doing today?",
            "Tell me a joke",
            "What time is it?"
        ]
        
        for query in low_confidence_queries:
            result = self.nlp_processor.process_input(query)
            assert result['confidence'] < 0.5, f"Expected low confidence for: {query}"
    
    def test_edge_cases(self):
        """Test edge cases and error handling"""
        edge_cases = [
            "",  # Empty string
            "   ",  # Whitespace only
            "a",  # Single character
            "?",  # Single punctuation
            "123",  # Numbers only
            "!!!",  # Punctuation only
        ]
        
        for query in edge_cases:
            result = self.nlp_processor.process_input(query)
            
            # Should not crash and should return valid structure
            assert 'intent' in result
            assert 'confidence' in result
            assert 'entities' in result
            assert isinstance(result['confidence'], (int, float))
            assert 0 <= result['confidence'] <= 1
    
    def test_long_query_handling(self):
        """Test handling of very long queries"""
        long_query = """
        I am a 25-year-old professional working as a software engineer making $75,000 per year.
        I currently have $10,000 in savings and $25,000 in student loan debt with a 6% interest rate.
        I live in an apartment that costs $1,200 per month in rent and I spend about $500 per month on food.
        My car payment is $300 per month and I have $2,000 in credit card debt at 18% APR.
        I want to know if I should focus on paying off my debt first or if I should start investing in a 401k.
        My employer offers a 401k match of up to 4% of my salary. I'm also wondering about building an emergency fund
        and whether I should consider buying a house in the next few years. What would you recommend for my situation?
        """
        
        result = self.nlp_processor.process_input(long_query)
        
        # Should handle long text without issues
        assert 'intent' in result
        assert 'confidence' in result
        assert 'entities' in result
        
        # Should extract multiple entities from the detailed information
        entities = result['entities']
        if entities:
            # Should find monetary amounts
            if 'amount' in entities:
                amounts = entities['amount']
                expected_amounts = ['$75,000', '$10,000', '$25,000', '$1,200', '$500', '$300', '$2,000']
                found_count = sum(1 for expected in expected_amounts if any(expected in amount for amount in amounts))
                assert found_count > 0, "Should extract some monetary amounts from long query"
            
            # Should find percentages
            if 'percentage' in entities:
                percentages = entities['percentage']
                assert any('6%' in p or '6' in p for p in percentages) or any('18%' in p or '18' in p for p in percentages), \
                    "Should extract interest rate percentages"
    
    def test_multiple_intents_in_query(self):
        """Test queries that might match multiple intents"""
        multi_intent_queries = [
            "Should I pay off debt or invest in stocks?",  # debt + investment
            "I need help budgeting and saving money",      # budget + savings  
            "How can I save for retirement while paying off student loans?",  # retirement + debt + savings
            "I want to improve my credit score and start investing",  # credit + investment
        ]
        
        for query in multi_intent_queries:
            result = self.nlp_processor.process_input(query)
            
            # Should still return a primary intent
            assert 'intent' in result
            assert isinstance(result['intent'], str)
            assert len(result['intent']) > 0
            
            # Confidence might be lower due to multiple intents
            assert 'confidence' in result
            assert result['confidence'] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])