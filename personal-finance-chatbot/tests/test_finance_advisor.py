"""
Unit tests for Finance Advisor
Tests budget analysis, financial health scoring, and recommendation generation
"""

import pytest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from chatbot.finance_advisor import FinanceAdvisor


class TestFinanceAdvisor:
    """Test finance advisor functionality"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.finance_advisor = FinanceAdvisor()
    
    def test_budget_analysis_structure(self):
        """Test that budget analysis returns proper structure"""
        monthly_income = 5000
        expenses = {
            'housing': 1200,
            'utilities': 200,
            'insurance': 300,
            'debt': 400,
            'food': 500,
            'transportation': 400,
            'entertainment': 200,
            'healthcare': 150,
            'personal': 100,
            'savings': 1000
        }
        
        result = self.finance_advisor.generate_comprehensive_budget_summary(
            monthly_income, expenses, 'professional'
        )
        
        # Check main structure
        required_keys = ['overview', 'financial_health_score', 'budget_analysis', 'recommendations']
        for key in required_keys:
            assert key in result, f"Missing key: {key}"
        
        # Check overview structure
        overview = result['overview']
        overview_keys = ['total_income', 'total_expenses', 'net_savings', 'savings_rate']
        for key in overview_keys:
            assert key in overview, f"Missing overview key: {key}"
        
        # Check financial health score structure
        health_score = result['financial_health_score']
        health_keys = ['score', 'rating', 'breakdown']
        for key in health_keys:
            assert key in health_score, f"Missing health score key: {key}"
        
        # Check budget analysis structure
        budget_analysis = result['budget_analysis']
        analysis_keys = ['positive_aspects', 'areas_for_improvement', 'category_breakdown']
        for key in analysis_keys:
            assert key in budget_analysis, f"Missing budget analysis key: {key}"
        
        # Check recommendations
        assert isinstance(result['recommendations'], list)
        assert len(result['recommendations']) > 0
    
    def test_overview_calculations(self):
        """Test budget overview calculations"""
        monthly_income = 4000
        expenses = {
            'housing': 1200,    # 30%
            'utilities': 150,   # 3.75%
            'insurance': 200,   # 5%
            'debt': 300,        # 7.5%
            'food': 400,        # 10%
            'transportation': 250, # 6.25%
            'entertainment': 150,  # 3.75%
            'healthcare': 100,     # 2.5%
            'personal': 80,        # 2%
            'savings': 600         # 15%
        }
        
        total_expected_expenses = sum(expenses.values())
        expected_net_savings = monthly_income - (total_expected_expenses - expenses['savings'])
        expected_savings_rate = (expenses['savings'] / monthly_income) * 100
        
        result = self.finance_advisor.generate_comprehensive_budget_summary(
            monthly_income, expenses, 'professional'
        )
        
        overview = result['overview']
        
        # Test calculations
        assert overview['total_income'] == monthly_income
        assert overview['total_expenses'] == total_expected_expenses - expenses['savings']  # Exclude savings from expenses
        assert abs(overview['net_savings'] - expected_net_savings) < 0.01
        assert abs(overview['savings_rate'] - expected_savings_rate) < 0.01
    
    def test_financial_health_score_excellent(self):
        """Test financial health scoring for excellent finances"""
        monthly_income = 6000
        expenses = {
            'housing': 1200,      # 20% (excellent)
            'utilities': 150,     # 2.5%
            'insurance': 300,     # 5%
            'debt': 300,          # 5% (low debt)
            'food': 450,          # 7.5%
            'transportation': 300, # 5%
            'entertainment': 200,  # 3.3%
            'healthcare': 100,     # 1.7%
            'personal': 100,       # 1.7%
            'savings': 1500       # 25% (excellent)
        }
        
        result = self.finance_advisor.generate_comprehensive_budget_summary(
            monthly_income, expenses, 'professional'
        )
        
        health_score = result['financial_health_score']
        
        # Should have high score
        assert health_score['score'] >= 80
        assert health_score['rating'] in ['Good', 'Excellent']
        
        # Check breakdown
        breakdown = health_score['breakdown']
        assert 'savings_rate_score' in breakdown
        assert 'debt_ratio_score' in breakdown
        assert 'expense_control_score' in breakdown
        assert 'emergency_fund_score' in breakdown
    
    def test_financial_health_score_poor(self):
        """Test financial health scoring for poor finances"""
        monthly_income = 3000
        expenses = {
            'housing': 1500,      # 50% (too high)
            'utilities': 200,     # 6.7%
            'insurance': 150,     # 5%
            'debt': 800,          # 26.7% (too high)
            'food': 350,          # 11.7%
            'transportation': 200, # 6.7%
            'entertainment': 150,  # 5%
            'healthcare': 80,      # 2.7%
            'personal': 70,        # 2.3%
            'savings': 100        # 3.3% (too low)
        }
        
        result = self.finance_advisor.generate_comprehensive_budget_summary(
            monthly_income, expenses, 'young_adult'
        )
        
        health_score = result['financial_health_score']
        
        # Should have low score
        assert health_score['score'] <= 50
        assert health_score['rating'] in ['Poor', 'Needs Improvement']
    
    def test_category_analysis_housing_too_high(self):
        """Test identification of housing costs that are too high"""
        monthly_income = 4000
        expenses = {
            'housing': 2000,      # 50% (way too high)
            'utilities': 150,
            'insurance': 200,
            'debt': 200,
            'food': 300,
            'transportation': 200,
            'entertainment': 100,
            'healthcare': 80,
            'personal': 50,
            'savings': 200
        }
        
        result = self.finance_advisor.generate_comprehensive_budget_summary(
            monthly_income, expenses, 'professional'
        )
        
        budget_analysis = result['budget_analysis']
        
        # Should identify housing as area for improvement
        improvements = ' '.join(budget_analysis['areas_for_improvement']).lower()
        assert 'housing' in improvements or 'rent' in improvements or 'mortgage' in improvements
        
        # Category breakdown should show high percentage for housing
        category_breakdown = budget_analysis['category_breakdown']
        housing_info = next((cat for cat in category_breakdown if 'housing' in cat.lower()), None)
        assert housing_info is not None
        assert '50%' in housing_info
    
    def test_category_analysis_good_savings_rate(self):
        """Test identification of good savings habits"""
        monthly_income = 5000
        expenses = {
            'housing': 1000,      # 20%
            'utilities': 150,
            'insurance': 250,
            'debt': 300,
            'food': 400,
            'transportation': 300,
            'entertainment': 150,
            'healthcare': 100,
            'personal': 80,
            'savings': 1000      # 20% (excellent)
        }
        
        result = self.finance_advisor.generate_comprehensive_budget_summary(
            monthly_income, expenses, 'professional'
        )
        
        budget_analysis = result['budget_analysis']
        
        # Should identify good savings as positive aspect
        positive_aspects = ' '.join(budget_analysis['positive_aspects']).lower()
        assert 'saving' in positive_aspects or '20%' in positive_aspects
    
    def test_recommendations_generation(self):
        """Test that appropriate recommendations are generated"""
        monthly_income = 3500
        expenses = {
            'housing': 1400,      # 40% (high)
            'utilities': 180,     # 5.1%
            'insurance': 200,     # 5.7%
            'debt': 600,          # 17.1% (high)
            'food': 450,          # 12.9% (high)
            'transportation': 250, # 7.1%
            'entertainment': 200,  # 5.7% (could reduce)
            'healthcare': 100,     # 2.9%
            'personal': 120,       # 3.4%
            'savings': 150        # 4.3% (low)
        }
        
        result = self.finance_advisor.generate_comprehensive_budget_summary(
            monthly_income, expenses, 'young_adult'
        )
        
        recommendations = result['recommendations']
        
        # Should have multiple recommendations
        assert len(recommendations) >= 5
        
        # Should address the major issues
        rec_text = ' '.join(recommendations).lower()
        
        # Should mention housing costs
        assert any(word in rec_text for word in ['housing', 'rent', 'mortgage'])
        
        # Should mention debt
        assert any(word in rec_text for word in ['debt', 'payment', 'loan'])
        
        # Should mention savings
        assert any(word in rec_text for word in ['save', 'saving', 'emergency'])
    
    def test_user_type_specific_recommendations(self):
        """Test that recommendations are tailored to user type"""
        monthly_income = 4000
        expenses = {
            'housing': 1200,
            'utilities': 150,
            'insurance': 200,
            'debt': 300,
            'food': 400,
            'transportation': 300,
            'entertainment': 150,
            'healthcare': 100,
            'personal': 80,
            'savings': 800
        }
        
        # Test student recommendations
        student_result = self.finance_advisor.generate_comprehensive_budget_summary(
            monthly_income, expenses, 'student'
        )
        student_rec_text = ' '.join(student_result['recommendations']).lower()
        assert any(word in student_rec_text for word in ['student', 'education', 'textbook', 'discount'])
        
        # Test professional recommendations
        professional_result = self.finance_advisor.generate_comprehensive_budget_summary(
            monthly_income, expenses, 'professional'
        )
        professional_rec_text = ' '.join(professional_result['recommendations']).lower()
        assert any(word in professional_rec_text for word in ['401k', 'career', 'professional', 'investment'])
        
        # Test senior recommendations
        senior_result = self.finance_advisor.generate_comprehensive_budget_summary(
            monthly_income, expenses, 'senior'
        )
        senior_rec_text = ' '.join(senior_result['recommendations']).lower()
        assert any(word in senior_rec_text for word in ['retirement', 'healthcare', 'medicare', 'conservative'])
    
    def test_edge_case_zero_income(self):
        """Test handling of zero income"""
        monthly_income = 0
        expenses = {
            'housing': 800,
            'utilities': 100,
            'insurance': 150,
            'debt': 200,
            'food': 300,
            'transportation': 150,
            'entertainment': 50,
            'healthcare': 50,
            'personal': 30,
            'savings': 0
        }
        
        result = self.finance_advisor.generate_comprehensive_budget_summary(
            monthly_income, expenses, 'general'
        )
        
        # Should handle gracefully without crashing
        assert 'overview' in result
        assert result['overview']['total_income'] == 0
        assert result['overview']['net_savings'] <= 0  # Should be negative
        
        # Should provide appropriate recommendations
        recommendations = result['recommendations']
        rec_text = ' '.join(recommendations).lower()
        assert any(word in rec_text for word in ['income', 'job', 'work', 'earn'])
    
    def test_edge_case_no_expenses(self):
        """Test handling of no expenses (all zeros)"""
        monthly_income = 3000
        expenses = {
            'housing': 0,
            'utilities': 0,
            'insurance': 0,
            'debt': 0,
            'food': 0,
            'transportation': 0,
            'entertainment': 0,
            'healthcare': 0,
            'personal': 0,
            'savings': 0
        }
        
        result = self.finance_advisor.generate_comprehensive_budget_summary(
            monthly_income, expenses, 'general'
        )
        
        # Should handle gracefully
        assert 'overview' in result
        assert result['overview']['total_expenses'] == 0
        assert result['overview']['net_savings'] == monthly_income
        
        # Should recommend creating a budget
        recommendations = result['recommendations']
        rec_text = ' '.join(recommendations).lower()
        assert any(word in rec_text for word in ['budget', 'expense', 'track', 'plan'])
    
    def test_edge_case_very_high_income(self):
        """Test handling of very high income"""
        monthly_income = 50000  # Very high income
        expenses = {
            'housing': 5000,      # 10%
            'utilities': 500,     # 1%
            'insurance': 1000,    # 2%
            'debt': 2000,         # 4%
            'food': 1500,         # 3%
            'transportation': 1000, # 2%
            'entertainment': 2000,  # 4%
            'healthcare': 500,      # 1%
            'personal': 1000,       # 2%
            'savings': 10000       # 20%
        }
        
        result = self.finance_advisor.generate_comprehensive_budget_summary(
            monthly_income, expenses, 'professional'
        )
        
        # Should handle large numbers correctly
        assert result['overview']['total_income'] == 50000
        health_score = result['financial_health_score']
        assert health_score['score'] >= 80  # Should have excellent score
        
        # Recommendations should be appropriate for high earners
        recommendations = result['recommendations']
        rec_text = ' '.join(recommendations).lower()
        assert any(word in rec_text for word in ['investment', 'tax', 'retirement', 'diversi'])
    
    def test_financial_health_score_calculation_components(self):
        """Test individual components of financial health score"""
        # Test savings rate component
        test_cases = [
            (25, 80, 90, 6, 90, 100),  # Excellent all around
            (15, 70, 70, 4, 75, 85),   # Good
            (5, 50, 50, 2, 40, 60),    # Needs improvement
            (2, 20, 30, 0.5, 20, 40),  # Poor
        ]
        
        for savings_rate, debt_ratio, expense_control, emergency_fund, min_score, max_score in test_cases:
            score_result = self.finance_advisor._calculate_financial_health_score(
                savings_rate, debt_ratio, expense_control, emergency_fund
            )
            
            assert min_score <= score_result['score'] <= max_score, \
                f"Score {score_result['score']} not in expected range {min_score}-{max_score}"
            
            # Check that breakdown exists and makes sense
            breakdown = score_result['breakdown']
            assert all(key in breakdown for key in ['savings_rate_score', 'debt_ratio_score', 
                                                   'expense_control_score', 'emergency_fund_score'])
            
            # All scores should be between 0 and 25 (25 points each)
            for component_score in breakdown.values():
                assert 0 <= component_score <= 25


if __name__ == "__main__":
    pytest.main([__file__, "-v"])