import json
import os
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime


class DemographicsManager:
    """
    Enhanced Demographics Manager for user profiling and personalized communication
    """
    
    def __init__(self):
        self.user_profiles = {}
        self.communication_styles = self._initialize_communication_styles()
        self.user_classifications = self._initialize_user_classifications()
        
    def _initialize_communication_styles(self) -> Dict[str, Dict[str, Any]]:
        """Initialize communication styles for different user types"""
        return {
            'student': {
                'greeting': "Hey!",
                'tone': 'casual',
                'complexity': 'simple',
                'examples': True,
                'encouragement': 'high',
                'jargon_level': 'low',
                'explanation_depth': 'moderate'
            },
            'professional': {
                'greeting': "Hello",
                'tone': 'professional',
                'complexity': 'detailed',
                'examples': True,
                'encouragement': 'moderate',
                'jargon_level': 'high',
                'explanation_depth': 'comprehensive'
            },
            'young_adult': {
                'greeting': "Hi there!",
                'tone': 'friendly',
                'complexity': 'balanced',
                'examples': True,
                'encouragement': 'high',
                'jargon_level': 'moderate',
                'explanation_depth': 'practical'
            },
            'senior': {
                'greeting': "Good day",
                'tone': 'respectful',
                'complexity': 'clear',
                'examples': True,
                'encouragement': 'supportive',
                'jargon_level': 'low',
                'explanation_depth': 'thorough'
            },
            'general': {
                'greeting': "Hello",
                'tone': 'neutral',
                'complexity': 'balanced',
                'examples': True,
                'encouragement': 'moderate',
                'jargon_level': 'moderate',
                'explanation_depth': 'standard'
            }
        }

    def _initialize_user_classifications(self) -> Dict[str, Dict[str, Any]]:
        """Initialize criteria for user classification"""
        return {
            'student': {
                'age_range': (16, 26),
                'keywords': ['student', 'college', 'university', 'school', 'studying', 'tuition'],
                'income_indicators': ['part-time', 'allowance', 'scholarship', 'student loan'],
                'financial_priorities': ['textbooks', 'tuition', 'dorm', 'cheap food', 'student discount']
            },
            'professional': {
                'age_range': (22, 65),
                'keywords': ['work', 'job', 'career', 'salary', 'professional', 'office', 'company'],
                'income_indicators': ['salary', 'bonus', '401k', 'health insurance', 'benefits'],
                'financial_priorities': ['retirement', 'mortgage', 'investment', 'tax optimization']
            },
            'young_adult': {
                'age_range': (18, 30),
                'keywords': ['first job', 'starting out', 'new graduate', 'entry level'],
                'income_indicators': ['entry level', 'starting salary', 'first paycheck'],
                'financial_priorities': ['emergency fund', 'credit building', 'apartment', 'first car']
            },
            'senior': {
                'age_range': (55, 100),
                'keywords': ['retirement', 'pension', 'retired', 'senior', 'social security'],
                'income_indicators': ['pension', 'social security', 'retirement fund', 'fixed income'],
                'financial_priorities': ['healthcare', 'estate planning', 'conservative investing']
            }
        }

    def add_user_profile(self, user_id: str, demographics: Dict[str, Any]):
        """Add or update user profile with comprehensive demographic information"""
        # Ensure user_id exists in profiles
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = {}
        
        # Update profile with new demographics
        self.user_profiles[user_id].update(demographics)
        
        # Add timestamp for profile updates
        self.user_profiles[user_id]['last_updated'] = datetime.now().isoformat()
        
        # Determine and cache user type
        user_type = self._classify_user(user_id)
        self.user_profiles[user_id]['user_type'] = user_type

    def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user profile by ID"""
        return self.user_profiles.get(user_id, None)

    def _classify_user(self, user_id: str) -> str:
        """Enhanced user classification based on multiple factors"""
        profile = self.get_user_profile(user_id)
        if not profile:
            return 'general'
        
        # Score each classification
        classification_scores = {}
        
        for user_type, criteria in self.user_classifications.items():
            score = 0
            
            # Age-based scoring
            age = profile.get('age')
            if age:
                age_range = criteria['age_range']
                if age_range[0] <= age <= age_range[1]:
                    score += 3
                elif abs(age - age_range[0]) <= 5 or abs(age - age_range[1]) <= 5:
                    score += 1
            
            # Keyword-based scoring from text inputs
            text_data = ' '.join([
                str(profile.get('occupation', '')),
                str(profile.get('description', '')),
                str(profile.get('goals', '')),
                str(profile.get('situation', ''))
            ]).lower()
            
            for keyword in criteria['keywords']:
                if keyword in text_data:
                    score += 2
            
            # Income indicator scoring
            for indicator in criteria['income_indicators']:
                if indicator in text_data:
                    score += 1
            
            # Financial priority scoring
            for priority in criteria['financial_priorities']:
                if priority in text_data:
                    score += 1
            
            classification_scores[user_type] = score
        
        # Return the classification with highest score
        if classification_scores:
            best_match = max(classification_scores, key=classification_scores.get)
            if classification_scores[best_match] > 2:  # Minimum confidence threshold
                return best_match
        
        return 'general'

    def determine_user_type(self, user_id: str) -> str:
        """Get user type with fallback to classification if not cached"""
        profile = self.get_user_profile(user_id)
        if profile and 'user_type' in profile:
            return profile['user_type']
        
        return self._classify_user(user_id)

    def adapt_communication_style(self, user_id: str, message: str, 
                                 context: str = 'general') -> str:
        """Adapt message based on user demographics and context"""
        user_type = self.determine_user_type(user_id)
        style = self.communication_styles.get(user_type, self.communication_styles['general'])
        
        adapted_message = message
        
        # Apply tone and complexity adjustments
        if style['tone'] == 'casual':
            adapted_message = self._make_casual(adapted_message)
        elif style['tone'] == 'professional':
            adapted_message = self._make_professional(adapted_message)
        elif style['tone'] == 'respectful':
            adapted_message = self._make_respectful(adapted_message)
        
        # Adjust complexity
        if style['complexity'] == 'simple':
            adapted_message = self._simplify_language(adapted_message)
        elif style['complexity'] == 'detailed':
            adapted_message = self._add_detail(adapted_message, context)
        
        # Add greeting if it's a conversation starter
        if context == 'greeting':
            greeting = style['greeting']
            adapted_message = f"{greeting} {adapted_message}"
        
        return adapted_message

    def _make_casual(self, message: str) -> str:
        """Make message more casual"""
        # Replace formal phrases with casual alternatives
        replacements = {
            'I recommend': 'I\'d suggest',
            'It is advisable': 'It\'s a good idea',
            'Furthermore': 'Also',
            'Therefore': 'So',
            'In conclusion': 'Bottom line',
            'Nevertheless': 'But',
            'Subsequently': 'Then'
        }
        
        for formal, casual in replacements.items():
            message = message.replace(formal, casual)
        
        return message

    def _make_professional(self, message: str) -> str:
        """Make message more professional"""
        # This could include more sophisticated transformations
        return message

    def _make_respectful(self, message: str) -> str:
        """Make message more respectful for senior users"""
        # Add courtesy terms and avoid slang
        if not message.startswith(('Please', 'I would', 'May I')):
            if 'recommend' in message.lower() or 'suggest' in message.lower():
                message = f"I would respectfully {message.lower()}"
        
        return message

    def _simplify_language(self, message: str) -> str:
        """Simplify language for easier understanding"""
        # Replace complex financial terms with simpler alternatives
        simplifications = {
            'diversification': 'spreading your investments',
            'portfolio': 'investment collection',
            'asset allocation': 'how you split your money',
            'compound interest': 'earning interest on your interest',
            'volatility': 'price changes',
            'liquidity': 'how easily you can access your money'
        }
        
        for complex_term, simple_term in simplifications.items():
            message = message.replace(complex_term, simple_term)
        
        return message

    def _add_detail(self, message: str, context: str) -> str:
        """Add more detail for professional users"""
        # This could add relevant technical details based on context
        return message

    def get_user_preferences(self, user_id: str) -> Dict[str, Any]:
        """Get user preferences for personalized experience"""
        user_type = self.determine_user_type(user_id)
        style = self.communication_styles.get(user_type, self.communication_styles['general'])
        profile = self.get_user_profile(user_id) or {}
        
        return {
            'communication_style': style,
            'user_type': user_type,
            'age': profile.get('age'),
            'experience_level': self._determine_experience_level(user_id),
            'primary_goals': profile.get('goals', []),
            'risk_tolerance': profile.get('risk_tolerance', 'moderate')
        }

    def _determine_experience_level(self, user_id: str) -> str:
        """Determine user's financial experience level"""
        profile = self.get_user_profile(user_id)
        if not profile:
            return 'beginner'
        
        # Simple heuristic based on age and user type
        age = profile.get('age', 25)
        user_type = profile.get('user_type', 'general')
        
        if user_type == 'student' or age < 25:
            return 'beginner'
        elif user_type == 'professional' and age > 35:
            return 'advanced'
        else:
            return 'intermediate'

    def update_user_interaction(self, user_id: str, interaction_data: Dict[str, Any]):
        """Update user profile based on interactions"""
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = {}
        
        # Track interaction patterns
        if 'interactions' not in self.user_profiles[user_id]:
            self.user_profiles[user_id]['interactions'] = []
        
        interaction_data['timestamp'] = datetime.now().isoformat()
        self.user_profiles[user_id]['interactions'].append(interaction_data)
        
        # Limit interaction history
        if len(self.user_profiles[user_id]['interactions']) > 50:
            self.user_profiles[user_id]['interactions'] = \
                self.user_profiles[user_id]['interactions'][-50:]

    def get_personalized_recommendations(self, user_id: str) -> List[str]:
        """Get recommendations based on user profile"""
        user_type = self.determine_user_type(user_id)
        profile = self.get_user_profile(user_id) or {}
        
        recommendations = []
        
        if user_type == 'student':
            recommendations.extend([
                "Start with a simple budget tracking app",
                "Look into student banking accounts with no fees",
                "Consider a secured credit card to build credit history"
            ])
        elif user_type == 'professional':
            recommendations.extend([
                "Maximize your employer's 401(k) matching",
                "Consider increasing your emergency fund to 6 months of expenses",
                "Review your insurance coverage annually"
            ])
        elif user_type == 'young_adult':
            recommendations.extend([
                "Focus on building an emergency fund first",
                "Start investing in low-cost index funds",
                "Consider automating your savings"
            ])
        elif user_type == 'senior':
            recommendations.extend([
                "Review your retirement withdrawal strategy",
                "Consider long-term care insurance",
                "Focus on preserving capital while generating income"
            ])
        
        return recommendations

    def export_user_data(self, user_id: str) -> Dict[str, Any]:
        """Export user data for backup or analysis"""
        profile = self.get_user_profile(user_id)
        if not profile:
            return {}
        
        return {
            'user_id': user_id,
            'profile': profile,
            'export_timestamp': datetime.now().isoformat()
        }

    def import_user_data(self, user_data: Dict[str, Any]):
        """Import user data from backup"""
        if 'user_id' in user_data and 'profile' in user_data:
            user_id = user_data['user_id']
            self.user_profiles[user_id] = user_data['profile']