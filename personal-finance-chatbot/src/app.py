# -*- coding: utf-8 -*-
import streamlit as st
import os
import sys
import json
from dotenv import load_dotenv
from datetime import datetime

# Fix Windows console encoding issues
if sys.platform == "win32":
    import codecs
    # Set console encoding to UTF-8 for Windows
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')
    # Set environment variable for Python UTF-8 mode
    os.environ["PYTHONIOENCODING"] = "utf-8"

# Load environment variables
load_dotenv()

# Import our enhanced modules
# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.chatbot.dual_ai_client import DualAIClient
from src.chatbot.nlp import NLPProcessor
from src.chatbot.finance_advisor import FinanceAdvisor
from src.utils.demographics import DemographicsManager

# Page configuration
st.set_page_config(
    page_title="Personal Finance AI",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Import logging for error handling
import logging

# Custom CSS for enhanced UI
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.main-header {
    text-align: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    color: white;
    padding: 5rem 2rem;
    border-radius: 0 0 3rem 3rem;
    margin: -1rem -1rem 4rem -1rem;
    position: relative;
    overflow: hidden;
}

.main-header::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
    animation: float 8s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(-30px) rotate(180deg); }
}

.hero-title {
    font-size: 4rem;
    font-weight: 800;
    margin-bottom: 1.5rem;
    background: linear-gradient(45deg, #ffffff, #e0e7ff, #fbbf24);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 40px rgba(255,255,255,0.6);
    animation: glow 3s ease-in-out infinite alternate;
    z-index: 1;
    position: relative;
}

@keyframes glow {
    from { text-shadow: 0 0 40px rgba(255,255,255,0.6); }
    to { text-shadow: 0 0 60px rgba(255,255,255,0.8), 0 0 80px rgba(59, 130, 246, 0.4); }
}

/* Enhanced Interactive Elements */
.financial-summary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 2rem;
    margin: 2rem 0;
    color: white;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.financial-summary::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
    animation: rotate 10s linear infinite;
}

@keyframes rotate {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.quick-stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin: 2rem 0;
}

.stat-item {
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    padding: 1.5rem;
    border-radius: 1rem;
    text-align: center;
    border: 2px solid #e2e8f0;
    transition: all 0.3s ease;
    cursor: pointer;
}

.stat-item:hover {
    transform: translateY(-5px) scale(1.02);
    border-color: #3B82F6;
    box-shadow: 0 10px 30px rgba(59, 130, 246, 0.2);
}

.pulse-animation {
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
}

.slide-in {
    animation: slideIn 0.8s ease-out;
}

@keyframes slideIn {
    from { transform: translateX(-100px); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

.dashboard-card {
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    padding: 2.5rem;
    border-radius: 1.5rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.12);
    border: 2px solid #e2e8f0;
    margin-bottom: 2rem;
    transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.dashboard-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.1), transparent);
    transition: left 0.8s;
}

.dashboard-card:hover {
    transform: translateY(-8px) scale(1.03);
    box-shadow: 0 20px 60px rgba(0,0,0,0.2);
    border-color: #3B82F6;
}

.dashboard-card:hover::before {
    left: 100%;
}

.feature-card {
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    padding: 2.5rem;
    border-radius: 1.5rem;
    box-shadow: 0 6px 30px rgba(0,0,0,0.1);
    border: 2px solid #f1f5f9;
    text-align: center;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}

.feature-card::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(45deg, #3B82F6, #10B981);
    transform: scaleX(0);
    transition: transform 0.4s ease;
}

.feature-card:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 15px 50px rgba(0,0,0,0.15);
    border-color: #3B82F6;
}

.feature-card:hover::after {
    transform: scaleX(1);
}

.stButton > button {
    background: linear-gradient(135deg, #10B981 0%, #3B82F6 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 15px !important;
    font-weight: 700 !important;
    padding: 1rem 2rem !important;
    transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4) !important;
    font-size: 1rem !important;
    letter-spacing: 0.8px !important;
    text-transform: uppercase !important;
    position: relative !important;
    overflow: hidden !important;
}

.stButton > button::before {
    content: '' !important;
    position: absolute !important;
    top: 0 !important;
    left: -100% !important;
    width: 100% !important;
    height: 100% !important;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent) !important;
    transition: left 0.6s !important;
}

.stButton > button:hover {
    transform: translateY(-4px) scale(1.05) !important;
    box-shadow: 0 12px 35px rgba(59, 130, 246, 0.5) !important;
}

.stButton > button:hover::before {
    left: 100% !important;
}

.stButton > button:active {
    transform: translateY(-2px) scale(1.02) !important;
}

.metric-container {
    background: white;
    padding: 1.5rem;
    border-radius: 1rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    border-left: 4px solid #3B82F6;
    margin-bottom: 1rem;
    transition: all 0.3s ease;
}

.metric-container:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(0,0,0,0.12);
}

.insights-section {
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    padding: 1.5rem;
    border-radius: 1rem;
    border: 1px solid #e2e8f0;
    margin: 1.5rem 0;
}

.offer-card {
    background: linear-gradient(135deg, #10B981, #3B82F6);
    color: white;
    padding: 1.5rem;
    border-radius: 1rem;
    margin-bottom: 1rem;
    transition: all 0.3s ease;
}

.offer-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 30px rgba(16, 185, 129, 0.3);
}

.subscription-card {
    background: white;
    padding: 1.2rem;
    border-radius: 0.8rem;
    box-shadow: 0 3px 15px rgba(0,0,0,0.08);
    border-left: 4px solid #3B82F6;
    margin-bottom: 1rem;
    transition: all 0.3s ease;
}

.subscription-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 25px rgba(0,0,0,0.12);
}

.bill-split-card {
    background: linear-gradient(135deg, #f8fafc, #e2e8f0);
    padding: 1.5rem;
    border-radius: 1rem;
    border: 1px solid #cbd5e1;
    margin-bottom: 1rem;
}

.savings-highlight {
    background: linear-gradient(45deg, #10B981, #059669);
    color: white;
    padding: 0.3rem 0.8rem;
    border-radius: 1rem;
    font-weight: 700;
    font-size: 0.9rem;
}

.category-tag {
    background: #e2e8f0;
    color: #475569;
    padding: 0.2rem 0.6rem;
    border-radius: 1rem;
    font-size: 0.8rem;
    font-weight: 600;
}

.split-amount {
    background: linear-gradient(45deg, #F59E0B, #EF4444);
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 0.5rem;
    font-weight: 700;
    display: inline-block;
}

/* Dark Theme Background */
body {
    background: linear-gradient(-45deg, #0a0a0a, #1a1a1a, #2a2a2a, #1e1e1e);
    background-size: 400% 400%;
    animation: darkGradientShift 20s ease infinite;
    min-height: 100vh;
    color: #ffffff;
}

.stApp {
    background: linear-gradient(-45deg, #0a0a0a, #1a1a1a, #2a2a2a, #1e1e1e);
    background-size: 400% 400%;
    animation: darkGradientShift 20s ease infinite;
    color: #ffffff;
}

/* Enhanced text colors for better contrast */
.stMarkdown, .stText, p, span, div {
    color: #f8fafc !important;
    text-shadow: 0 1px 2px rgba(0,0,0,0.5);
}

.stSelectbox label, .stTextInput label, .stNumberInput label {
    color: #f1f5f9 !important;
    font-weight: 600;
}

/* Card text colors */
.dashboard-card h4, .dashboard-card p {
    color: #1e293b !important;
    text-shadow: none;
}

.feature-card h4, .feature-card p {
    color: #334155 !important;
    text-shadow: none;
}

/* Button text enhancement */
.stButton > button {
    color: #ffffff !important;
    text-shadow: 0 1px 2px rgba(0,0,0,0.3) !important;
    font-weight: 700 !important;
}

/* Input field styling */
.stTextInput > div > div > input, .stNumberInput > div > div > input, .stSelectbox > div > div > select {
    background-color: rgba(255,255,255,0.95) !important;
    color: #1e293b !important;
    border: 2px solid #e2e8f0 !important;
    border-radius: 8px !important;
}

/* Success/Error message styling */
.stSuccess, .stError, .stInfo {
    color: #1e293b !important;
    background-color: rgba(255,255,255,0.95) !important;
    border-radius: 8px !important;
}

@keyframes darkGradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Dark Theme Floating Orbs */
.stApp::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: 
        radial-gradient(circle at 15% 85%, rgba(59, 130, 246, 0.08) 0%, transparent 40%),
        radial-gradient(circle at 85% 15%, rgba(16, 185, 129, 0.06) 0%, transparent 40%),
        radial-gradient(circle at 50% 50%, rgba(139, 92, 246, 0.05) 0%, transparent 40%),
        radial-gradient(circle at 25% 25%, rgba(245, 158, 11, 0.04) 0%, transparent 40%);
    animation: floatOrbs 25s ease-in-out infinite;
    pointer-events: none;
    z-index: -1;
}

@keyframes floatOrbs {
    0%, 100% { transform: translateY(0px) rotate(0deg) scale(1); }
    25% { transform: translateY(-20px) rotate(90deg) scale(1.1); }
    50% { transform: translateY(10px) rotate(180deg) scale(0.9); }
    75% { transform: translateY(-15px) rotate(270deg) scale(1.05); }
}

/* Dark Theme Moving Waves */
.stApp::after {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image:
        linear-gradient(45deg, transparent 30%, rgba(59, 130, 246, 0.04) 50%, transparent 70%),
        linear-gradient(-45deg, transparent 30%, rgba(16, 185, 129, 0.03) 50%, transparent 70%),
        linear-gradient(135deg, transparent 40%, rgba(139, 92, 246, 0.02) 50%, transparent 60%);
    background-size: 300px 300px, 200px 200px, 250px 250px;
    animation: moveWaves 30s linear infinite;
    pointer-events: none;
    z-index: -1;
}

@keyframes moveWaves {
    0% { background-position: 0% 0%, 0% 0%, 0% 0%; }
    100% { background-position: 300px 300px, -200px 200px, 250px -250px; }
}

/* Hide Streamlit default styling */
.block-container {
    padding-top: 1rem;
    position: relative;
    z-index: 1;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user_id' not in st.session_state:
    st.session_state.user_id = "default_user"
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'user_profile_complete' not in st.session_state:
    st.session_state.user_profile_complete = False
if 'show_app' not in st.session_state:
    st.session_state.show_app = True
if 'current_page' not in st.session_state:
    st.session_state.current_page = "profile"
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'user_logged_in' not in st.session_state:
    st.session_state.user_logged_in = False
if 'user_income' not in st.session_state:
    st.session_state.user_income = 0
if 'user_age' not in st.session_state:
    st.session_state.user_age = 0
if 'user_occupation' not in st.session_state:
    st.session_state.user_occupation = ""
if 'current_balance' not in st.session_state:
    st.session_state.current_balance = 0
if 'monthly_spending' not in st.session_state:
    st.session_state.monthly_spending = 0
if 'savings_goal' not in st.session_state:
    st.session_state.savings_goal = 0
if 'investments' not in st.session_state:
    st.session_state.investments = 0
if 'emergency_fund_target' not in st.session_state:
    st.session_state.emergency_fund_target = 0
if 'emergency_fund_current' not in st.session_state:
    st.session_state.emergency_fund_current = 0
if 'student_loan_remaining' not in st.session_state:
    st.session_state.student_loan_remaining = 0
if 'student_loan_original' not in st.session_state:
    st.session_state.student_loan_original = 0
if 'car_fund_target' not in st.session_state:
    st.session_state.car_fund_target = 0
if 'car_fund_current' not in st.session_state:
    st.session_state.car_fund_current = 0
if 'selected_ai_model' not in st.session_state:
    st.session_state.selected_ai_model = "Gemini"
if 'custom_goals' not in st.session_state:
    st.session_state.custom_goals = []
# Initialize new feature states
if 'subscriptions' not in st.session_state:
    st.session_state.subscriptions = [
        {"name": "Spotify Student", "cost": 497, "category": "Entertainment", "next_billing": "2024-02-15"},
        {"name": "Netflix", "cost": 747, "category": "Entertainment", "next_billing": "2024-02-20"},
        {"name": "Adobe Creative", "cost": 1659, "category": "Software", "next_billing": "2024-02-10"},
        {"name": "Gym Membership", "cost": 2075, "category": "Health", "next_billing": "2024-02-05"}
    ]
if 'bill_splits' not in st.session_state:
    st.session_state.bill_splits = []
if 'student_offers' not in st.session_state:
    st.session_state.student_offers = [
        {"service": "Amazon Prime Student", "discount": "50% off", "savings": "₹4897/year", "category": "Shopping"},
        {"service": "Microsoft Office 365", "discount": "Free", "savings": "₹8217/year", "category": "Software"},
        {"service": "Spotify Premium", "discount": "50% off", "savings": "₹4980/year", "category": "Music"},
        {"service": "Adobe Creative Cloud", "discount": "60% off", "savings": "₹29880/year", "category": "Software"},
        {"service": "Hulu + Live TV", "discount": "Student rate", "savings": "₹2905/month", "category": "Streaming"}
    ]

# Initialize components without caching to allow method updates
def initialize_components():
    """Initialize all chatbot components"""
    # Get Gemini API key from environment
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    granite_timeout = int(os.getenv('MODEL_TIMEOUT_SECONDS', 30))
    
    # Initialize Dual AI client (Gemini + Granite)
    ai_client = DualAIClient(gemini_api_key, granite_timeout)
    nlp_processor = NLPProcessor()
    finance_advisor = FinanceAdvisor()
    demographics_manager = DemographicsManager()
    
    return ai_client, nlp_processor, finance_advisor, demographics_manager

if 'ai_components' not in st.session_state:
    st.session_state.ai_components = initialize_components()

ai_client, nlp_processor, finance_advisor, demographics_manager = st.session_state.ai_components

def display_profile_page():
    """Enhanced Profile Page Dashboard"""
    # Hero Header
    st.markdown("""
    <div class="main-header">
        <div class="hero-title">SmartSpends-AI</div>
        <div style="font-size: 1.5rem; opacity: 0.9;">Your Intelligent Money Companion</div>
        <div style="font-size: 1.1rem; opacity: 0.8; margin-top: 1rem;">Welcome back! Here's your financial overview</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Financial Summary Section
    net_worth = st.session_state.current_balance + st.session_state.investments
    monthly_surplus = st.session_state.user_income - st.session_state.monthly_spending
    
    st.markdown(f"""
    <div class="financial-summary">
        <h2 style="margin: 0 0 1rem 0; font-size: 2rem; font-weight: 800; z-index: 1; position: relative;">Financial Health Score</h2>
        <div style="display: flex; justify-content: center; gap: 3rem; margin: 2rem 0; z-index: 1; position: relative;">
            <div style="text-align: center;">
                <div style="font-size: 2.5rem; font-weight: 800;">₹{net_worth:,.0f}</div>
                <div style="opacity: 0.9; font-size: 1rem;">Net Worth</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2.5rem; font-weight: 800; color: {'#10B981' if monthly_surplus >= 0 else '#EF4444'}">₹{monthly_surplus:,.0f}</div>
                <div style="opacity: 0.9; font-size: 1rem;">Monthly Surplus</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2.5rem; font-weight: 800;">85%</div>
                <div style="opacity: 0.9; font-size: 1rem;">Health Score</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced Financial Cards
    st.markdown("""
    <div style="background: white; padding: 1.5rem 2rem; border-radius: 2rem; box-shadow: 0 8px 32px rgba(0,0,0,0.1); 
                margin: 2rem auto; max-width: 600px; text-align: center; border: 2px solid #e2e8f0;">
        <h3 style="color: #1e293b; font-weight: 800; margin: 0; font-size: 2.2rem; 
                   background: linear-gradient(45deg, #3B82F6, #10B981); -webkit-background-clip: text; 
                   -webkit-text-fill-color: transparent;">📊 Your Financial Dashboard</h3>
        <p style="color: #64748b; margin: 0.5rem 0 0 0; font-size: 1rem;">Real-time overview of your finances</p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        balance_color = "#10B981" if st.session_state.current_balance > 0 else "#64748b"
        st.markdown(f"""
        <div class="dashboard-card" style="background: linear-gradient(135deg, #10B981 0%, #059669 100%); color: white; border: none;">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.5rem;">
                <div style="display: flex; align-items: center;">
                    <span style="font-size: 2.5rem; margin-right: 1rem; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));">💰</span>
                    <h4 style="margin: 0; font-weight: 700; font-size: 1.1rem;">Current Balance</h4>
                </div>
                <div style="background: rgba(255,255,255,0.2); padding: 0.5rem; border-radius: 50%; cursor: pointer;">
                    <span style="font-size: 1.2rem;">🔄</span>
                </div>
            </div>
            <p style="font-size: 2.8rem; font-weight: 800; margin: 0; text-shadow: 0 2px 4px rgba(0,0,0,0.2);">₹{st.session_state.current_balance:,.0f}</p>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 1rem;">
                <p style="opacity: 0.9; margin: 0; font-size: 0.95rem;">Available funds</p>
                <div style="background: rgba(255,255,255,0.2); padding: 0.3rem 0.8rem; border-radius: 1rem; font-size: 0.8rem; font-weight: 600;">
                    Active
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        spending_percentage = (st.session_state.monthly_spending / st.session_state.user_income * 100) if st.session_state.user_income > 0 else 0
        st.markdown(f"""
        <div class="dashboard-card" style="background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%); color: white; border: none;">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.5rem;">
                <div style="display: flex; align-items: center;">
                    <span style="font-size: 2.5rem; margin-right: 1rem; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));">📊</span>
                    <h4 style="margin: 0; font-weight: 700; font-size: 1.1rem;">Monthly Spending</h4>
                </div>
                <div style="background: rgba(255,255,255,0.2); padding: 0.5rem; border-radius: 50%; cursor: pointer;">
                    <span style="font-size: 1.2rem;">📈</span>
                </div>
            </div>
            <p style="font-size: 2.8rem; font-weight: 800; margin: 0; text-shadow: 0 2px 4px rgba(0,0,0,0.2);">₹{st.session_state.monthly_spending:,.0f}</p>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 1rem;">
                <p style="opacity: 0.9; margin: 0; font-size: 0.95rem;">This month</p>
                <div style="background: rgba(255,255,255,0.2); padding: 0.3rem 0.8rem; border-radius: 1rem; font-size: 0.8rem; font-weight: 600;">
                    {spending_percentage:.0f}% of income
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        current_savings = st.session_state.current_balance - st.session_state.monthly_spending
        savings_progress = (current_savings / st.session_state.savings_goal * 100) if st.session_state.savings_goal > 0 else 0
        st.markdown(f"""
        <div class="dashboard-card" style="background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%); color: white; border: none;">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.5rem;">
                <div style="display: flex; align-items: center;">
                    <span style="font-size: 2.5rem; margin-right: 1rem; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));">🎯</span>
                    <h4 style="margin: 0; font-weight: 700; font-size: 1.1rem;">Savings Goal</h4>
                </div>
                <div style="background: rgba(255,255,255,0.2); padding: 0.5rem; border-radius: 50%; cursor: pointer;">
                    <span style="font-size: 1.2rem;">🎯</span>
                </div>
            </div>
            <p style="font-size: 2.8rem; font-weight: 800; margin: 0; text-shadow: 0 2px 4px rgba(0,0,0,0.2);">₹{st.session_state.savings_goal:,.0f}</p>
            <div style="margin: 1rem 0;">
                <div style="background: rgba(255,255,255,0.2); border-radius: 10px; height: 8px;">
                    <div style="background: #FBBF24; width: {min(savings_progress, 100):.0f}%; height: 100%; border-radius: 10px; transition: width 0.8s ease;"></div>
                </div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <p style="opacity: 0.9; margin: 0; font-size: 0.95rem;">Target amount</p>
                <div style="background: rgba(255,255,255,0.2); padding: 0.3rem 0.8rem; border-radius: 1rem; font-size: 0.8rem; font-weight: 600;">
                    {savings_progress:.0f}% achieved
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        investment_growth = 5.7  # Mock growth percentage
        st.markdown(f"""
        <div class="dashboard-card" style="background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%); color: white; border: none;">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.5rem;">
                <div style="display: flex; align-items: center;">
                    <span style="font-size: 2.5rem; margin-right: 1rem; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));">📈</span>
                    <h4 style="margin: 0; font-weight: 700; font-size: 1.1rem;">Investments</h4>
                </div>
                <div style="background: rgba(255,255,255,0.2); padding: 0.5rem; border-radius: 50%; cursor: pointer;">
                    <span style="font-size: 1.2rem;">💹</span>
                </div>
            </div>
            <p style="font-size: 2.8rem; font-weight: 800; margin: 0; text-shadow: 0 2px 4px rgba(0,0,0,0.2);">₹{st.session_state.investments:,.0f}</p>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 1rem;">
                <p style="opacity: 0.9; margin: 0; font-size: 0.95rem;">Portfolio value</p>
                <div style="background: rgba(16, 185, 129, 0.8); padding: 0.3rem 0.8rem; border-radius: 1rem; font-size: 0.8rem; font-weight: 600;">
                    +{investment_growth}% ↑
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick Actions with enhanced styling
    st.markdown("""
    <div style="background: white; padding: 1.5rem 2rem; border-radius: 2rem; box-shadow: 0 8px 32px rgba(0,0,0,0.1); 
                margin: 3rem auto 2rem auto; max-width: 500px; text-align: center; border: 2px solid #e2e8f0;">
        <h3 style="color: #1e293b; font-weight: 800; margin: 0; font-size: 2rem; 
                   background: linear-gradient(45deg, #F59E0B, #EF4444); -webkit-background-clip: text; 
                   -webkit-text-fill-color: transparent;">⚡ Quick Actions</h3>
        <p style="color: #64748b; margin: 0.5rem 0 0 0; font-size: 0.95rem;">Manage your finances instantly</p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("💬 AI Chat", use_container_width=True):
            st.session_state.current_page = "chat"
            st.rerun()
    with col2:
        if st.button("📊 Budgets", use_container_width=True):
            st.session_state.current_page = "budgets"
            st.rerun()
    with col3:
        if st.button("💳 Subscriptions", use_container_width=True):
            st.session_state.current_page = "subscriptions"
            st.rerun()
    with col4:
        if st.button("🤝 Bill Split", use_container_width=True):
            st.session_state.current_page = "bill_split"
            st.rerun()
    with col5:
        if st.button("✏️ Edit Profile", use_container_width=True):
            st.session_state.current_page = "edit_profile"
            st.rerun()
    
    # Additional features row with enhanced styling
    st.markdown("""
    <div style="background: white; padding: 1.5rem 2rem; border-radius: 2rem; box-shadow: 0 8px 32px rgba(0,0,0,0.1); 
                margin: 3rem auto 2rem auto; max-width: 500px; text-align: center; border: 2px solid #e2e8f0;">
        <h3 style="color: #1e293b; font-weight: 800; margin: 0; font-size: 2rem; 
                   background: linear-gradient(45deg, #8B5CF6, #EC4899); -webkit-background-clip: text; 
                   -webkit-text-fill-color: transparent;">🚀 More Features</h3>
        <p style="color: #64748b; margin: 0.5rem 0 0 0; font-size: 0.95rem;">Advanced tools for smart money management</p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🎯 Goals", use_container_width=True):
            st.session_state.current_page = "goals"
            st.rerun()
    with col2:
        if st.button("📈 Insights", use_container_width=True):
            st.session_state.current_page = "insights"
            st.rerun()
    with col3:
        if st.button("🎓 Student Offers", use_container_width=True):
            st.session_state.current_page = "student_offers"
            st.rerun()
    with col4:
        if st.button("🏠 Dashboard", use_container_width=True):
            st.session_state.current_page = "profile"
            st.rerun()

def display_login_page():
    """Dedicated Login/Profile Setup Page"""
    st.markdown("""
    <div class="main-header">
        <div class="hero-title">Welcome to SMARTSPENDS</div>
        <div style="font-size: 1.5rem; opacity: 0.9; margin-bottom: 2rem;">Let's set up your financial profile</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<h3 style="color: #1e293b; font-weight: 700; margin: 2rem 0 1.5rem 0; text-align: center;">👤 Personal Information</h3>', unsafe_allow_html=True)
    
    with st.form("user_profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            user_name = st.text_input("📝 Full Name", placeholder="Enter your full name")
            user_age = st.number_input("🎂 Age", min_value=16, max_value=100, value=25)
            user_occupation = st.selectbox("💼 Occupation", [
                "Student", "Professional", "Self-employed", "Part-time Worker", "Unemployed", "Other"
            ])
        
        with col2:
            user_income = st.number_input("💰 Monthly Income (₹)", min_value=0, value=0, step=5000)
            experience_level = st.selectbox("📈 Financial Experience", [
                "Beginner", "Intermediate", "Advanced"
            ])
            risk_tolerance = st.selectbox("⚡ Risk Tolerance", [
                "Conservative", "Moderate", "Aggressive"
            ])
        
        st.markdown('<h4 style="color: #1e293b; margin: 1.5rem 0 1rem 0;">💳 Financial Information</h4>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            current_balance = st.number_input("💰 Current Balance (₹)", min_value=0, value=0, step=1000)
            monthly_spending = st.number_input("📊 Monthly Spending (₹)", min_value=0, value=0, step=1000)
        
        with col2:
            savings_goal = st.number_input("🎯 Savings Goal (₹)", min_value=0, value=0, step=1000)
            investments = st.number_input("📈 Current Investments (₹)", min_value=0, value=0, step=1000)
        
        st.markdown('<h4 style="color: #1e293b; margin: 1.5rem 0 1rem 0;">🎯 Financial Goals Setup</h4>', unsafe_allow_html=True)
        
        # Emergency Fund
        st.markdown('<h5 style="color: #10B981; margin: 1rem 0 0.5rem 0;">🏠 Emergency Fund</h5>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            emergency_fund_target = st.number_input("🎯 Target Amount (₹)", min_value=0, value=0, step=5000, key="ef_target")
        with col2:
            emergency_fund_current = st.number_input("💰 Current Amount (₹)", min_value=0, value=0, step=1000, key="ef_current")
        
        # Student Loan
        st.markdown('<h5 style="color: #EF4444; margin: 1rem 0 0.5rem 0;">🎓 Student Loan Payoff</h5>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            student_loan_original = st.number_input("💵 Original Amount (₹)", min_value=0, value=0, step=10000, key="sl_original")
        with col2:
            student_loan_remaining = st.number_input("💳 Remaining Amount (₹)", min_value=0, value=0, step=5000, key="sl_remaining")
        
        # Car Fund
        st.markdown('<h5 style="color: #3B82F6; margin: 1rem 0 0.5rem 0;">🚗 New Car Fund</h5>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            car_fund_target = st.number_input("🎯 Target Amount (₹)", min_value=0, value=0, step=10000, key="cf_target")
        with col2:
            car_fund_current = st.number_input("💰 Current Saved (₹)", min_value=0, value=0, step=5000, key="cf_current")
        
        st.markdown('<h4 style="color: #1e293b; margin: 1.5rem 0 1rem 0;">🎯 Financial Goals (Select all that apply)</h4>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            emergency_fund = st.checkbox("🏠 Build Emergency Fund")
            pay_debt = st.checkbox("💳 Pay Off Debt")
            save_retirement = st.checkbox("👴 Save for Retirement")
            buy_home = st.checkbox("🏡 Buy a Home")
        
        with col2:
            invest_stocks = st.checkbox("📈 Invest in Stocks")
            start_business = st.checkbox("🚀 Start a Business")
            save_education = st.checkbox("🎓 Save for Education")
            plan_healthcare = st.checkbox("🏥 Plan for Healthcare")
        
        submitted = st.form_submit_button("🚀 Complete Setup", type="primary", use_container_width=True)
        
        if submitted:
            if user_name.strip():
                # Store user information
                st.session_state.user_name = user_name.strip()
                st.session_state.user_age = user_age
                st.session_state.user_occupation = user_occupation
                st.session_state.user_income = user_income
                st.session_state.current_balance = current_balance
                st.session_state.monthly_spending = monthly_spending
                st.session_state.savings_goal = savings_goal
                st.session_state.investments = investments
                st.session_state.emergency_fund_target = emergency_fund_target
                st.session_state.emergency_fund_current = emergency_fund_current
                st.session_state.student_loan_remaining = student_loan_remaining
                st.session_state.student_loan_original = student_loan_original
                st.session_state.car_fund_target = car_fund_target
                st.session_state.car_fund_current = car_fund_current
                st.session_state.user_logged_in = True
                
                # Store goals
                goals = []
                if emergency_fund: goals.append("Emergency Fund")
                if pay_debt: goals.append("Pay Off Debt")
                if save_retirement: goals.append("Save for Retirement")
                if buy_home: goals.append("Buy a Home")
                if invest_stocks: goals.append("Invest in Stocks")
                if start_business: goals.append("Start a Business")
                if save_education: goals.append("Save for Education")
                if plan_healthcare: goals.append("Plan for Healthcare")
                
                # Save to demographics manager
                user_data = {
                    'age': user_age,
                    'occupation': user_occupation.lower(),
                    'income': user_income,
                    'experience_level': experience_level.lower(),
                    'goals': goals,
                    'risk_tolerance': risk_tolerance.lower(),
                    'setup_date': datetime.now().isoformat()
                }
                
                demographics_manager.add_user_profile(st.session_state.user_id, user_data)
                st.success(f"Welcome {user_name}! Your profile has been created successfully.")
                st.rerun()
            else:
                st.error("Please enter your full name to continue.")

def display_chat_page():
    """Enhanced Chat interface page"""
    if st.button("← Back to Dashboard", key="back_from_chat"):
        st.session_state.current_page = "profile"
        st.rerun()
    
    # Enhanced Chat Header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%); color: white; padding: 2.5rem; 
                border-radius: 2rem; margin-bottom: 2rem; text-align: center; box-shadow: 0 10px 40px rgba(59, 130, 246, 0.3);">
        <h1 style="margin: 0; font-size: 2.5rem; font-weight: 800;">💬 SmartSpends-AI Chat</h1>
        <p style="margin: 0.8rem 0 0 0; opacity: 0.9; font-size: 1.1rem;">Get instant financial advice from our AI assistant</p>
    </div>
    """, unsafe_allow_html=True)
    
    # AI Model Selection
    st.markdown("""
    <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 1rem; margin-bottom: 1.5rem; backdrop-filter: blur(10px);">
        <h4 style="color: white; margin: 0 0 0.5rem 0; font-weight: 600;">🤖 Choose Your AI Assistant</h4>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔮 Google Gemini", key="select_gemini", use_container_width=True, 
                    type="primary" if st.session_state.selected_ai_model == "Gemini" else "secondary"):
            st.session_state.selected_ai_model = "Gemini"
            st.success("✅ Gemini AI selected - Advanced reasoning & natural conversations")
    
    with col2:
        if st.button("🏗️ IBM Granite", key="select_granite", use_container_width=True,
                    type="primary" if st.session_state.selected_ai_model == "Granite" else "secondary"):
            st.session_state.selected_ai_model = "Granite"
            st.success("✅ Granite AI selected - Privacy-focused & local processing")
    
    st.markdown(f"""
    <div style="background: rgba(59, 130, 246, 0.2); padding: 0.8rem; border-radius: 0.8rem; margin: 1rem 0; text-align: center;">
        <span style="color: white; font-weight: 600;">Currently using: {st.session_state.selected_ai_model} AI</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat input
    user_input = st.text_input("Ask me about your finances:", placeholder="e.g., How can I save more money this month?")
    
    if st.button("Send"):
        if user_input:
            with st.spinner("🤖 AI is thinking..."):
                try:
                    # Process input with NLP
                    nlp_result = nlp_processor.process_input(user_input)
                    
                    # Get user profile for personalized response
                    user_profile = demographics_manager.get_user_profile(st.session_state.user_id)
                    user_type = demographics_manager.determine_user_type(st.session_state.user_id)
                    
                    # Create enhanced user context for AI
                    user_context = {**user_profile, 'user_type': user_type} if user_profile else {'user_type': 'general'}
                    
                    # Generate response using selected AI model
                    enhanced_prompt = f"Give a short, actionable financial advice in 2-3 sentences maximum. Question: {user_input}"
                    
                    if st.session_state.selected_ai_model == "Gemini":
                        response = ai_client.get_gemini_response(enhanced_prompt, user_context)
                    else:
                        response = ai_client.get_granite_response(enhanced_prompt, user_context)
                    
                    # Limit response length
                    if len(response) > 250:
                        response = response[:247] + "..."
                    
                    # Store in conversation history
                    st.session_state.conversation_history.append((user_input, response))
                    
                    # Display response
                    st.success("💡 **Quick AI Advice:**")
                    st.write(response)
                    
                except Exception as e:
                    st.error(f"❌ System Error: {str(e)}")
                    st.info("🔄 Please try your question again.")
    
    # Display recent chat history
    if st.session_state.conversation_history:
        st.subheader("💬 Recent Conversations")
        for i, (question, answer) in enumerate(reversed(st.session_state.conversation_history[-3:])):
            with st.expander(f"Q: {question[:50]}..."):
                st.write("**You:** " + question)
                st.write("**Assistant:** " + answer)

def display_budget_analyzer():
    """Enhanced Budget analyzer tool"""
    if st.button("← Back to Dashboard", key="back_from_budget"):
        st.session_state.current_page = "profile"
        st.rerun()
    
    # Enhanced Budget Header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #10B981 0%, #059669 100%); color: white; padding: 2.5rem; 
                border-radius: 2rem; margin-bottom: 2rem; text-align: center; box-shadow: 0 10px 40px rgba(16, 185, 129, 0.3);">
        <h1 style="margin: 0; font-size: 2.5rem; font-weight: 800;">📊 Budget Analyzer</h1>
        <p style="margin: 0.8rem 0 0 0; opacity: 0.9; font-size: 1.1rem;">Analyze your income and expenses with AI insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("💡 Enter Your Financial Information"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Income")
            monthly_income = st.number_input("Monthly Income (₹)", min_value=0.0, value=0.0, step=5000.0)
            
            st.subheader("Fixed Expenses")
            housing = st.number_input("Housing (rent/mortgage) (₹)", min_value=0.0, value=0.0, step=2000.0)
            utilities = st.number_input("Utilities (₹)", min_value=0.0, value=0.0, step=1000.0)
        
        with col2:
            st.subheader("Variable Expenses")
            food = st.number_input("Food & Groceries (₹)", min_value=0.0, value=0.0, step=1000.0)
            transportation = st.number_input("Transportation (₹)", min_value=0.0, value=0.0, step=1000.0)
            entertainment = st.number_input("Entertainment (₹)", min_value=0.0, value=0.0, step=1000.0)
        
        if st.button("Analyze Budget", type="primary"):
            if monthly_income > 0:
                total_expenses = housing + utilities + food + transportation + entertainment
                net_savings = monthly_income - total_expenses
                savings_rate = (net_savings / monthly_income) * 100 if monthly_income > 0 else 0
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Monthly Income", f"₹{monthly_income:,.0f}")
                with col2:
                    st.metric("Total Expenses", f"₹{total_expenses:,.0f}")
                with col3:
                    st.metric("Net Savings", f"₹{net_savings:,.0f}")
                
                st.metric("Savings Rate", f"{savings_rate:.1f}%")
            else:
                st.error("Please enter your monthly income to analyze your budget.")

def display_subscriptions_page():
    """Enhanced Subscription tracking page"""
    if st.button("← Back to Dashboard", key="back_from_subscriptions"):
        st.session_state.current_page = "profile"
        st.rerun()
    
    # Enhanced Subscriptions Header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%); color: white; padding: 2.5rem; 
                border-radius: 2rem; margin-bottom: 2rem; text-align: center; box-shadow: 0 10px 40px rgba(139, 92, 246, 0.3);">
        <h1 style="margin: 0; font-size: 2.5rem; font-weight: 800;">💳 Subscription Manager</h1>
        <p style="margin: 0.8rem 0 0 0; opacity: 0.9; font-size: 1.1rem;">Track and manage all your subscriptions in one place</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Overview metrics
    total_monthly = sum(sub['cost'] for sub in st.session_state.subscriptions)
    total_yearly = total_monthly * 12
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Active Subscriptions", len(st.session_state.subscriptions))
    with col2:
        st.metric("Monthly Total", f"₹{total_monthly:.0f}")
    with col3:
        st.metric("Yearly Estimate", f"₹{total_yearly:.0f}")
    
    # Add new subscription
    with st.expander("➕ Add New Subscription"):
        col1, col2 = st.columns(2)
        with col1:
            sub_name = st.text_input("Service Name", placeholder="e.g., Netflix")
            sub_cost = st.number_input("Monthly Cost (₹)", min_value=1.0, value=799.0, step=50.0)
        with col2:
            sub_category = st.selectbox("Category", ["Entertainment", "Software", "Health", "Education", "Shopping", "Other"])
            sub_billing = st.date_input("Next Billing Date")
        
        if st.button("Add Subscription", type="primary"):
            if sub_name.strip():
                new_sub = {
                    "name": sub_name.strip(),
                    "cost": sub_cost,
                    "category": sub_category,
                    "next_billing": sub_billing.strftime("%Y-%m-%d")
                }
                st.session_state.subscriptions.append(new_sub)
                st.success(f"Added {sub_name} subscription!")
                st.rerun()
            else:
                st.error("Please enter a subscription name.")
    
    # Enhanced Subscriptions Display Header
    st.markdown("""
    <div style="background: white; padding: 1.5rem 2rem; border-radius: 2rem; box-shadow: 0 8px 32px rgba(0,0,0,0.1); 
                margin: 2rem auto; max-width: 600px; text-align: center; border: 2px solid #e2e8f0;">
        <h3 style="color: #1e293b; font-weight: 800; margin: 0; font-size: 2rem; 
                   background: linear-gradient(45deg, #8B5CF6, #3B82F6); -webkit-background-clip: text; 
                   -webkit-text-fill-color: transparent;">📊 Your Subscriptions</h3>
        <p style="color: #64748b; margin: 0.5rem 0 0 0; font-size: 0.95rem;">Manage your recurring payments</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display subscriptions using Streamlit components
    for i, sub in enumerate(st.session_state.subscriptions):
        yearly_cost = sub['cost'] * 12
        
        # Category color mapping
        category_colors = {
            'Entertainment': '#EF4444',
            'Software': '#3B82F6', 
            'Health': '#10B981',
            'Education': '#F59E0B',
            'Shopping': '#EC4899',
            'Other': '#6B7280'
        }
        color = category_colors.get(sub['category'], '#6B7280')
        
        with st.container():
            col1, col2, col3 = st.columns([3, 2, 2])
            
            with col1:
                st.markdown(f"""
                <div style="background: white; padding: 1.5rem; border-radius: 1rem; 
                            box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-left: 4px solid {color}; margin-bottom: 1rem;">
                    <h4 style="margin: 0 0 0.5rem 0; color: #1e293b; font-weight: 700;">{sub['name']}</h4>
                    <span style="background: {color}; color: white; padding: 0.2rem 0.6rem; 
                                 border-radius: 1rem; font-size: 0.8rem; font-weight: 600;">{sub['category']}</span>
                    <p style="margin: 0.5rem 0 0 0; color: #64748b; font-size: 0.9rem;">
                        📅 Next: {sub['next_billing']}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.metric("Monthly Cost", f"₹{sub['cost']:.0f}")
                st.metric("Yearly Cost", f"₹{yearly_cost:,}")
            
            with col3:
                if st.button(f"✏️ Edit", key=f"edit_{i}", use_container_width=True):
                    st.info(f"Edit functionality for {sub['name']} - Coming soon!")
                if st.button(f"🗑️ Cancel", key=f"cancel_{i}", use_container_width=True):
                    st.session_state.subscriptions.pop(i)
                    st.success(f"Cancelled {sub['name']} subscription!")
                    st.rerun()

def display_bill_split_page():
    """Enhanced Bill splitting page"""
    if st.button("← Back to Dashboard", key="back_from_bill_split"):
        st.session_state.current_page = "profile"
        st.rerun()
    
    # Enhanced Bill Split Header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%); color: white; padding: 2.5rem; 
                border-radius: 2rem; margin-bottom: 2rem; text-align: center; box-shadow: 0 10px 40px rgba(245, 158, 11, 0.3);">
        <h1 style="margin: 0; font-size: 2.5rem; font-weight: 800;">🤝 Bill Splitting</h1>
        <p style="margin: 0.8rem 0 0 0; opacity: 0.9; font-size: 1.1rem;">Split expenses with friends and track payments easily</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create new bill split
    with st.expander("➕ Split a New Bill"):
        col1, col2 = st.columns(2)
        with col1:
            bill_name = st.text_input("Bill Description", placeholder="e.g., Dinner at Restaurant")
            total_amount = st.number_input("Total Amount (₹)", min_value=1.0, value=4150.0, step=50.0)
        with col2:
            your_name = st.text_input("Your Name", value="User")
            friends = st.text_area("Friends (one per line)", placeholder="Alice\nBob\nCharlie")
        
        if friends and total_amount > 0:
            friend_list = [f.strip() for f in friends.split('\n') if f.strip()]
            total_people = len(friend_list) + 1
            per_person = total_amount / total_people
            
            st.info(f"Each person pays: ₹{per_person:.0f}")
            
            if st.button("Create Split", type="primary"):
                new_split = {
                    "bill_name": bill_name,
                    "total_amount": total_amount,
                    "your_share": per_person,
                    "friends": friend_list,
                    "settled": False
                }
                st.session_state.bill_splits.append(new_split)
                st.success(f"Created bill split for {bill_name}!")
                st.rerun()
    
    # Display active bill splits
    if st.session_state.bill_splits:
        st.subheader("📋 Active Bill Splits")
        for i, split in enumerate(st.session_state.bill_splits):
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(f"**{split['bill_name']}** - ₹{split['total_amount']:.0f}")
                st.write(f"Your share: ₹{split['your_share']:.0f}")
            with col2:
                status = "✅ Settled" if split.get('settled', False) else "⏳ Pending"
                st.write(status)
            with col3:
                if not split.get('settled', False):
                    if st.button("Mark Settled", key=f"settle_{i}"):
                        st.session_state.bill_splits[i]['settled'] = True
                        st.rerun()

def display_goals_page():
    """Enhanced Goals management page"""
    if st.button("← Back to Dashboard", key="back_from_goals"):
        st.session_state.current_page = "profile"
        st.rerun()
    
    # Enhanced Goals Header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%); color: white; padding: 2.5rem; 
                border-radius: 2rem; margin-bottom: 2rem; text-align: center; box-shadow: 0 10px 40px rgba(239, 68, 68, 0.3);">
        <h1 style="margin: 0; font-size: 2.5rem; font-weight: 800;">🎯 Financial Goals</h1>
        <p style="margin: 0.8rem 0 0 0; opacity: 0.9; font-size: 1.1rem;">Set, track, and achieve your financial milestones</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Active Goals", "3")
    with col2:
        st.metric("Goals Achieved", "1")
    with col3:
        st.metric("Total Progress", "65%")
    
    # Emergency Fund Goal
    st.subheader("🏠 Emergency Fund")
    ef_progress = (st.session_state.emergency_fund_current / st.session_state.emergency_fund_target * 100) if st.session_state.emergency_fund_target > 0 else 0
    st.write(f"**Target:** ₹{st.session_state.emergency_fund_target:,.0f} • **Current:** ₹{st.session_state.emergency_fund_current:,.0f} ({ef_progress:.0f}%)")
    st.progress(ef_progress / 100)
    
    # Student Loan Goal
    st.subheader("🎓 Student Loan Payoff")
    sl_progress = ((st.session_state.student_loan_original - st.session_state.student_loan_remaining) / st.session_state.student_loan_original * 100) if st.session_state.student_loan_original > 0 else 0
    st.write(f"**Remaining:** ₹{st.session_state.student_loan_remaining:,.0f} • **Original:** ₹{st.session_state.student_loan_original:,.0f}")
    st.progress(sl_progress / 100)
    
    # New Car Goal
    st.subheader("🚗 New Car Fund")
    cf_progress = (st.session_state.car_fund_current / st.session_state.car_fund_target * 100) if st.session_state.car_fund_target > 0 else 0
    st.write(f"**Target:** ₹{st.session_state.car_fund_target:,.0f} • **Current:** ₹{st.session_state.car_fund_current:,.0f} ({cf_progress:.0f}%)")
    st.progress(cf_progress / 100)
    
    # Add New Goal with enhanced UI
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(248,250,252,0.95) 100%); 
                padding: 2rem; border-radius: 2rem; box-shadow: 0 12px 40px rgba(0,0,0,0.15); 
                margin: 2rem 0; border: 2px solid rgba(239, 68, 68, 0.2); backdrop-filter: blur(10px);">
        <h3 style="color: #1e293b; font-weight: 800; margin: 0 0 1rem 0; font-size: 1.8rem; text-align: center;
                   background: linear-gradient(45deg, #EF4444, #F59E0B); -webkit-background-clip: text; 
                   -webkit-text-fill-color: transparent;">➕ Create New Goal</h3>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("new_goal_form"):
        col1, col2 = st.columns(2)
        with col1:
            goal_name = st.text_input("🎯 Goal Name", placeholder="e.g., Vacation Fund, New Laptop")
            target_amount = st.number_input("💰 Target Amount (₹)", min_value=1000, value=50000, step=5000)
        with col2:
            target_date = st.date_input("📅 Target Date")
            monthly_contribution = st.number_input("📈 Monthly Contribution (₹)", min_value=500, value=5000, step=500)
        
        goal_category = st.selectbox("📂 Category", ["Savings", "Investment", "Purchase", "Travel", "Education", "Emergency", "Other"])
        goal_description = st.text_area("📝 Description (Optional)", placeholder="Brief description of your goal...")
        
        submitted = st.form_submit_button("🚀 Create Goal", type="primary", use_container_width=True)
        
        if submitted and goal_name.strip():
            # Initialize custom goals list if not exists
            if 'custom_goals' not in st.session_state:
                st.session_state.custom_goals = []
            
            # Calculate timeline
            months_needed = target_amount // monthly_contribution if monthly_contribution > 0 else 999
            
            new_goal = {
                "name": goal_name.strip(),
                "target_amount": target_amount,
                "current_amount": 0,
                "monthly_contribution": monthly_contribution,
                "target_date": target_date.strftime("%Y-%m-%d"),
                "category": goal_category,
                "description": goal_description.strip(),
                "created_date": datetime.now().strftime("%Y-%m-%d"),
                "months_needed": months_needed
            }
            
            st.session_state.custom_goals.append(new_goal)
            st.success(f"✅ Created new goal: {goal_name} (₹{target_amount:,.0f})")
            # Custom coin animation
            st.markdown("""
            <style>
            @keyframes coinFall {
                0% { transform: translateY(-100vh) rotate(0deg); opacity: 0.5; }
                100% { transform: translateY(100vh) rotate(360deg); opacity: 0; }
            }
            .coin {
                position: fixed;
                font-size: 2rem;
                opacity: 0.5;
                animation: coinFall 3s linear;
                z-index: 9999;
                pointer-events: none;
            }
            </style>
            <div class="coin" style="left: 15%; animation-delay: 0s;">🪙</div>
            <div class="coin" style="left: 35%; animation-delay: 0.3s;">💰</div>
            <div class="coin" style="left: 55%; animation-delay: 0.6s;">🪙</div>
            <div class="coin" style="left: 75%; animation-delay: 0.9s;">💰</div>
            """, unsafe_allow_html=True)
            st.rerun()
        elif submitted:
            st.error("Please enter a goal name.")
    
    # Display custom goals if any exist
    if 'custom_goals' in st.session_state and st.session_state.custom_goals:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(248,250,252,0.95) 100%); 
                    padding: 2rem; border-radius: 2rem; box-shadow: 0 12px 40px rgba(0,0,0,0.15); 
                    margin: 2rem 0; border: 2px solid rgba(16, 185, 129, 0.2); backdrop-filter: blur(10px);">
            <h3 style="color: #1e293b; font-weight: 800; margin: 0 0 1rem 0; font-size: 1.8rem; text-align: center;
                       background: linear-gradient(45deg, #10B981, #3B82F6); -webkit-background-clip: text; 
                       -webkit-text-fill-color: transparent;">🎯 Your Custom Goals</h3>
        </div>
        """, unsafe_allow_html=True)
        
        for i, goal in enumerate(st.session_state.custom_goals):
            progress = (goal['current_amount'] / goal['target_amount'] * 100) if goal['target_amount'] > 0 else 0
            
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.markdown(f"""
                <div style="background: white; padding: 1.5rem; border-radius: 1rem; 
                            box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-left: 4px solid #10B981;">
                    <h4 style="margin: 0 0 0.5rem 0; color: #1e293b; font-weight: 700;">{goal['name']}</h4>
                    <p style="margin: 0 0 0.5rem 0; color: #64748b; font-size: 0.9rem;">{goal['description']}</p>
                    <div style="background: #f1f5f9; border-radius: 10px; height: 8px; margin: 1rem 0;">
                        <div style="background: #10B981; width: {progress:.1f}%; height: 100%; border-radius: 10px;"></div>
                    </div>
                    <p style="margin: 0; color: #10B981; font-weight: 600; font-size: 0.9rem;">{progress:.1f}% Complete</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.metric("Target", f"₹{goal['target_amount']:,.0f}")
                st.metric("Monthly", f"₹{goal['monthly_contribution']:,.0f}")
            
            with col3:
                st.metric("Timeline", f"{goal['months_needed']} months")
                if st.button(f"🗑️ Delete", key=f"delete_goal_{i}"):
                    st.session_state.custom_goals.pop(i)
                    st.rerun()

def display_insights_page():
    """Enhanced Financial insights page"""
    if st.button("← Back to Dashboard", key="back_from_insights"):
        st.session_state.current_page = "profile"
        st.rerun()
    
    # Enhanced Insights Header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #06B6D4 0%, #0891B2 100%); color: white; padding: 2.5rem; 
                border-radius: 2rem; margin-bottom: 2rem; text-align: center; box-shadow: 0 10px 40px rgba(6, 182, 212, 0.3);">
        <h1 style="margin: 0; font-size: 2.5rem; font-weight: 800;">📈 Financial Insights</h1>
        <p style="margin: 0.8rem 0 0 0; opacity: 0.9; font-size: 1.1rem;">AI-powered analysis of your spending patterns and trends</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced Insights Display
    st.markdown("""
    <div style="background: white; padding: 1.5rem 2rem; border-radius: 2rem; box-shadow: 0 8px 32px rgba(0,0,0,0.1); 
                margin: 2rem auto; max-width: 600px; text-align: center; border: 2px solid #e2e8f0;">
        <h3 style="color: #1e293b; font-weight: 800; margin: 0; font-size: 2rem; 
                   background: linear-gradient(45deg, #06B6D4, #10B981); -webkit-background-clip: text; 
                   -webkit-text-fill-color: transparent;">💡 This Month's Insights</h3>
        <p style="color: #64748b; margin: 0.5rem 0 0 0; font-size: 0.95rem;">AI-powered financial analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #10B981, #059669); color: white; padding: 1.5rem; border-radius: 1rem; text-align: center; margin-bottom: 1rem;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">✅</div>
            <h4 style="margin: 0; font-weight: 700;">Budget Status</h4>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 0.9rem;">75% utilized - On track!</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #F59E0B, #D97706); color: white; padding: 1.5rem; border-radius: 1rem; text-align: center; margin-bottom: 1rem;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">⚠️</div>
            <h4 style="margin: 0; font-weight: 700;">Entertainment</h4>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 0.9rem;">15% above average</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #3B82F6, #1D4ED8); color: white; padding: 1.5rem; border-radius: 1rem; text-align: center; margin-bottom: 1rem;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">📈</div>
            <h4 style="margin: 0; font-weight: 700;">Investments</h4>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 0.9rem;">+5.7% this month!</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Spending breakdown
    st.subheader("📊 Spending Breakdown")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Top Categories:**")
        st.write("• Food & Dining: ₹40,272 (39%)")
        st.write("• Transportation: ₹18,272 (18%)")
        st.write("• Housing: ₹24,900 (24%)")
    with col2:
        st.write("**Recommendations:**")
        st.write("• Consider meal planning to reduce food costs")
        st.write("• Look into public transportation options")
        st.write("• Review subscription services")

def display_student_offers_page():
    """Enhanced Student discounts and offers page"""
    if st.button("← Back to Dashboard", key="back_from_student_offers"):
        st.session_state.current_page = "profile"
        st.rerun()
    
    # Enhanced Student Offers Header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #EC4899 0%, #DB2777 100%); color: white; padding: 2.5rem; 
                border-radius: 2rem; margin-bottom: 2rem; text-align: center; box-shadow: 0 10px 40px rgba(236, 72, 153, 0.3);">
        <h1 style="margin: 0; font-size: 2.5rem; font-weight: 800;">🎓 Student Discounts & Offers</h1>
        <p style="margin: 0.8rem 0 0 0; opacity: 0.9; font-size: 1.1rem;">Save money with exclusive student deals and discounts</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate total potential savings
    total_yearly_savings = sum(int(offer['savings'].replace('₹', '').replace('/year', '').replace('/month', '').replace(',', '')) 
                              * (12 if '/month' in offer['savings'] else 1) 
                              for offer in st.session_state.student_offers 
                              if '₹' in offer['savings'])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Available Offers", len(st.session_state.student_offers))
    with col2:
        st.metric("Potential Yearly Savings", f"₹{total_yearly_savings:,}")
    with col3:
        st.metric("Categories", len(set(offer['category'] for offer in st.session_state.student_offers)))
    
    # Enhanced Offers Display
    st.markdown("""
    <div style="background: white; padding: 1.5rem 2rem; border-radius: 2rem; box-shadow: 0 8px 32px rgba(0,0,0,0.1); 
                margin: 2rem auto; max-width: 500px; text-align: center; border: 2px solid #e2e8f0;">
        <h3 style="color: #1e293b; font-weight: 800; margin: 0; font-size: 2rem; 
                   background: linear-gradient(45deg, #EC4899, #F59E0B); -webkit-background-clip: text; 
                   -webkit-text-fill-color: transparent;">💰 Available Offers</h3>
        <p style="color: #64748b; margin: 0.5rem 0 0 0; font-size: 0.95rem;">Exclusive deals just for students</p>
    </div>
    """, unsafe_allow_html=True)
    
    for offer in st.session_state.student_offers:
        st.markdown(f"""
        <div class="offer-card" style="margin-bottom: 1.5rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h3 style="margin: 0; color: white; font-size: 1.4rem; font-weight: 700;">{offer['service']}</h3>
                    <p style="margin: 0.5rem 0; opacity: 0.9; font-size: 1rem;">{offer['discount']}</p>
                    <span style="background: rgba(255,255,255,0.2); padding: 0.3rem 0.8rem; border-radius: 1rem; font-size: 0.85rem; font-weight: 600;">
                        {offer['category']}
                    </span>
                </div>
                <div style="text-align: right;">
                    <div class="savings-highlight" style="font-size: 1.1rem; margin-bottom: 0.8rem;">{offer['savings']}</div>
                    <div style="display: flex; gap: 0.5rem;">
                        <button style="background: rgba(255,255,255,0.2); border: none; padding: 0.5rem 1rem; border-radius: 0.5rem; color: white; cursor: pointer; font-weight: 600;">🔗 Get</button>
                        <button style="background: rgba(255,255,255,0.2); border: none; padding: 0.5rem 1rem; border-radius: 0.5rem; color: white; cursor: pointer; font-weight: 600;">ℹ️ Info</button>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def display_landing_page():
    """Professional Landing Page"""
    # Hero Section
    st.markdown("""
    <div class="main-header">
        <div class="hero-title">SMARTSPENDS</div>
        <div style="font-size: 1.8rem; font-weight: 500; margin-bottom: 1.5rem; opacity: 0.95;">Personal Finance AI</div>
        <div style="font-size: 1.3rem; margin-bottom: 2rem; opacity: 0.9; max-width: 600px; margin-left: auto; margin-right: auto; line-height: 1.6;">
            Your Intelligent Money Companion powered by Google Gemini 1.5 Flash with Granite AI fallback for reliable, personalized financial guidance.
        </div>
        <div style="margin-top: 2rem;">
            <div style="display: flex; justify-content: center; gap: 2rem; margin-bottom: 2rem;">
                <div style="text-align: center;">
                    <div style="font-size: 2.5rem; font-weight: 700; color: #ffffff;">AI</div>
                    <div style="font-size: 0.9rem; opacity: 0.8;">Powered</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 2.5rem; font-weight: 700; color: #ffffff;">24/7</div>
                    <div style="font-size: 0.9rem; opacity: 0.8;">Available</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 2.5rem; font-weight: 700; color: #ffffff;">100%</div>
                    <div style="font-size: 0.9rem; opacity: 0.8;">Personalized</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # CTA Button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Get Started", key="hero_cta", help="Start your financial journey"):
            st.session_state.show_app = True
            st.rerun()
    
    # Features Section
    st.markdown('<h2 style="text-align: center; font-size: 2.5rem; font-weight: 700; color: #1e293b; margin: 4rem 0 3rem 0;">Smart Features for Smarter Money</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    features = [
        ("📊", "Budget Analysis", "Intelligent budget tracking with personalized insights and spending pattern analysis"),
        ("💡", "Smart Spending Insights", "AI-powered recommendations to optimize your spending and find savings opportunities"),
        ("🎯", "Goal-Based Planning", "Set and track financial goals with step-by-step guidance tailored to your timeline"),
        ("📈", "Investment Guidance", "Student-friendly investment advice with risk-appropriate recommendations"),
        ("💳", "Debt Management", "Strategic debt repayment plans and credit building advice for students"),
        ("🤖", "Dual AI System", "Google Gemini for advanced insights, Granite for reliable fallback responses")
    ]
    
    for i, (icon, title, description) in enumerate(features):
        col = [col1, col2, col3][i % 3]
        with col:
            st.markdown(f"""
            <div class="feature-card">
                <div style="font-size: 3rem; margin-bottom: 1rem; background: linear-gradient(45deg, #3B82F6, #10B981); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{icon}</div>
                <div style="font-size: 1.3rem; font-weight: 600; color: #1e293b; margin-bottom: 0.8rem;">{title}</div>
                <div style="color: #64748b; line-height: 1.5;">{description}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Why Choose Us Section
    st.markdown('<h2 style="text-align: center; font-size: 2.5rem; font-weight: 700; color: #1e293b; margin: 4rem 0 3rem 0;">Why Choose SMARTSPENDS?</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    why_choose_items = [
        ("🔒", "Data Security First", "Your financial data is protected with enterprise-grade security and privacy measures"),
        ("🎯", "AI-Powered Precision", "Cutting-edge AI technology provides accurate, contextual financial advice"),
        ("🎓", "Built for Students", "Designed specifically for student financial challenges and opportunities"),
        ("🚀", "Always Improving", "Continuous learning AI that gets better at helping you over time")
    ]
    
    for i, (icon, title, description) in enumerate(why_choose_items):
        col = col1 if i % 2 == 0 else col2
        with col:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); padding: 2rem; border-radius: 1rem; text-align: center; border: 1px solid #e2e8f0; margin-bottom: 1.5rem; transition: all 0.3s ease;">
                <div style="font-size: 3rem; margin-bottom: 1rem; background: linear-gradient(45deg, #3B82F6, #10B981); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{icon}</div>
                <div style="font-size: 1.3rem; font-weight: 600; color: #1e293b; margin-bottom: 0.8rem;">{title}</div>
                <div style="color: #64748b; line-height: 1.5;">{description}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Call to Action Section
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e293b 0%, #334155 100%); color: white; padding: 4rem 2rem; border-radius: 2rem; text-align: center; margin: 4rem 0;">
        <div style="font-size: 2.5rem; font-weight: 700; margin-bottom: 2rem;">Plan smarter. Spend better. Save faster.</div>
        <p style="font-size: 1.2rem; opacity: 0.9; margin-bottom: 2rem; max-width: 600px; margin-left: auto; margin-right: auto;">
            Join thousands of students who are already taking control of their financial future with AI-powered guidance.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Big CTA button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🎯 Start with SmartSpends", key="main_cta", help="Begin your financial journey"):
            st.session_state.show_app = True
            st.rerun()
    
    # Footer
    st.markdown("""
    <div style="text-align: center; padding: 3rem 2rem; color: #64748b; border-top: 1px solid #e2e8f0; margin-top: 4rem;">
        <div style="margin-bottom: 1.5rem;">
            <a href="#" style="margin: 0 1.5rem; color: #64748b; text-decoration: none; font-weight: 500;">About</a>
            <a href="#" style="margin: 0 1.5rem; color: #64748b; text-decoration: none; font-weight: 500;">Privacy Policy</a>
            <a href="#" style="margin: 0 1.5rem; color: #64748b; text-decoration: none; font-weight: 500;">Contact</a>
        </div>
        <div style="font-weight: 500;">© 2025 SmartSpends. All rights reserved.</div>
    </div>
    """, unsafe_allow_html=True)

def display_edit_profile_page():
    """Edit Profile Page"""
    if st.button("← Back to Dashboard", key="back_from_edit_profile"):
        st.session_state.current_page = "profile"
        st.rerun()
    
    # Enhanced Edit Profile Header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%); color: white; padding: 2.5rem; 
                border-radius: 2rem; margin-bottom: 2rem; text-align: center; box-shadow: 0 10px 40px rgba(139, 92, 246, 0.3);">
        <h1 style="margin: 0; font-size: 2.5rem; font-weight: 800;">✏️ Edit Profile</h1>
        <p style="margin: 0.8rem 0 0 0; opacity: 0.9; font-size: 1.1rem;">Update your financial information</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("edit_profile_form"):
        st.markdown('<h3 style="color: #f8fafc; font-weight: 700; margin: 2rem 0 1.5rem 0; text-align: center;">👤 Personal Information</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            user_name = st.text_input("📝 Full Name", value=st.session_state.user_name)
            user_age = st.number_input("🎂 Age", min_value=16, max_value=100, value=st.session_state.user_age)
            user_occupation = st.selectbox("💼 Occupation", [
                "Student", "Professional", "Self-employed", "Part-time Worker", "Unemployed", "Other"
            ], index=["Student", "Professional", "Self-employed", "Part-time Worker", "Unemployed", "Other"].index(st.session_state.user_occupation) if st.session_state.user_occupation in ["Student", "Professional", "Self-employed", "Part-time Worker", "Unemployed", "Other"] else 0)
        
        with col2:
            user_income = st.number_input("💰 Monthly Income (₹)", min_value=0, value=st.session_state.user_income, step=5000)
            current_balance = st.number_input("💰 Current Balance (₹)", min_value=0, value=st.session_state.current_balance, step=1000)
            monthly_spending = st.number_input("📊 Monthly Spending (₹)", min_value=0, value=st.session_state.monthly_spending, step=1000)
        
        st.markdown('<h4 style="color: #f8fafc; margin: 1.5rem 0 1rem 0;">🎯 Financial Goals</h4>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            savings_goal = st.number_input("🎯 Savings Goal (₹)", min_value=0, value=st.session_state.savings_goal, step=1000)
            investments = st.number_input("📈 Current Investments (₹)", min_value=0, value=st.session_state.investments, step=1000)
            emergency_fund_target = st.number_input("🏠 Emergency Fund Target (₹)", min_value=0, value=st.session_state.emergency_fund_target, step=5000)
        
        with col2:
            emergency_fund_current = st.number_input("💰 Emergency Fund Current (₹)", min_value=0, value=st.session_state.emergency_fund_current, step=1000)
            car_fund_target = st.number_input("🚗 Car Fund Target (₹)", min_value=0, value=st.session_state.car_fund_target, step=10000)
            car_fund_current = st.number_input("💰 Car Fund Current (₹)", min_value=0, value=st.session_state.car_fund_current, step=5000)
        
        submitted = st.form_submit_button("💾 Save Changes", type="primary", use_container_width=True)
        
        if submitted:
            # Update session state with new values
            st.session_state.user_name = user_name
            st.session_state.user_age = user_age
            st.session_state.user_occupation = user_occupation
            st.session_state.user_income = user_income
            st.session_state.current_balance = current_balance
            st.session_state.monthly_spending = monthly_spending
            st.session_state.savings_goal = savings_goal
            st.session_state.investments = investments
            st.session_state.emergency_fund_target = emergency_fund_target
            st.session_state.emergency_fund_current = emergency_fund_current
            st.session_state.car_fund_target = car_fund_target
            st.session_state.car_fund_current = car_fund_current
            
            # Update demographics manager
            user_data = {
                'age': user_age,
                'occupation': user_occupation.lower(),
                'income': user_income,
                'setup_date': datetime.now().isoformat()
            }
            demographics_manager.add_user_profile(st.session_state.user_id, user_data)
            
            st.success("✅ Profile updated successfully!")
            # Custom coin animation with CSS
            st.markdown("""
            <style>
            @keyframes coinFall {
                0% { transform: translateY(-100vh) rotate(0deg); opacity: 0.5; }
                100% { transform: translateY(100vh) rotate(360deg); opacity: 0; }
            }
            .coin {
                position: fixed;
                font-size: 2rem;
                opacity: 0.5;
                animation: coinFall 3s linear;
                z-index: 9999;
                pointer-events: none;
            }
            </style>
            <div class="coin" style="left: 10%; animation-delay: 0s;">🪙</div>
            <div class="coin" style="left: 20%; animation-delay: 0.2s;">💰</div>
            <div class="coin" style="left: 30%; animation-delay: 0.4s;">🪙</div>
            <div class="coin" style="left: 40%; animation-delay: 0.6s;">💰</div>
            <div class="coin" style="left: 50%; animation-delay: 0.8s;">🪙</div>
            <div class="coin" style="left: 60%; animation-delay: 1s;">💰</div>
            <div class="coin" style="left: 70%; animation-delay: 1.2s;">🪙</div>
            <div class="coin" style="left: 80%; animation-delay: 1.4s;">💰</div>
            <div class="coin" style="left: 90%; animation-delay: 1.6s;">🪙</div>
            """, unsafe_allow_html=True)
            
            # Auto-redirect after 2 seconds
            import time
            time.sleep(1)
            st.session_state.current_page = "profile"
            st.rerun()

def main():
    """Main application function"""
    # Check if user wants to see the app
    if not st.session_state.show_app:
        display_landing_page()
        return
    
    # Check if user is logged in
    if not st.session_state.user_logged_in:
        display_login_page()
        return
    
    # Display the appropriate page based on current_page
    current_page = st.session_state.get('current_page', 'profile')
    
    if current_page == "profile":
        display_profile_page()
    elif current_page == "chat":
        display_chat_page()
    elif current_page == "budgets":
        display_budget_analyzer()
    elif current_page == "subscriptions":
        display_subscriptions_page()
    elif current_page == "bill_split":
        display_bill_split_page()
    elif current_page == "goals":
        display_goals_page()
    elif current_page == "insights":
        display_insights_page()
    elif current_page == "student_offers":
        display_student_offers_page()
    elif current_page == "edit_profile":
        display_edit_profile_page()
    else:
        display_profile_page()

if __name__ == "__main__":
    main()