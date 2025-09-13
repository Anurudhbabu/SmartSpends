import re
import os
import nltk
from typing import Dict, List, Tuple, Any, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class NLPProcessor:
    """
    Enhanced NLP processor for financial chatbot with advanced intent recognition,
    entity extraction, and context understanding.
    """
    
    def __init__(self):
        self._download_nltk_data()
        self._initialize_financial_intents()
        self._initialize_entity_patterns()
        self.vectorizer = TfidfVectorizer()
        self.intent_vectors = None
        self._train_intent_classifier()

    def _download_nltk_data(self):
        """Download required NLTK data"""
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
        
        try:
            nltk.data.find('taggers/averaged_perceptron_tagger')
        except LookupError:
            nltk.download('averaged_perceptron_tagger')

    def _initialize_financial_intents(self):
        """Initialize comprehensive financial intent categories with training phrases"""
        self.financial_intents = {
            "budget": [
                "help me create a budget", "how to budget", "budget planning", 
                "track expenses", "spending plan", "monthly budget", "budget advice",
                "how much should I spend", "expense tracking", "allocate money"
            ],
            "savings": [
                "how to save money", "savings advice", "save more", "emergency fund",
                "saving goals", "savings account", "how much to save", "building savings",
                "savings plan", "save for future", "increase savings"
            ],
            "investment": [
                "how to invest", "investment advice", "stocks", "bonds", "portfolio",
                "mutual funds", "retirement fund", "investment strategy", "index funds",
                "diversify investments", "long-term investing", "investment options"
            ],
            "debt": [
                "pay off debt", "debt management", "credit card debt", "student loans",
                "debt consolidation", "debt strategy", "eliminate debt", "debt payoff",
                "reduce debt", "debt advice", "loan payments"
            ],
            "taxes": [
                "tax advice", "tax deductions", "tax planning", "tax savings",
                "file taxes", "tax strategies", "tax optimization", "tax preparation",
                "reduce taxes", "tax benefits", "tax credits"
            ],
            "retirement": [
                "retirement planning", "retirement savings", "401k", "IRA", "pension",
                "retire early", "retirement fund", "retirement advice", "retirement goals",
                "save for retirement", "retirement contributions"
            ],
            "insurance": [
                "insurance advice", "health insurance", "life insurance", "auto insurance",
                "insurance coverage", "insurance planning", "insurance needs",
                "insurance comparison", "insurance benefits"
            ],
            "credit": [
                "credit score", "build credit", "improve credit", "credit report",
                "credit card advice", "credit history", "credit repair", "credit utilization",
                "good credit", "credit management"
            ],
            "income": [
                "increase income", "side hustle", "passive income", "salary negotiation",
                "income streams", "earn more money", "financial growth", "income advice",
                "raise income", "multiple income sources"
            ]
        }

    def _initialize_entity_patterns(self):
        """Initialize patterns for extracting financial entities"""
        self.entity_patterns = {
            'amount': [
                r'\$[\d,]+(?:\.\d{2})?',  # $1,000.00
                r'[\d,]+\s*(?:dollars?|bucks?|\$)',  # 1000 dollars
                r'(?:USD|usd)\s*[\d,]+(?:\.\d{2})?',  # USD 1000
                r'[\d,]+(?:\.\d{2})?\s*(?:dollars?|USD|usd|\$)'  # 1000.00 dollars
            ],
            'percentage': [
                r'[\d.]+\s*%',  # 20%
                r'[\d.]+\s*percent',  # 20 percent
                r'[\d.]+\s*per\s*cent'  # 20 per cent
            ],
            'time_period': [
                r'(?:monthly|weekly|yearly|annually|daily)',
                r'per\s+(?:month|week|year|day)',
                r'(?:every|each)\s+(?:month|week|year|day)',
                r'[\d]+\s*(?:months?|weeks?|years?|days?)'
            ],
            'age': [
                r'(?:I\'m|I am|age|aged)\s*[\d]+',
                r'[\d]+\s*(?:years? old|y\.?o\.?)',
                r'born in [\d]{4}'
            ],
            'profession': [
                r'(?:I\'m a|I am a|I work as|profession|job|career)\s*(\w+(?:\s+\w+)*)',
                r'student|professional|worker|employee|self-employed|entrepreneur'
            ]
        }

    def _train_intent_classifier(self):
        """Train a simple TF-IDF based intent classifier"""
        all_training_phrases = []
        self.intent_labels = []
        
        for intent, phrases in self.financial_intents.items():
            for phrase in phrases:
                all_training_phrases.append(phrase.lower())
                self.intent_labels.append(intent)
        
        if all_training_phrases:
            self.intent_vectors = self.vectorizer.fit_transform(all_training_phrases)

    def preprocess_input(self, user_input: str) -> str:
        """Enhanced preprocessing with tokenization and normalization"""
        # Basic preprocessing
        processed = user_input.lower().strip()
        
        # Remove extra whitespace
        processed = re.sub(r'\s+', ' ', processed)
        
        # Normalize common variations
        processed = processed.replace("i'm", "i am")
        processed = processed.replace("can't", "cannot")
        processed = processed.replace("won't", "will not")
        processed = processed.replace("don't", "do not")
        
        return processed

    def recognize_intent(self, processed_input: str) -> Tuple[str, float]:
        """Recognize intent using TF-IDF similarity"""
        if self.intent_vectors is None or self.intent_vectors.shape[0] == 0:
            return self._fallback_intent_recognition(processed_input)
        
        try:
            # Transform input to TF-IDF vector
            input_vector = self.vectorizer.transform([processed_input])
            
            # Calculate similarities
            similarities = cosine_similarity(input_vector, self.intent_vectors)[0]
            
            # Find best match
            best_idx = np.argmax(similarities)
            best_score = similarities[best_idx]
            
            if best_score > 0.1:  # Threshold for confidence
                return self.intent_labels[best_idx], best_score
            
        except Exception as e:
            print(f"Error in intent recognition: {e}")
        
        return self._fallback_intent_recognition(processed_input)

    def _fallback_intent_recognition(self, processed_input: str) -> Tuple[str, float]:
        """Fallback intent recognition using keyword matching"""
        intent_scores = {}
        
        for intent, phrases in self.financial_intents.items():
            score = 0
            for phrase in phrases:
                if phrase.lower() in processed_input:
                    score += 1
                else:
                    # Check for partial matches
                    words = phrase.lower().split()
                    matches = sum(1 for word in words if word in processed_input)
                    if matches > 0:
                        score += matches / len(words) * 0.5
            
            if score > 0:
                intent_scores[intent] = score
        
        if intent_scores:
            best_intent = max(intent_scores, key=intent_scores.get)
            confidence = min(intent_scores[best_intent] / 3.0, 1.0)  # Normalize confidence
            return best_intent, confidence
        
        return "general", 0.1

    def extract_entities(self, processed_input: str) -> Dict[str, Any]:
        """Extract financial entities using regex patterns"""
        entities = {}
        
        for entity_type, patterns in self.entity_patterns.items():
            matches = []
            for pattern in patterns:
                found = re.findall(pattern, processed_input, re.IGNORECASE)
                if found:
                    matches.extend(found)
            
            if matches:
                if entity_type == 'amount':
                    entities[entity_type] = self._parse_amount(matches[0])
                elif entity_type == 'percentage':
                    entities[entity_type] = self._parse_percentage(matches[0])
                elif entity_type == 'age':
                    entities[entity_type] = self._parse_age(matches[0])
                else:
                    entities[entity_type] = matches[0]
        
        return entities

    def _parse_amount(self, amount_str: str) -> float:
        """Parse monetary amount from string"""
        # Remove currency symbols and text
        cleaned = re.sub(r'[^\d,.]', '', amount_str)
        cleaned = cleaned.replace(',', '')
        
        try:
            return float(cleaned)
        except ValueError:
            return 0.0

    def _parse_percentage(self, percentage_str: str) -> float:
        """Parse percentage from string"""
        numbers = re.findall(r'[\d.]+', percentage_str)
        if numbers:
            return float(numbers[0])
        return 0.0

    def _parse_age(self, age_str: str) -> int:
        """Parse age from string"""
        numbers = re.findall(r'\d+', age_str)
        if numbers:
            return int(numbers[0])
        return 0

    def process_input(self, user_input: str) -> Dict[str, Any]:
        """
        Main processing function that combines all NLP tasks
        """
        processed_input = self.preprocess_input(user_input)
        intent, confidence = self.recognize_intent(processed_input)
        entities = self.extract_entities(processed_input)
        
        return {
            'intent': intent,
            'confidence': confidence,
            'entities': entities,
            'processed_text': processed_input,
            'original_text': user_input
        }

    def get_intent_suggestions(self, user_input: str, top_k: int = 3) -> List[Tuple[str, float]]:
        """Get top-k intent suggestions with confidence scores"""
        processed_input = self.preprocess_input(user_input)
        
        if not self.intent_vectors:
            return [(intent, 0.1) for intent in list(self.financial_intents.keys())[:top_k]]
        
        try:
            input_vector = self.vectorizer.transform([processed_input])
            similarities = cosine_similarity(input_vector, self.intent_vectors)[0]
            
            # Get top-k intents
            top_indices = np.argsort(similarities)[::-1][:len(set(self.intent_labels))]
            
            # Group by intent and take best score for each
            intent_scores = {}
            for idx in top_indices:
                intent = self.intent_labels[idx]
                score = similarities[idx]
                if intent not in intent_scores or score > intent_scores[intent]:
                    intent_scores[intent] = score
            
            # Sort and return top-k
            sorted_intents = sorted(intent_scores.items(), key=lambda x: x[1], reverse=True)
            return sorted_intents[:top_k]
            
        except Exception as e:
            print(f"Error getting intent suggestions: {e}")
            return [(intent, 0.1) for intent in list(self.financial_intents.keys())[:top_k]]