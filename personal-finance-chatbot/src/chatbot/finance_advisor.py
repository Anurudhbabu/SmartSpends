import os
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any, Optional
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


class FinanceAdvisor:
    """
    Enhanced Finance Advisor with comprehensive budget analysis,
    spending insights, and demographic-aware recommendations.
    """
    
    def __init__(self):
        self.default_savings_goal = float(os.getenv('DEFAULT_SAVINGS_GOAL', 0.20))
        self.emergency_fund_months = int(os.getenv('DEFAULT_EMERGENCY_FUND_MONTHS', 6))
        
        # Standard budget categories and recommended percentages
        self.budget_categories = {
            'housing': {'recommended_pct': 0.30, 'description': 'Rent, mortgage, utilities, property taxes'},
            'food': {'recommended_pct': 0.12, 'description': 'Groceries, dining out, food delivery'},
            'transportation': {'recommended_pct': 0.15, 'description': 'Car payment, gas, insurance, public transport'},
            'utilities': {'recommended_pct': 0.08, 'description': 'Electric, gas, water, internet, phone'},
            'insurance': {'recommended_pct': 0.05, 'description': 'Health, life, disability insurance'},
            'healthcare': {'recommended_pct': 0.05, 'description': 'Medical expenses, prescriptions, dental'},
            'savings': {'recommended_pct': 0.20, 'description': 'Emergency fund, retirement, investments'},
            'entertainment': {'recommended_pct': 0.05, 'description': 'Movies, subscriptions, hobbies, dining'},
            'personal': {'recommended_pct': 0.05, 'description': 'Clothing, personal care, miscellaneous'},
            'debt': {'recommended_pct': 0.10, 'description': 'Credit cards, loans, other debt payments'}
        }
        
        # Financial health metrics
        self.health_metrics = {
            'debt_to_income_ratio': {'excellent': 0.1, 'good': 0.2, 'fair': 0.36, 'poor': float('inf')},
            'savings_rate': {'excellent': 0.20, 'good': 0.15, 'fair': 0.10, 'poor': 0.05},
            'emergency_fund_months': {'excellent': 6, 'good': 4, 'fair': 2, 'poor': 1}
        }

    def generate_comprehensive_budget_summary(self, income: float, expenses: Dict[str, float], 
                                            user_type: str = "general") -> Dict[str, Any]:
        """
        Generate a comprehensive budget summary with analysis and recommendations
        """
        # Handle savings correctly - if 'savings' is in expenses, use it as the actual savings amount
        if 'savings' in expenses:
            savings = expenses['savings']
            # Calculate total expenses excluding savings (since savings isn't really an expense)
            other_expenses = {k: v for k, v in expenses.items() if k != 'savings'}
            total_expenses = sum(other_expenses.values())
        else:
            total_expenses = sum(expenses.values())
            savings = income - total_expenses
        
        # Calculate percentages
        expense_percentages = {category: (amount / income) * 100 
                             for category, amount in expenses.items() if income > 0}
        
        # Analyze budget health
        budget_analysis = self._analyze_budget_health(income, expenses, savings)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(income, expenses, user_type, budget_analysis)
        
        # Create visualizations
        charts = self._create_budget_visualizations(income, expenses, savings)
        
        summary = {
            'overview': {
                'total_income': income,
                'total_expenses': total_expenses,
                'net_savings': savings,
                'savings_rate': (savings / income) * 100 if income > 0 else 0,
                'expense_ratio': (total_expenses / income) * 100 if income > 0 else 0
            },
            'spending_breakdown': expenses,
            'expense_percentages': expense_percentages,
            'budget_analysis': budget_analysis,
            'recommendations': recommendations,
            'charts': charts,
            'financial_health_score': self._calculate_financial_health_score(income, expenses, savings, total_expenses)
        }
        
        return summary

    def _analyze_budget_health(self, income: float, expenses: Dict[str, float], 
                              savings: float) -> Dict[str, Any]:
        """Analyze budget health against recommended guidelines"""
        analysis = {
            'category_analysis': {},
            'overall_health': 'good',
            'areas_for_improvement': [],
            'positive_aspects': []
        }
        
        if income <= 0:
            analysis['overall_health'] = 'critical'
            analysis['areas_for_improvement'].append('No income recorded')
            return analysis
        
        # Analyze each category
        for category, amount in expenses.items():
            category_pct = (amount / income) if income > 0 else 0
            recommended_pct = self.budget_categories.get(category, {}).get('recommended_pct', 0.05)
            
            category_health = 'good'
            if category_pct > recommended_pct * 1.5:
                category_health = 'poor'
                analysis['areas_for_improvement'].append(
                    f"{category.title()} spending is {category_pct:.1%} of income (recommended: {recommended_pct:.1%})"
                )
            elif category_pct > recommended_pct * 1.2:
                category_health = 'fair'
                analysis['areas_for_improvement'].append(
                    f"{category.title()} spending is slightly high at {category_pct:.1%} of income"
                )
            elif category_pct <= recommended_pct:
                analysis['positive_aspects'].append(
                    f"{category.title()} spending is well-controlled at {category_pct:.1%} of income"
                )
            
            analysis['category_analysis'][category] = {
                'current_pct': category_pct,
                'recommended_pct': recommended_pct,
                'health': category_health,
                'overspend_amount': max(0, amount - (income * recommended_pct))
            }
        
        # Overall savings analysis
        savings_rate = (savings / income) if income > 0 else 0
        if savings_rate >= 0.20:
            analysis['positive_aspects'].append("Excellent savings rate - you're saving 20%+ of income")
        elif savings_rate >= 0.15:
            analysis['positive_aspects'].append("Good savings rate - you're saving 15%+ of income")
        elif savings_rate >= 0.10:
            analysis['areas_for_improvement'].append("Consider increasing savings rate to 15-20%")
        else:
            analysis['areas_for_improvement'].append("Low savings rate - aim to save at least 10-15% of income")
            if analysis['overall_health'] == 'good':
                analysis['overall_health'] = 'fair'
        
        return analysis

    def _generate_recommendations(self, income: float, expenses: Dict[str, float], 
                                user_type: str, budget_analysis: Dict[str, Any]) -> List[str]:
        """Generate personalized recommendations based on budget analysis and user type"""
        recommendations = []
        
        # User type specific advice
        if user_type == "student":
            recommendations.extend([
                "Look for student discounts on software, transportation, and entertainment",
                "Consider textbook rental services instead of buying new books",
                "Start building credit with a student credit card (use responsibly)",
                "Take advantage of free campus resources (gym, library, events)"
            ])
        elif user_type == "professional":
            recommendations.extend([
                "Maximize employer 401(k) match if available",
                "Consider tax-advantaged accounts (IRA, HSA)",
                "Review and negotiate insurance policies annually",
                "Automate savings and investments to pay yourself first"
            ])
        elif user_type == "young_adult":
            recommendations.extend([
                "Build an emergency fund covering 3-6 months of expenses",
                "Start investing early to benefit from compound growth",
                "Consider term life insurance if you have dependents",
                "Focus on building good credit for future major purchases"
            ])
        
        # Budget-specific recommendations
        for category, analysis in budget_analysis.get('category_analysis', {}).items():
            if analysis['health'] == 'poor':
                recommendations.extend(self._get_category_reduction_tips(category, analysis['overspend_amount']))
        
        # Savings recommendations
        if income > 0:
            savings_rate = (income - sum(expenses.values())) / income
            if savings_rate < 0.15:
                recommendations.append("Consider the 50/30/20 rule: 50% needs, 30% wants, 20% savings")
                recommendations.append("Track expenses for a month to identify areas to cut spending")
        
        return recommendations

    def _get_category_reduction_tips(self, category: str, overspend_amount: float) -> List[str]:
        """Get specific tips for reducing spending in a category"""
        tips = {
            'food': [
                f"Consider meal planning and cooking at home to save ~${overspend_amount:.0f}/month",
                "Use grocery store apps and coupons for discounts",
                "Try generic brands which can save 20-30% on grocery bills"
            ],
            'entertainment': [
                f"Review subscriptions and cancel unused ones to save ~${overspend_amount:.0f}/month",
                "Look for free local events and activities",
                "Consider sharing streaming services with family/friends"
            ],
            'transportation': [
                f"Consider carpooling or public transit to save ~${overspend_amount:.0f}/month",
                "Shop around for better car insurance rates",
                "Combine errands into single trips to save on gas"
            ],
            'housing': [
                f"Consider downsizing or finding a roommate to save ~${overspend_amount:.0f}/month",
                "Negotiate rent or look for better deals",
                "Improve energy efficiency to reduce utility costs"
            ]
        }
        
        return tips.get(category, [f"Look for ways to reduce {category} expenses by ~${overspend_amount:.0f}/month"])

    def _create_budget_visualizations(self, income: float, expenses: Dict[str, float], 
                                    savings: float) -> Dict[str, str]:
        """Create budget visualization charts"""
        # This would generate actual charts in a real implementation
        # For now, return placeholder descriptions
        return {
            'pie_chart': 'Expense breakdown pie chart',
            'bar_chart': 'Category comparison with recommended percentages',
            'trend_chart': 'Spending trends over time'
        }

    def _calculate_financial_health_score(self, income: float, expenses: Dict[str, float], 
                                        savings: float, actual_expenses: float = None) -> Dict[str, Any]:
        """Calculate overall financial health score"""
        if income <= 0:
            return {'score': 0, 'rating': 'Critical', 'description': 'No income recorded'}
        
        score = 0
        max_score = 100
        
        # Savings rate (30 points)
        savings_rate = savings / income
        if savings_rate >= 0.20:
            score += 30
        elif savings_rate >= 0.15:
            score += 25
        elif savings_rate >= 0.10:
            score += 20
        elif savings_rate >= 0.05:
            score += 15
        
        # Debt-to-income ratio (25 points)
        debt_amount = expenses.get('debt', 0)
        debt_ratio = debt_amount / income
        if debt_ratio <= 0.10:
            score += 25
        elif debt_ratio <= 0.20:
            score += 20
        elif debt_ratio <= 0.36:
            score += 15
        else:
            score += 5
        
        # Expense control (25 points) - use actual expenses if provided, else calculate
        if actual_expenses is not None:
            total_expenses = actual_expenses
        else:
            # Exclude savings from expenses calculation if it exists
            if 'savings' in expenses:
                total_expenses = sum(v for k, v in expenses.items() if k != 'savings')
            else:
                total_expenses = sum(expenses.values())
        
        expense_ratio = total_expenses / income
        if expense_ratio <= 0.75:
            score += 25
        elif expense_ratio <= 0.85:
            score += 20
        elif expense_ratio <= 0.95:
            score += 15
        elif expense_ratio <= 1.0:
            score += 10
        
        # Emergency fund (20 points) - estimated based on savings
        estimated_monthly_expenses = total_expenses
        if savings >= estimated_monthly_expenses * 6:
            score += 20
        elif savings >= estimated_monthly_expenses * 3:
            score += 15
        elif savings >= estimated_monthly_expenses * 1:
            score += 10
        elif savings > 0:
            score += 5
        
        # Determine rating
        if score >= 90:
            rating = 'Excellent'
        elif score >= 80:
            rating = 'Good'
        elif score >= 70:
            rating = 'Fair'
        elif score >= 60:
            rating = 'Poor'
        else:
            rating = 'Critical'
        
        return {
            'score': score,
            'rating': rating,
            'description': f'Your financial health score is {score}/100 ({rating})'
        }

    def _calculate_financial_health_score_from_metrics(self, savings_rate: float, debt_ratio: float, 
                                                      expense_control: float, emergency_fund: float) -> Dict[str, Any]:
        """
        Calculate financial health score from pre-calculated metrics (for testing)
        
        Args:
            savings_rate: Savings rate as percentage (0-100)
            debt_ratio: Debt-to-income ratio as percentage (0-100)  
            expense_control: Expense control score (0-100)
            emergency_fund: Emergency fund in months
        """
        score = 0
        
        # Savings rate (30 points) - convert percentage to decimal
        savings_rate_decimal = savings_rate / 100
        if savings_rate_decimal >= 0.20:
            score += 30
        elif savings_rate_decimal >= 0.15:
            score += 25
        elif savings_rate_decimal >= 0.10:
            score += 20
        elif savings_rate_decimal >= 0.05:
            score += 15
        
        # Debt-to-income ratio (25 points) - convert percentage to decimal
        debt_ratio_decimal = debt_ratio / 100
        if debt_ratio_decimal <= 0.10:
            score += 25
        elif debt_ratio_decimal <= 0.20:
            score += 20
        elif debt_ratio_decimal <= 0.36:
            score += 15
        else:
            score += 5
        
        # Expense control (25 points) - use the score directly scaled to 0-25
        score += min(25, expense_control * 0.25)
        
        # Emergency fund (20 points)
        if emergency_fund >= 6:
            score += 20
        elif emergency_fund >= 3:
            score += 15
        elif emergency_fund >= 1:
            score += 10
        elif emergency_fund > 0:
            score += 5
        
        # Determine rating
        if score >= 90:
            rating = 'Excellent'
        elif score >= 80:
            rating = 'Good'
        elif score >= 70:
            rating = 'Fair'
        elif score >= 60:
            rating = 'Poor'
        else:
            rating = 'Critical'
        
        return {
            'score': int(score),
            'rating': rating,
            'description': f'Your financial health score is {int(score)}/100 ({rating})'
        }

    def get_spending_insights(self, expenses: Dict[str, float], income: float = 0, 
                            user_type: str = "general") -> Dict[str, Any]:
        """Generate actionable spending insights"""
        insights = {
            'summary': [],
            'opportunities': [],
            'warnings': [],
            'trends': [],
            'recommendations': []
        }
        
        if not expenses:
            insights['warnings'].append("No expense data available for analysis")
            return insights
        
        total_expenses = sum(expenses.values())
        
        # Top spending categories
        sorted_expenses = sorted(expenses.items(), key=lambda x: x[1], reverse=True)
        top_category = sorted_expenses[0]
        
        insights['summary'].append(
            f"Your highest expense category is {top_category[0]} at ${top_category[1]:.2f}"
        )
        
        # Category analysis
        for category, amount in expenses.items():
            category_pct = (amount / total_expenses) * 100 if total_expenses > 0 else 0
            
            if category_pct > 30:
                insights['warnings'].append(
                    f"{category.title()} represents {category_pct:.1f}% of your spending - consider if this is sustainable"
                )
            elif category_pct > 20:
                insights['opportunities'].append(
                    f"{category.title()} is a significant expense ({category_pct:.1f}%) - review for potential savings"
                )
        
        # Income-based insights
        if income > 0:
            expense_ratio = (total_expenses / income) * 100
            if expense_ratio > 100:
                insights['warnings'].append("You're spending more than you earn - immediate action needed")
            elif expense_ratio > 90:
                insights['warnings'].append("You're spending over 90% of income - little room for savings")
            elif expense_ratio < 80:
                insights['opportunities'].append("Good expense control - opportunity to increase savings")
        
        # Generate recommendations
        insights['recommendations'] = self._generate_recommendations(
            income, expenses, user_type, {'category_analysis': {}}
        )
        
        return insights

    def create_financial_plan(self, income: float, expenses: Dict[str, float], 
                            goals: Dict[str, Any], user_type: str = "general") -> Dict[str, Any]:
        """Create a comprehensive financial plan"""
        plan = {
            'current_situation': self.generate_comprehensive_budget_summary(income, expenses, user_type),
            'goals': goals,
            'action_items': [],
            'timeline': {},
            'projected_outcomes': {}
        }
        
        # Add goal-specific action items
        for goal_type, goal_data in goals.items():
            if goal_type == 'emergency_fund':
                target_amount = goal_data.get('amount', sum(expenses.values()) * 6)
                current_savings = income - sum(expenses.values())
                months_to_goal = target_amount / max(current_savings, 1) if current_savings > 0 else float('inf')
                
                plan['action_items'].extend([
                    f"Save ${target_amount:.0f} for emergency fund",
                    f"Automatically transfer ${current_savings:.0f}/month to savings",
                    f"Expected timeline: {months_to_goal:.0f} months" if months_to_goal != float('inf') else "Increase income or reduce expenses first"
                ])
        
        return plan