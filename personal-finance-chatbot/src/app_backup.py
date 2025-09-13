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
    page_title="SMARTSPENDS – SmartSpends-AI",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for fintech styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.main-header {
    text-align: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 4rem 2rem;
    border-radius: 0 0 2rem 2rem;
    margin: -1rem -1rem 3rem -1rem;
}

.hero-title {
    font-size: 3.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    background: linear-gradient(45deg, #ffffff, #e0e7ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 30px rgba(255,255,255,0.5);
}

.hero-subtitle {
    font-size: 1.5rem;
    font-weight: 400;
    margin-bottom: 1rem;
    opacity: 0.9;
}

.hero-description {
    font-size: 1.1rem;
    opacity: 0.8;
    max-width: 600px;
    margin: 0 auto 2rem auto;
    line-height: 1.6;
}

.cta-button {
    background: linear-gradient(45deg, #10B981, #3B82F6);
    color: white;
    padding: 1rem 2.5rem;
    border: none;
    border-radius: 50px;
    font-size: 1.1rem;
    font-weight: 600;
    text-decoration: none;
    display: inline-block;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
}

.cta-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4);
}

/* Custom button styling for Streamlit */
.stButton > button {
    background: linear-gradient(45deg, #10B981, #3B82F6) !important;
    color: white !important;
    border: none !important;
    border-radius: 50px !important;
    font-weight: 600 !important;
    padding: 0.8rem 2rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4) !important;
}

.feature-card {
    background: white;
    padding: 2rem;
    border-radius: 1rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    border: 1px solid #f1f5f9;
    text-align: center;
    transition: all 0.3s ease;
    margin-bottom: 1.5rem;
}

.feature-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 40px rgba(0,0,0,0.12);
}

.feature-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
    background: linear-gradient(45deg, #3B82F6, #10B981);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.feature-title {
    font-size: 1.3rem;
    font-weight: 600;
    color: #1e293b;
    margin-bottom: 0.5rem;
}

.feature-description {
    color: #64748b;
    line-height: 1.5;
}

.section-title {
    font-size: 2.5rem;
    font-weight: 700;
    text-align: center;
    color: #1e293b;
    margin-bottom: 3rem;
    background: linear-gradient(45deg, #1e293b, #475569);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.why-choose-card {
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    padding: 2rem;
    border-radius: 1rem;
    text-align: center;
    border: 1px solid #e2e8f0;
    margin-bottom: 1.5rem;
}

.cta-section {
    background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
    color: white;
    padding: 4rem 2rem;
    border-radius: 2rem;
    text-align: center;
    margin: 3rem 0;
}

.cta-title {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 2rem;
}

.footer {
    text-align: center;
    padding: 2rem;
    color: #64748b;
    border-top: 1px solid #e2e8f0;
    margin-top: 3rem;
}

.stats-container {
    display: flex;
    justify-content: space-around;
    margin: 2rem 0;
    flex-wrap: wrap;
}

.stat-item {
    text-align: center;
    margin: 1rem;
}

.stat-number {
    font-size: 2.5rem;
    font-weight: 700;
    color: #3B82F6;
}

.stat-label {
    font-size: 0.9rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Profile Page Styles */
.profile-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 3rem;
    border-radius: 1.5rem;
    margin-bottom: 2.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    position: relative;
    overflow: hidden;
}

.profile-avatar {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    background: linear-gradient(45deg, #10B981, #3B82F6);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.5rem;
    font-weight: 700;
    color: white;
    margin-right: 2rem;
    box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    border: 4px solid rgba(255,255,255,0.3);
    transition: all 0.3s ease;
}

.profile-info {
    flex-grow: 1;
}

.profile-name {
    font-size: 2.5rem;
    font-weight: 800;
    margin: 0;
    text-shadow: 0 2px 10px rgba(0,0,0,0.2);
}

.profile-subtitle {
    font-size: 1.2rem;
    opacity: 0.9;
    margin: 0.8rem 0 0 0;
    font-weight: 400;
}

.dashboard-card {
    background: white;
    padding: 2rem;
    border-radius: 1.2rem;
    box-shadow: 0 6px 25px rgba(0,0,0,0.1);
    border: 1px solid #e2e8f0;
    margin-bottom: 1.5rem;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.dashboard-card:hover {
    transform: translateY(-5px) scale(1.02);
    box-shadow: 0 15px 45px rgba(0,0,0,0.15);
    border-color: #3B82F6;
}

.card-header {
    display: flex;
    align-items: center;
    margin-bottom: 1rem;
}

.card-icon {
    font-size: 2rem;
    margin-right: 1rem;
    background: linear-gradient(45deg, #3B82F6, #10B981);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    filter: drop-shadow(0 2px 4px rgba(59, 130, 246, 0.3));
}

.card-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #1e293b;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    margin: 0;
}

.card-value {
    font-size: 2rem;
    font-weight: 700;
    color: #000000;
    margin: 0;
}

.card-change {
    font-size: 0.9rem;
    margin-top: 0.5rem;
}

.positive-change {
    color: #10B981;
}

.negative-change {
    color: #EF4444;
}

.insights-section {
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    padding: 1.5rem;
    border-radius: 1rem;
    border: 1px solid #e2e8f0;
    margin: 1.5rem 0;
}

.insight-item {
    background: white;
    padding: 1rem;
    border-radius: 0.5rem;
    margin-bottom: 0.8rem;
    border-left: 4px solid #3B82F6;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.alert-item {
    background: #FEF3C7;
    border-left-color: #F59E0B;
}

.navigation-menu {
    background: white;
    padding: 1rem;
    border-radius: 1rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    border: 1px solid #f1f5f9;
    margin-top: 2rem;
}

.nav-item {
    display: flex;
    align-items: center;
    padding: 0.8rem 1rem;
    margin: 0.3rem 0;
    border-radius: 0.5rem;
    cursor: pointer;
    transition: all 0.3s ease;
    text-decoration: none;
    color: #64748b;
}

.nav-item:hover {
    background: #f1f5f9;
    color: #3B82F6;
}

.nav-item.active {
    background: linear-gradient(45deg, #3B82F6, #10B981);
    color: white;
}

.nav-icon {
    margin-right: 0.8rem;
    font-size: 1.2rem;
}

.settings-icon {
    background: rgba(255,255,255,0.2);
    padding: 0.5rem;
    border-radius: 50%;
    cursor: pointer;
    transition: all 0.3s ease;
}

.settings-icon:hover {
    background: rgba(255,255,255,0.3);
    transform: rotate(90deg);
}

/* Enhanced interactive elements */
.stButton > button {
    transition: all 0.3s ease !important;
    font-weight: 500 !important;
}

.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
}

/* Improved metrics styling */
.metric-container {
    background: white;
    padding: 1rem;
    border-radius: 0.8rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    border-left: 4px solid #3B82F6;
    margin-bottom: 1rem;
}

/* Progress bars */
.progress-bar {
    background: #e2e8f0;
    border-radius: 10px;
    height: 12px;
    margin: 10px 0;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    border-radius: 10px;
    transition: width 0.8s ease;
}

/* Status badges */
.status-badge {
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.badge-success {
    background: #10B981;
    color: white;
}

.badge-warning {
    background: #F59E0B;
    color: white;
}

.badge-info {
    background: #3B82F6;
    color: white;
}

/* Enhanced expandables */
.stExpander > div > div > div > p {
    font-weight: 600 !important;
    color: #1e293b !important;
}

/* Hide Streamlit default styling */
.block-container {
    padding-top: 1rem;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* New Features Styling */
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

.bill-split-card {
    background: linear-gradient(135deg, #f8fafc, #e2e8f0);
    padding: 1.5rem;
    border-radius: 1rem;
    border: 1px solid #cbd5e1;
    margin-bottom: 1rem;
}

.feature-nav {
    display: flex;
    gap: 0.8rem;
    margin-bottom: 2rem;
    flex-wrap: wrap;
}

.feature-nav-item {
    background: white;
    padding: 0.8rem 1.5rem;
    border-radius: 2rem;
    border: 2px solid #e2e8f0;
    text-decoration: none;
    color: #64748b;
    font-weight: 600;
    transition: all 0.3s ease;
    cursor: pointer;
}

.feature-nav-item:hover {
    border-color: #3B82F6;
    color: #3B82F6;
    transform: translateY(-2px);
}

.feature-nav-item.active {
    background: linear-gradient(45deg, #3B82F6, #10B981);
    color: white;
    border-color: transparent;
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
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user_id' not in st.session_state:
    st.session_state.user_id = "default_user"
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'user_profile_complete' not in st.session_state:
    st.session_state.user_profile_complete = True  # Skip profile setup
if 'show_app' not in st.session_state:
    st.session_state.show_app = True  # Go directly to app features
if 'current_page' not in st.session_state:
    st.session_state.current_page = "profile"  # Default to profile for logged in users
if 'user_name' not in st.session_state:
    st.session_state.user_name = "User"  # Default name
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
        {"service": "Amazon Prime Student", "discount": "50% off", "savings": "₹4,897/year", "category": "Shopping"},
        {"service": "Microsoft Office 365", "discount": "Free", "savings": "₹8,217/year", "category": "Software"},
        {"service": "Spotify Premium", "discount": "50% off", "savings": "₹4,980/year", "category": "Music"},
        {"service": "Adobe Creative Cloud", "discount": "60% off", "savings": "₹29,880/year", "category": "Software"},
        {"service": "Hulu + Live TV", "discount": "Student rate", "savings": "₹2,905/month", "category": "Streaming"}
    ]

# Initialize components
@st.cache_resource
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

ai_client, nlp_processor, finance_advisor, demographics_manager = initialize_components()

def display_hero_section():
    """Hero section with title, subtitle, and CTA"""
    st.markdown("""
    <div class="main-header">
        <div class="hero-title">SMARTSPENDS</div>
        <div class="hero-subtitle">Your Intelligent Money Companion</div>
        <div class="hero-description">
            Powered by Google Gemini 1.5 Flash with Granite AI fallback, SMARTSPENDS delivers 
            personalized financial advice that adapts to your unique student lifestyle and goals.
        </div>
        <div class="stats-container">
            <div class="stat-item">
                <div class="stat-number">AI</div>
                <div class="stat-label">Powered</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">24/7</div>
                <div class="stat-label">Available</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">100%</div>
                <div class="stat-label">Personalized</div>
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

def display_features_section():
    """Features section with cards"""
    st.markdown('<h2 class="section-title">Smart Features for Smarter Money</h2>', unsafe_allow_html=True)
    
    # Features grid
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
                <div class="feature-icon">{icon}</div>
                <div class="feature-title">{title}</div>
                <div class="feature-description">{description}</div>
            </div>
            """, unsafe_allow_html=True)

def display_why_choose_section():
    """Why choose us section"""
    st.markdown('<h2 class="section-title">Why Choose SMARTSPENDS?</h2>', unsafe_allow_html=True)
    
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
            <div class="why-choose-card">
                <div class="feature-icon">{icon}</div>
                <div class="feature-title">{title}</div>
                <div class="feature-description">{description}</div>
            </div>
            """, unsafe_allow_html=True)

def display_cta_section():
    """Call to action section"""
    st.markdown("""
    <div class="cta-section">
        <div class="cta-title">Plan smarter. Spend better. Save faster.</div>
        <p style="font-size: 1.2rem; opacity: 0.9; margin-bottom: 2rem;">
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

def display_footer():
    """Footer section"""
    st.markdown("""
    <div class="footer">
        <div style="margin-bottom: 1rem;">
            <a href="#" style="margin: 0 1rem; color: #64748b; text-decoration: none;">About</a>
            <a href="#" style="margin: 0 1rem; color: #64748b; text-decoration: none;">Privacy Policy</a>
            <a href="#" style="margin: 0 1rem; color: #64748b; text-decoration: none;">Contact</a>
        </div>
        <div>© 2025 SmartSpends. All rights reserved.</div>
    </div>
    """, unsafe_allow_html=True)

def display_landing_page():
    """Main landing page"""
    display_hero_section()
    
    # Add some spacing
    st.markdown("<br>", unsafe_allow_html=True)
    
    display_features_section()
    
    # Add some spacing
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    display_why_choose_section()
    
    display_cta_section()
    
    display_footer()

def display_profile_page():
    """Professional Profile Page Dashboard"""
    # Get user data
    user_profile = demographics_manager.get_user_profile(st.session_state.user_id)
    user_name = st.session_state.get('user_name', 'User')
    
    # Profile Header with more dynamic content
    current_time = datetime.now()
    if current_time.hour < 12:
        greeting = "Good morning"
    elif current_time.hour < 17:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"
    
    # Profile Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"""
        <div class="profile-header">
            <div style="display: flex; align-items: center;">
                <div class="profile-avatar">
                    {user_name[0].upper()}
                </div>
                <div class="profile-info">
                    <h1 class="profile-name">{greeting}, {user_name}👋</h1>
                    <p class="profile-subtitle">Here's your financial overview for today</p>
                    <div style="display: flex; gap: 15px; margin-top: 10px; font-size: 0.9rem; opacity: 0.8;">
                        <span>📅 {current_time.strftime('%B %d, %Y')}</span>
                        <span>🏦 Last updated: {current_time.strftime('%I:%M %p')}</span>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("⚙️ Settings", key="settings_btn", help="Account settings"):
            st.session_state.show_settings = True
            st.rerun()
            
        if st.button("🔔 Notifications", key="notifications_btn", help="View notifications"):
            st.session_state.show_notifications = True
            st.rerun()
    
    # Financial Summary Cards with improved interactivity
    st.markdown('<h3 style="color: #000000; font-weight: 700; margin-bottom: 1.5rem;">📊 Financial Overview</h3>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("💰 Current Balance", key="balance_card", help="View balance details", use_container_width=True):
            st.session_state.show_balance_details = True
        st.markdown("""
        <div class="dashboard-card">
            <div class="card-header">
                <span class="card-icon">💰</span>
                <h3 class="card-title">Current Balance</h3>
            </div>
            <p class="card-value">₹2,05,485</p>
            <p class="card-change positive-change">+2.5% from last month</p>
            <div style="background: #e2e8f0; border-radius: 10px; height: 8px; margin: 10px 0;">
                <div style="background: linear-gradient(45deg, #10B981, #3B82F6); width: 75%; height: 100%; border-radius: 10px;"></div>
            </div>
            <p style="font-size: 0.8rem; color: #2d3748;">75% of monthly budget</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("📊 Monthly Spending", key="spending_card", help="View spending breakdown", use_container_width=True):
            st.session_state.show_spending_details = True
        st.markdown("""
        <div class="dashboard-card">
            <div class="card-header">
                <span class="card-icon">📊</span>
                <h3 class="card-title">Monthly Spending</h3>
            </div>
            <p class="card-value">₹1,03,975</p>
            <p class="card-change negative-change">+8.3% from last month</p>
            <div style="background: #e2e8f0; border-radius: 10px; height: 8px; margin: 10px 0;">
                <div style="background: linear-gradient(45deg, #EF4444, #F59E0B); width: 62%; height: 100%; border-radius: 10px;"></div>
            </div>
            <p style="font-size: 0.8rem; color: #2d3748;">62% of monthly budget</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if st.button("🎯 Savings Goal", key="savings_card", help="View goal progress", use_container_width=True):
            st.session_state.show_savings_details = True
        st.markdown("""
        <div class="dashboard-card">
            <div class="card-header">
                <span class="card-icon">🎯</span>
                <h3 class="card-title">Savings Goal</h3>
            </div>
            <p class="card-value">72%</p>
            <p class="card-change positive-change">₹29,970 of ₹41,625 goal</p>
            <div style="background: #e2e8f0; border-radius: 10px; height: 8px; margin: 10px 0;">
                <div style="background: linear-gradient(45deg, #10B981, #3B82F6); width: 72%; height: 100%; border-radius: 10px;"></div>
            </div>
            <p style="font-size: 0.8rem; color: #2d3748;">₹11,655 remaining</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        if st.button("📈 Investments", key="investments_card", help="View portfolio details", use_container_width=True):
            st.session_state.show_investment_details = True
        st.markdown("""
        <div class="dashboard-card">
            <div class="card-header">
                <span class="card-icon">📈</span>
                <h3 class="card-title">Investments</h3>
            </div>
            <p class="card-value">₹70,767</p>
            <p class="card-change positive-change">+5.7% portfolio gain</p>
            <div style="background: #e2e8f0; border-radius: 10px; height: 8px; margin: 10px 0;">
                <div style="background: linear-gradient(45deg, #10B981, #3B82F6); width: 85%; height: 100%; border-radius: 10px;"></div>
            </div>
            <p style="font-size: 0.8rem; color: #2d3748;">Portfolio growth: +₹3,763</p>
        </div>
        """, unsafe_allow_html=True)
    

    # Quick Actions Section with enhanced styling
    st.markdown("""
    <div style="margin: 2rem 0 1rem 0;">
        <h3 style="color: #000000; font-weight: 700; margin-bottom: 1.5rem;">⚡ Quick Actions</h3>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("💳 Add Transaction", key="add_transaction", help="Log a new transaction", use_container_width=True):
            st.session_state.show_add_transaction = True
    
    with col2:
        if st.button("📝 Update Budget", key="update_budget", help="Modify your budget", use_container_width=True):
            st.session_state.current_page = "budgets"
            st.rerun()
    
    with col3:
        if st.button("🎯 Set New Goal", key="set_goal", help="Create a financial goal", use_container_width=True):
            st.session_state.current_page = "goals"
            st.rerun()
    
    with col4:
        if st.button("💬 Ask AI", key="ask_ai", help="Get financial advice", use_container_width=True):
            st.session_state.current_page = "chat"
            st.rerun()
    
    # Navigation Menu
    st.markdown("""
    <div class="navigation-menu">
        <h3 style="margin-bottom: 1rem; color: #1e293b;">🧭 Quick Navigation</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Core Features Navigation with enhanced styling
    st.markdown("""
    <div style="margin: 2rem 0 1rem 0;">
        <h3 style="color: #000000; font-weight: 700; margin-bottom: 1.5rem;">🧭 Core Features</h3>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("🏠 Dashboard", key="nav_dashboard", help="Current page", use_container_width=True):
            st.session_state.current_page = "profile"
            st.rerun()
    
    with col2:
        if st.button("💬 AI Chat", key="nav_chat", help="Chat with AI assistant", use_container_width=True):
            st.session_state.current_page = "chat"
            st.rerun()
    
    with col3:
        if st.button("📊 Budgets", key="nav_budgets", help="Budget analysis", use_container_width=True):
            st.session_state.current_page = "budgets"
            st.rerun()
    
    with col4:
        if st.button("🎯 Goals", key="nav_goals", help="Financial goals", use_container_width=True):
            st.session_state.current_page = "goals"
            st.rerun()
    
    with col5:
        if st.button("📈 Insights", key="nav_insights", help="Financial insights", use_container_width=True):
            st.session_state.current_page = "insights"
            st.rerun()
    
    # Student Features Navigation with enhanced styling  
    st.markdown("""
    <div style="margin: 2rem 0 1rem 0;">
        <h3 style="color: #000000; font-weight: 700; margin-bottom: 1.5rem;">✨ Student Features</h3>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💳 Subscriptions", key="nav_subscriptions", help="Track all subscriptions", use_container_width=True):
            st.session_state.current_page = "subscriptions"
            st.rerun()
    
    with col2:
        if st.button("🤝 Bill Splitting", key="nav_bill_split", help="Split bills with friends", use_container_width=True):
            st.session_state.current_page = "bill_split"
            st.rerun()
    
    with col3:
        if st.button("🎓 Student Offers", key="nav_offers", help="Student discounts & offers", use_container_width=True):
            st.session_state.current_page = "student_offers"
            st.rerun()
    
    # Enhanced Financial Insights Section
    st.markdown("""
    <div style="margin: 3rem 0 1rem 0;">
        <h3 style="color: #000000; font-weight: 700; margin-bottom: 1.5rem;">💡 Smart Insights</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Insights cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="dashboard-card" style="background: linear-gradient(135deg, #10B981, #059669); color: white;">
            <div class="card-header">
                <span style="font-size: 1.5rem;">💰</span>
                <h4 style="margin: 0; color: white; font-weight: 600;">Monthly Budget Status</h4>
            </div>
            <p style="font-size: 1.1rem; margin: 0.5rem 0; opacity: 0.9;">You're on track! 75% budget utilized</p>
            <p style="font-size: 0.9rem; margin: 0; opacity: 0.8;">Remaining: ₹68,495 for this month</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="dashboard-card" style="background: linear-gradient(135deg, #3B82F6, #1D4ED8); color: white;">
            <div class="card-header">
                <span style="font-size: 1.5rem;">📈</span>
                <h4 style="margin: 0; color: white; font-weight: 600;">Investment Growth</h4>
            </div>
            <p style="font-size: 1.1rem; margin: 0.5rem 0; opacity: 0.9;">Portfolio up 5.7% this month!</p>
            <p style="font-size: 0.9rem; margin: 0; opacity: 0.8;">Consider increasing SIP by ₹2,000</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Modal popups for detailed views
    if st.session_state.get('show_balance_details', False):
        with st.expander("💰 Balance Details", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Checking Account", "₹1,53,260", "+₹10,417")
                st.metric("Savings Account", "₹53,137", "+₹1,245")
            with col2:
                st.metric("Credit Available", "₹1,24,500", "85% utilization")
                st.metric("Cash on Hand", "₹4,150", "—")
            if st.button("Close", key="close_balance"):
                st.session_state.show_balance_details = False
                st.rerun()
    
    if st.session_state.get('show_spending_details', False):
        with st.expander("📊 Spending Breakdown", expanded=True):
            st.markdown("""
            **Top Categories This Month:**
            - 🍔 Food & Dining: ₹40,272 (39%)
            - 🚗 Transportation: ₹18,272 (18%)
            - 🏠 Housing: ₹24,900 (24%)
            - 🎮 Entertainment: ₹11,823 (11%)
            - 💊 Healthcare: ₹8,300 (8%)
            """)
            if st.button("Close", key="close_spending"):
                st.session_state.show_spending_details = False
                st.rerun()
    
    if st.session_state.get('show_savings_details', False):
        with st.expander("🎯 Savings Goal Progress", expanded=True):
            st.markdown("""
            **Emergency Fund Goal: ₹41,500**
            - Current Progress: ₹29,880 (72%)
            - Monthly Contribution: ₹7,055
            - Estimated Completion: 2 months
            - Last Deposit: ₹2,075 (3 days ago)
            """)
            st.progress(0.72)
            if st.button("Close", key="close_savings"):
                st.session_state.show_savings_details = False
                st.rerun()
    
    if st.session_state.get('show_investment_details', False):
        with st.expander("📈 Investment Portfolio", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Value", "₹70,567", "+₹3,752 (5.7%)")
                st.metric("Monthly Contribution", "₹8,300", "—")
            with col2:
                st.markdown("""
                **Portfolio Allocation:**
                - 📈 S&P 500 Index: 60% (₹42,340)
                - 🌍 International: 25% (₹17,642)
                - 🏦 Bonds: 15% (₹10,585)
                """)
            if st.button("Close", key="close_investments"):
                st.session_state.show_investment_details = False
                st.rerun()
    
    if st.session_state.get('show_add_transaction', False):
        with st.expander("💳 Add New Transaction", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                transaction_type = st.selectbox("Type", ["Expense", "Income"])
                amount = st.number_input("Amount (₹)", min_value=0.01, value=830.00)
            with col2:
                category = st.selectbox("Category", ["Food", "Transportation", "Entertainment", "Healthcare", "Shopping", "Other"])
                description = st.text_input("Description", placeholder="e.g., Lunch at cafe")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Save Transaction", type="primary"):
                    st.success(f"Added {transaction_type.lower()}: ₹{amount:.0f} for {category}")
                    st.session_state.show_add_transaction = False
                    st.rerun()
            with col2:
                if st.button("Cancel", key="cancel_transaction"):
                    st.session_state.show_add_transaction = False
                    st.rerun()
    
    # Handle Settings/Edit Profile
    if st.session_state.get('show_settings', False):
        display_edit_profile_sidebar()

def display_edit_profile_sidebar():
    """Display edit profile functionality in sidebar"""
    with st.sidebar:
        st.header("⚙️ Edit Profile")
        
        # Get current profile data
        user_profile = demographics_manager.get_user_profile(st.session_state.user_id)
        current_name = st.session_state.get('user_name', '')
        
        # Profile form with current values
        user_name = st.text_input("Full Name", value=current_name, key="edit_user_name")
        age = st.number_input("Age", min_value=16, max_value=100, 
                            value=user_profile.get('age', 25) if user_profile else 25, key="edit_age")
        
        occupation = st.selectbox("Occupation Status", [
            "Student", "Professional", "Self-employed", "Retired", "Unemployed", "Other"
        ], index=["student", "professional", "self-employed", "retired", "unemployed", "other"].index(
            user_profile.get('occupation', 'student')) if user_profile else 0, key="edit_occupation")
        
        income = st.number_input("Monthly Income (₹)", min_value=0, 
                               value=user_profile.get('income', 0) if user_profile else 0, 
                               step=1000, key="edit_income")
        
        experience_level = st.selectbox("Financial Experience", [
            "Beginner", "Intermediate", "Advanced"
        ], index=["beginner", "intermediate", "advanced"].index(
            user_profile.get('experience_level', 'beginner')) if user_profile else 0, key="edit_experience")
        
        goals = st.multiselect("Financial Goals", [
            "Build Emergency Fund", "Pay Off Debt", "Save for Retirement",
            "Buy a Home", "Invest in Stocks", "Start a Business",
            "Save for Education", "Plan for Healthcare"
        ], default=user_profile.get('goals', []) if user_profile else [], key="edit_goals")
        
        risk_tolerance = st.selectbox("Risk Tolerance", [
            "Conservative", "Moderate", "Aggressive"
        ], index=["conservative", "moderate", "aggressive"].index(
            user_profile.get('risk_tolerance', 'moderate')) if user_profile else 1, key="edit_risk")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Update Profile", key="update_profile"):
                if user_name.strip():
                    # Update user profile
                    user_data = {
                        'age': age,
                        'occupation': occupation.lower(),
                        'income': income,
                        'experience_level': experience_level.lower(),
                        'goals': goals,
                        'risk_tolerance': risk_tolerance.lower(),
                        'updated_date': datetime.now().isoformat()
                    }
                    
                    demographics_manager.add_user_profile(st.session_state.user_id, user_data)
                    st.session_state.user_name = user_name.strip()
                    st.success("Profile updated successfully!")
                    st.session_state.show_settings = False
                    st.rerun()
                else:
                    st.error("Please enter your full name.")
        
        with col2:
            if st.button("✖️ Cancel", key="cancel_edit"):
                st.session_state.show_settings = False
                st.rerun()

def setup_user_profile():
    """Setup user profile in sidebar"""
    with st.sidebar:
        st.header("👤 User Profile")
        
        # AI Provider Info
        st.subheader("🤖 AI Assistant")
        ai_info = ai_client.get_model_info()
        model_name = ai_info.get('model_name', 'AI Assistant')
        system_type = ai_info.get('system', 'Unknown')
        
        if 'Gemini' in model_name:
            st.success("✅ Gemini AI Ready (Primary)")
            st.info("🔮 Cloud AI • Latest Knowledge • Advanced Reasoning")
        elif 'Granite' in model_name:
            st.success("✅ Granite AI Ready")
            if ai_info.get('initialized', False):
                st.info("🧠 Local AI • Privacy-Focused")
            else:
                st.info("🔧 Rule-Based • Instant Responses")
        else:
            st.warning("⚠️ AI Assistant Loading...")
            
        # Show system status
        with st.expander("🔧 System Status"):
            st.write(ai_client.get_status())
        
        st.divider()
        
        # Basic demographics
        user_name = st.text_input("Full Name", value=st.session_state.get('user_name', ''), placeholder="Enter your full name")
        
        age = st.number_input("Age", min_value=16, max_value=100, value=25)
        
        occupation = st.selectbox("Occupation Status", [
            "Student", "Professional", "Self-employed", "Retired", "Unemployed", "Other"
        ])
        
        income = st.number_input("Monthly Income (₹)", min_value=0, value=0, step=1000)
        
        experience_level = st.selectbox("Financial Experience", [
            "Beginner", "Intermediate", "Advanced"
        ])
        
        goals = st.multiselect("Financial Goals", [
            "Build Emergency Fund", "Pay Off Debt", "Save for Retirement",
            "Buy a Home", "Invest in Stocks", "Start a Business",
            "Save for Education", "Plan for Healthcare"
        ])
        
        risk_tolerance = st.selectbox("Risk Tolerance", [
            "Conservative", "Moderate", "Aggressive"
        ])
        
        if st.button("Save Profile"):
            if user_name.strip():
                # Create user profile
                user_data = {
                    'age': age,
                    'occupation': occupation.lower(),
                    'income': income,
                    'experience_level': experience_level.lower(),
                    'goals': goals,
                    'risk_tolerance': risk_tolerance.lower(),
                    'setup_date': datetime.now().isoformat()
                }
                
                demographics_manager.add_user_profile(st.session_state.user_id, user_data)
                st.session_state.user_name = user_name.strip()
                st.session_state.user_profile_complete = True
                st.success("Profile saved successfully!")
                st.rerun()
            else:
                st.error("Please enter your full name.")

def display_chat_interface():
    """Main chat interface"""
    st.title("💰 SmartSpends-AI - Powered by Gemini & Granite")
    
    # Check if user profile is complete
    user_profile = demographics_manager.get_user_profile(st.session_state.user_id)
    if not user_profile:
        st.info("👈 Please complete your profile in the sidebar to get personalized advice!")
        return
    
    user_type = demographics_manager.determine_user_type(st.session_state.user_id)
    
    # Welcome message with personalization
    welcome_style = demographics_manager.communication_styles.get(user_type, 
                                                                  demographics_manager.communication_styles['general'])
    
    # Get active AI info
    model_info = ai_client.get_model_info()
    active_ai = model_info.get('model_name', 'AI Assistant')
    
    st.markdown(f"""
    ### {welcome_style['greeting']} Welcome to your personalized financial assistant!
    
    I'm powered by **{active_ai}** with smart fallback capabilities. Your financial data is handled securely.
    Based on your profile, I can see you're a **{user_type}** and I'll tailor my advice accordingly.
    
    **What I can help you with:**
    - 📊 Budget analysis and recommendations
    - 💡 Spending insights and optimization
    - 🎯 Goal-based financial planning
    - 📈 Investment guidance
    - 💳 Debt management strategies
    - 🔄 **Dual AI System** - Best of cloud and local AI
    """)

def display_budget_analyzer():
    """Budget analyzer tool"""
    # Budget analyzer page
    
    st.header("📊 Budget Analyzer")
    
    with st.expander("💡 Enter Your Financial Information"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Income")
            monthly_income = st.number_input("Monthly Income (₹)", min_value=0.0, value=0.0, step=1000.0)
            
            st.subheader("Fixed Expenses")
            housing = st.number_input("Housing (rent/mortgage) (₹)", min_value=0.0, value=0.0, step=500.0)
            utilities = st.number_input("Utilities (₹)", min_value=0.0, value=0.0, step=200.0)
            insurance = st.number_input("Insurance (₹)", min_value=0.0, value=0.0, step=200.0)
            debt = st.number_input("Debt Payments (₹)", min_value=0.0, value=0.0, step=200.0)
        
        with col2:
            st.subheader("Variable Expenses")
            food = st.number_input("Food & Groceries (₹)", min_value=0.0, value=0.0, step=200.0)
            transportation = st.number_input("Transportation (₹)", min_value=0.0, value=0.0, step=200.0)
            entertainment = st.number_input("Entertainment (₹)", min_value=0.0, value=0.0, step=200.0)
            healthcare = st.number_input("Healthcare (₹)", min_value=0.0, value=0.0, step=200.0)
            personal = st.number_input("Personal Care (₹)", min_value=0.0, value=0.0, step=200.0)
            savings = st.number_input("Current Savings (₹)", min_value=0.0, value=0.0, step=200.0)
        
        if st.button("Analyze Budget", type="primary"):
            if monthly_income > 0:
                expenses = {
                    'housing': housing,
                    'utilities': utilities,
                    'insurance': insurance,
                    'debt': debt,
                    'food': food,
                    'transportation': transportation,
                    'entertainment': entertainment,
                    'healthcare': healthcare,
                    'personal': personal,
                    'savings': savings
                }
                
                user_type = demographics_manager.determine_user_type(st.session_state.user_id)
                budget_analysis = finance_advisor.generate_comprehensive_budget_summary(
                    monthly_income, expenses, user_type
                )
                
                # Display results
                display_budget_results(budget_analysis)
            else:
                st.error("Please enter your monthly income to analyze your budget.")

def display_budget_results(budget_analysis):
    """Display budget analysis results"""
    overview = budget_analysis['overview']
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Monthly Income", f"₹{overview['total_income']:,.0f}")
    with col2:
        st.metric("Total Expenses", f"₹{overview['total_expenses']:,.0f}")
    with col3:
        savings_color = "normal" if overview['net_savings'] >= 0 else "inverse"
        st.metric("Net Savings", f"₹{overview['net_savings']:,.0f}", delta_color=savings_color)
    with col4:
        st.metric("Savings Rate", f"{overview['savings_rate']:.1f}%")
    
    # Financial Health Score
    health_score = budget_analysis['financial_health_score']
    st.subheader(f"Financial Health Score: {health_score['score']}/100 ({health_score['rating']})")
    
    progress_color = "green" if health_score['score'] >= 80 else "orange" if health_score['score'] >= 60 else "red"
    st.progress(health_score['score'] / 100)
    
    # Analysis and recommendations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Budget Analysis")
        analysis = budget_analysis['budget_analysis']
        
        if analysis['positive_aspects']:
            st.success("✅ What you're doing well:")
            for aspect in analysis['positive_aspects']:
                st.write(f"• {aspect}")
        
        if analysis['areas_for_improvement']:
            st.warning("⚠️ Areas for improvement:")
            for area in analysis['areas_for_improvement']:
                st.write(f"• {area}")
    
    with col2:
        st.subheader("💡 Recommendations")
        recommendations = budget_analysis['recommendations']
        
        for i, rec in enumerate(recommendations[:8], 1):  # Show top 8 recommendations
            st.write(f"{i}. {rec}")

def display_chat_history():
    """Display conversation history"""
    if st.session_state.conversation_history:
        st.subheader("💬 Conversation History")
        
        for i, (question, answer) in enumerate(reversed(st.session_state.conversation_history[-5:])):
            with st.expander(f"Q: {question[:50]}..." if len(question) > 50 else f"Q: {question}"):
                st.write("**You:** " + question)
                st.write("**Assistant:** " + answer)

def main():
    """Main application function"""
    # Check if user wants to see the app or landing page
    if not st.session_state.show_app:
        # Show landing page
        display_landing_page()
        return
    
    # Check if user profile is complete
    if not st.session_state.user_profile_complete:
        # Show profile setup in sidebar
        setup_user_profile()
        # Profile setup without back button
        
        st.markdown("---")
        st.info("👈 Please complete your profile to access your dashboard!")
        return
    
    # User is logged in and profile is complete - show the appropriate page
    current_page = st.session_state.get('current_page', 'profile')
    
    # Top navigation bar
    st.markdown("""
    <div style="background: white; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem; 
                box-shadow: 0 2px 8px rgba(0,0,0,0.1); display: flex; justify-content: space-between; align-items: center;">
        <div style="font-size: 1.5rem; font-weight: 700; color: #3B82F6;">SMARTSPENDS</div>
        <div style="font-size: 0.9rem; color: #64748b;">Personal Finance Dashboard</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display the appropriate page based on current_page
    if current_page == "profile":
        display_profile_page()
    elif current_page == "chat":
        display_chat_page()
    elif current_page == "budgets":
        display_budget_analyzer()
    elif current_page == "goals":
        display_goals_page()
    elif current_page == "insights":
        display_insights_page()
    elif current_page == "subscriptions":
        display_subscriptions_page()
    elif current_page == "bill_split":
        display_bill_split_page()
    elif current_page == "student_offers":
        display_student_offers_page()
    else:
        # Default to profile page
        st.session_state.current_page = "profile"
        display_profile_page()
    
    # Add profile edit option in sidebar
    with st.sidebar:
        st.markdown("---")
        if st.button("👤 Edit Profile", key="edit_profile"):
            st.session_state.user_profile_complete = False
            st.rerun()

# Additional page functions
def display_chat_page():
    """Chat interface page"""
    # Chat interface page
    
    st.markdown("# 💬 SmartSpends-AI Assistant")
    
    with st.sidebar:
        st.success("✅ Profile Complete")
        
        # AI Provider Info
        st.subheader("🤖 AI Assistant")
        ai_info = ai_client.get_model_info()
        model_name = ai_info.get('model_name', 'AI Assistant')
        
        if 'Gemini' in model_name:
            st.success("✅ Gemini AI Active")
            st.info("🔮 Cloud AI • Latest Knowledge • Advanced Reasoning")
        elif 'Granite' in model_name:
            st.success("✅ Granite AI Active")
            if ai_info.get('initialized', False):
                st.info("🧠 Local AI • Privacy-Focused")
            else:
                st.info("🔧 Rule-Based • Instant Responses")
        else:
            st.warning("⚠️ AI System Loading...")
            
        # Show system status
        with st.expander("🔧 System Status"):
            st.write(ai_client.get_status())
        
        st.divider()
        
        # User profile info
        user_profile = demographics_manager.get_user_profile(st.session_state.user_id)
        user_type = demographics_manager.determine_user_type(st.session_state.user_id)
        
        st.write(f"**User Type:** {user_type.title()}")
        st.write(f"**Age:** {user_profile.get('age', 'N/A')}")
        st.write(f"**Occupation:** {user_profile.get('occupation', 'N/A').title()}")
    
    # Chat interface
    display_chat_interface()
    
    # Chat input
    user_input = st.text_input("Ask me about your finances:", placeholder="e.g., How can I save more money this month?")
    
    col1, col2, col3 = st.columns([1, 1, 4])
    
    with col1:
        send_button = st.button("Send", type="primary")
    with col2:
        clear_button = st.button("Clear Chat")
    with col3:
        if st.button("🔄 Reset AI"):
            st.cache_resource.clear()
            st.session_state.clear()
            st.success("AI system reset! Please refresh the page.")
            st.rerun()
    
    if clear_button:
        st.session_state.conversation_history = []
        st.rerun()
    
    if send_button and user_input:
        with st.spinner("🤖 AI is thinking..."):
            try:
                # Validate input
                if len(user_input.strip()) == 0:
                    st.warning("Please enter a question!")
                    return
                
                # Debug: Show what we're processing
                if os.getenv('DEBUG_MODE', 'False').lower() == 'true':
                    st.info(f"🔍 Processing: '{user_input}'")
                
                # Process input with NLP
                nlp_result = nlp_processor.process_input(user_input)
                
                # Get user profile for personalized response
                user_profile = demographics_manager.get_user_profile(st.session_state.user_id)
                user_type = demographics_manager.determine_user_type(st.session_state.user_id)
                
                # Debug: Show user context
                if os.getenv('DEBUG_MODE', 'False').lower() == 'true':
                    st.info(f"👤 User Type: {user_type}")
                
                # Create enhanced user context for AI
                user_context = {**user_profile, 'user_type': user_type}
                
                # Test AI connection before using
                connections = ai_client.test_connections()
                if not any(connections.values()):
                    st.error("❌ AI services are currently unavailable. Please try again in a moment.")
                    return
                
                # Generate response using Dual AI (Gemini + Granite)
                response = ai_client.get_response(user_input, user_context)
                
                # Debug: Show raw response
                if os.getenv('DEBUG_MODE', 'False').lower() == 'true':
                    st.info(f"🤖 Raw Response ({len(response)} chars): {response[:100]}...")
                
                # Check for error responses
                if "I'm having trouble processing your request" in response:
                    st.error("🔄 The AI encountered an issue. Let me try a different approach...")
                    
                    # Force switch to Granite and retry
                    ai_client.switch_to_granite()
                    response = ai_client.get_response(user_input, user_context)
                    
                elif "Sorry, I'm currently unavailable" in response:
                    st.warning("⚠️ Primary AI is temporarily unavailable, using backup system...")
                
                # Adapt response for user demographics
                adapted_response = demographics_manager.adapt_communication_style(
                    st.session_state.user_id, response
                )
                
                # Store in conversation history
                st.session_state.conversation_history.append((user_input, adapted_response))
                
                # Display response immediately
                st.success("💡 **AI Financial Assistant Response:**")
                st.write(adapted_response)
                
                # Show AI system used
                model_info = ai_client.get_model_info()
                active_ai = model_info.get('model_name', 'AI Assistant')
                st.caption(f"Response generated by: {active_ai}")
                
                # Show intent and confidence if in debug mode
                if os.getenv('DEBUG_MODE', 'False').lower() == 'true':
                    with st.expander("🔍 Full Debug Info"):
                        st.json({
                            "nlp_result": nlp_result,
                            "user_context": user_context,
                            "connections": connections,
                            "model_info": model_info,
                            "response_length": len(response)
                        })
                
            except Exception as e:
                st.error(f"❌ System Error: {str(e)}")
                st.info("🔄 Please try your question again. If the issue persists, try refreshing the page.")
                
                # Debug: Show full error
                if os.getenv('DEBUG_MODE', 'False').lower() == 'true':
                    import traceback
                    st.code(traceback.format_exc())
    
    # Display recent chat history
    display_chat_history()

def display_goals_page():
    """Goals management page"""
    # Goals management page
    
    st.markdown("# 🎯 Financial Goals")
    
    # Quick stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Active Goals", "4", "2 new this month")
    with col2:
        st.metric("Goals Achieved", "2", "+1 this quarter")
    with col3:
        st.metric("Total Target", "$25,450", "87% progress")
    
    st.markdown("---")
    
    # Emergency Fund Goal
    st.markdown("### 🏠 Emergency Fund")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("""
        <div class="dashboard-card">
            <h4>Emergency Fund Goal</h4>
            <p><strong>Target:</strong> ₹4,15,000 • <strong>Current:</strong> ₹2,98,800 (72%)</p>
            <div style="background: #e2e8f0; border-radius: 10px; height: 12px; margin: 10px 0;">
                <div style="background: linear-gradient(45deg, #10B981, #3B82F6); width: 72%; height: 100%; border-radius: 10px;"></div>
            </div>
            <p style="color: #10B981;"><strong>✅ On track!</strong> Estimated completion: 3 months</p>
            <div style="display: flex; gap: 15px; margin-top: 10px; font-size: 0.9rem;">
                <span>💰 Monthly contribution: $200</span>
                <span>📅 Started: January 2024</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        if st.button("💰 Add to Goal", key="add_emergency", use_container_width=True):
            st.session_state.show_add_to_emergency = True
        if st.button("📊 View Details", key="emergency_details", use_container_width=True):
            st.session_state.show_emergency_details = True
    
    # Student Loan Goal
    st.markdown("### 🎓 Student Loan Payoff")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("""
        <div class="dashboard-card">
            <h4>Student Loan Elimination</h4>
            <p><strong>Remaining:</strong> ₹10,33,350 • <strong>Original:</strong> ₹18,67,500</p>
            <div style="background: #e2e8f0; border-radius: 10px; height: 12px; margin: 10px 0;">
                <div style="background: linear-gradient(45deg, #EF4444, #F59E0B); width: 45%; height: 100%; border-radius: 10px;"></div>
            </div>
            <p style="color: #F59E0B;"><strong>45% Complete</strong> • Estimated payoff: 4 years</p>
            <div style="display: flex; gap: 15px; margin-top: 10px; font-size: 0.9rem;">
                <span>💳 Monthly payment: $285</span>
                <span>📈 Interest rate: 4.5%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        if st.button("💰 Extra Payment", key="extra_loan", use_container_width=True):
            st.session_state.show_extra_payment = True
        if st.button("📊 Amortization", key="loan_schedule", use_container_width=True):
            st.session_state.show_loan_schedule = True
    
    # New Car Goal
    st.markdown("### 🚗 New Car Fund")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("""
        <div class="dashboard-card">
            <h4>Reliable Transportation Goal</h4>
            <p><strong>Target:</strong> ₹6,64,000 • <strong>Current:</strong> ₹99,600 (15%)</p>
            <div style="background: #e2e8f0; border-radius: 10px; height: 12px; margin: 10px 0;">
                <div style="background: linear-gradient(45deg, #3B82F6, #8B5CF6); width: 15%; height: 100%; border-radius: 10px;"></div>
            </div>
            <p style="color: #3B82F6;"><strong>Just started</strong> • Target date: December 2025</p>
            <div style="display: flex; gap: 15px; margin-top: 10px; font-size: 0.9rem;">
                <span>💰 Monthly target: $150</span>
                <span>🎯 Priority: Medium</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        if st.button("💰 Contribute", key="add_car", use_container_width=True):
            st.session_state.show_add_to_car = True
        if st.button("🚗 Adjust Goal", key="car_details", use_container_width=True):
            st.session_state.show_car_details = True
    
    # Add New Goal Button
    st.markdown("---")
    if st.button("➕ Create New Goal", key="new_goal", help="Set up a new financial goal"):
        st.session_state.show_new_goal = True
    
    # Goal creation modal
    if st.session_state.get('show_new_goal', False):
        with st.expander("➕ Create New Financial Goal", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                goal_name = st.text_input("Goal Name", placeholder="e.g., Vacation Fund")
                target_amount = st.number_input("Target Amount (₹)", min_value=8300, value=83000, step=8300)
                priority = st.selectbox("Priority", ["High", "Medium", "Low"])
            with col2:
                target_date = st.date_input("Target Date")
                monthly_contribution = st.number_input("Monthly Contribution (₹)", min_value=830, value=4150, step=830)
                category = st.selectbox("Category", ["Emergency", "Education", "Travel", "Housing", "Transportation", "Investment", "Other"])
            
            goal_description = st.text_area("Description (optional)", placeholder="Why is this goal important to you?")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Create Goal", type="primary"):
                    st.success(f"Created new goal: {goal_name} (₹{target_amount:,.0f})")
                    st.session_state.show_new_goal = False
                    st.rerun()
            with col2:
                if st.button("Cancel", key="cancel_goal"):
                    st.session_state.show_new_goal = False
                    st.rerun()

def display_insights_page():
    """Financial insights page"""
    # Financial insights page
    
    st.markdown("# 📈 Financial Insights")
    
    user_profile = demographics_manager.get_user_profile(st.session_state.user_id)
    if user_profile:
        user_type = demographics_manager.determine_user_type(st.session_state.user_id)
        
        # Personalized recommendations
        st.subheader("🎯 Personalized Recommendations")
        recommendations = demographics_manager.get_personalized_recommendations(st.session_state.user_id)
        
        for i, rec in enumerate(recommendations, 1):
            st.write(f"{i}. {rec}")
        
        # Financial education based on user type
        st.subheader("📚 Learning Resources")
        
        if user_type == "student":
            st.info("""
            **Student Financial Tips:**
            - Learn about compound interest early
            - Take advantage of student discounts
            - Start building credit responsibly
            - Use free educational resources
            """)
        elif user_type == "professional":
            st.info("""
            **Professional Financial Strategies:**
            - Maximize employer benefits (401k match, HSA)
            - Consider tax optimization strategies
            - Review and adjust investment portfolio
            - Plan for major life events
            """)
        elif user_type == "young_adult":
            st.info("""
            **Young Adult Financial Priorities:**
            - Build emergency fund (3-6 months expenses)
            - Establish good credit history
            - Start investing for long-term goals
            - Consider term life insurance
            """)
    else:
        st.info("Complete your profile to see personalized insights!")

def display_subscriptions_page():
    """Subscription tracking page"""
    # Subscription tracking page
    
    st.markdown("# 💳 Subscription Manager")
    st.markdown("Track and manage all your subscriptions in one place")
    
    # Overview metrics
    total_monthly = sum(sub['cost'] for sub in st.session_state.subscriptions)
    total_yearly = total_monthly * 12
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Active Subscriptions", len(st.session_state.subscriptions))
    with col2:
        st.metric("Monthly Total", f"₹{total_monthly:.0f}")
    with col3:
        st.metric("Yearly Estimate", f"₹{total_yearly:.0f}")
    with col4:
        upcoming_bills = sum(1 for sub in st.session_state.subscriptions if sub['next_billing'] <= "2024-02-10")
        st.metric("Bills Due Soon", upcoming_bills, "Next 7 days")
    
    st.markdown("---")
    
    # Add new subscription
    with st.expander("➕ Add New Subscription"):
        col1, col2 = st.columns(2)
        with col1:
            sub_name = st.text_input("Service Name", placeholder="e.g., Netflix")
            sub_cost = st.number_input("Monthly Cost (₹)", min_value=0.01, value=830.00, step=1.00)
        with col2:
            sub_category = st.selectbox("Category", ["Entertainment", "Software", "Health", "Education", "Shopping", "Other"])
            sub_billing = st.date_input("Next Billing Date")
        
        if st.button("Add Subscription", type="primary"):
            new_sub = {
                "name": sub_name,
                "cost": sub_cost,
                "category": sub_category,
                "next_billing": sub_billing.strftime("%Y-%m-%d")
            }
            st.session_state.subscriptions.append(new_sub)
            st.success(f"Added {sub_name} subscription!")
            st.rerun()
    
    # Display subscriptions by category
    st.markdown("### 📊 Your Subscriptions")
    
    categories = {}
    for sub in st.session_state.subscriptions:
        if sub['category'] not in categories:
            categories[sub['category']] = []
        categories[sub['category']].append(sub)
    
    for category, subs in categories.items():
        st.markdown(f"#### {category}")
        for i, sub in enumerate(subs):
            st.markdown(f"""
            <div class="subscription-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h4 style="margin: 0; color: #1e293b;">{sub['name']}</h4>
                        <p style="margin: 0.2rem 0; color: #64748b;">Next billing: {sub['next_billing']}</p>
                        <span class="category-tag">{sub['category']}</span>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 1.5rem; font-weight: 700; color: #3B82F6;">₹{sub['cost']:.0f}</div>
                        <div style="font-size: 0.8rem; color: #64748b;">per month</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 1, 3])
            with col1:
                if st.button("✏️ Edit", key=f"edit_{category}_{i}"):
                    st.info("Edit functionality coming soon!")
            with col2:
                if st.button("🗑️ Cancel", key=f"cancel_{category}_{i}"):
                    st.session_state.subscriptions.remove(sub)
                    st.rerun()

def display_bill_split_page():
    """Bill splitting page"""
    # Bill splitting page
    
    st.markdown("# 🤝 Bill Splitting Made Easy")
    st.markdown("Split expenses with friends and track who owes what")
    
    # Quick stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Active Splits", len(st.session_state.bill_splits))
    with col2:
        total_owed = sum(split.get('your_share', 0) for split in st.session_state.bill_splits if not split.get('settled', False))
        st.metric("You Owe", f"₹{total_owed:.0f}")
    with col3:
        total_owed_to_you = sum(split.get('others_owe', 0) for split in st.session_state.bill_splits if not split.get('settled', False))
        st.metric("Owed to You", f"₹{total_owed_to_you:.0f}")
    
    st.markdown("---")
    
    # Create new bill split
    with st.expander("➕ Split a New Bill"):
        st.markdown("### Bill Details")
        col1, col2 = st.columns(2)
        with col1:
            bill_name = st.text_input("Bill Description", placeholder="e.g., Dinner at Restaurant")
            total_amount = st.number_input("Total Amount (₹)", min_value=1, value=4150, step=50)
            split_type = st.selectbox("Split Type", ["Equal Split", "Custom Amounts", "Percentage Based"])
        with col2:
            your_name = st.text_input("Your Name", value=st.session_state.get('user_name', 'User'))
            friends = st.text_area("Friends (one per line)", placeholder="Alice\nBob\nCharlie")
            date_of_bill = st.date_input("Date", value=datetime.now().date())
        
        if friends and total_amount > 0:
            friend_list = [f.strip() for f in friends.split('\n') if f.strip()]
            total_people = len(friend_list) + 1  # +1 for user
            
            if split_type == "Equal Split":
                per_person = total_amount / total_people
                st.info(f"Each person pays: ₹{per_person:.0f}")
                
                if st.button("Create Split", type="primary"):
                    new_split = {
                        "bill_name": bill_name,
                        "total_amount": total_amount,
                        "your_share": per_person,
                        "others_owe": per_person * (total_people - 1),
                        "friends": friend_list,
                        "date": date_of_bill.strftime("%Y-%m-%d"),
                        "settled": False,
                        "split_type": "equal"
                    }
                    st.session_state.bill_splits.append(new_split)
                    st.success(f"Created bill split for {bill_name}!")
                    st.rerun()
    
    # Display active bill splits
    if st.session_state.bill_splits:
        st.markdown("### 📋 Active Bill Splits")
        
        for i, split in enumerate(st.session_state.bill_splits):
            status_color = "#10B981" if split.get('settled', False) else "#F59E0B"
            status_text = "✅ Settled" if split.get('settled', False) else "⏳ Pending"
            
            st.markdown(f"""
            <div class="bill-split-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <div>
                        <h4 style="margin: 0; color: #1e293b;">{split['bill_name']}</h4>
                        <p style="margin: 0.2rem 0; color: #64748b;">Date: {split['date']}</p>
                    </div>
                    <div style="color: {status_color}; font-weight: 600;">{status_text}</div>
                </div>
                <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                    <div class="split-amount">Total: ₹{split['total_amount']:.0f}</div>
                    <div class="split-amount">Your Share: ₹{split['your_share']:.0f}</div>
                </div>
                <div style="margin-top: 1rem;">
                    <strong>Friends:</strong> {', '.join(split['friends'])}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 1, 3])
            with col1:
                if not split.get('settled', False):
                    if st.button("✅ Mark Settled", key=f"settle_{i}"):
                        st.session_state.bill_splits[i]['settled'] = True
                        st.rerun()
            with col2:
                if st.button("📤 Share", key=f"share_{i}"):
                    st.info("Share link: sharing functionality coming soon!")
    else:
        st.info("No bill splits yet. Create your first one above!")

def display_student_offers_page():
    """Student discounts and offers page"""
    # Student discounts and offers page
    
    st.markdown("# 🎓 Student Discounts & Offers")
    st.markdown("Save money with exclusive student deals and discounts")
    
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
    
    st.markdown("---")
    
    # Filter by category
    st.markdown("### 🔍 Filter Offers")
    categories = ["All"] + list(set(offer['category'] for offer in st.session_state.student_offers))
    selected_category = st.selectbox("Filter by Category", categories)
    
    # Display offers
    st.markdown("### 💰 Available Offers")
    
    filtered_offers = st.session_state.student_offers if selected_category == "All" else [
        offer for offer in st.session_state.student_offers if offer['category'] == selected_category
    ]
    
    for offer in filtered_offers:
        st.markdown(f"""
        <div class="offer-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h3 style="margin: 0; color: white;">{offer['service']}</h3>
                    <p style="margin: 0.5rem 0; opacity: 0.9;">{offer['discount']}</p>
                    <span style="background: rgba(255,255,255,0.2); padding: 0.2rem 0.6rem; border-radius: 1rem; font-size: 0.8rem;">
                        {offer['category']}
                    </span>
                </div>
                <div style="text-align: right;">
                    <div class="savings-highlight">{offer['savings']}</div>
                    <div style="font-size: 0.8rem; opacity: 0.8; margin-top: 0.3rem;">savings</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 3])
        with col1:
            if st.button("🔗 Get Offer", key=f"get_{offer['service'].replace(' ', '_')}"):
                st.success(f"Redirecting to {offer['service']} student portal...")
        with col2:
            if st.button("ℹ️ Learn More", key=f"info_{offer['service'].replace(' ', '_')}"):
                st.info(f"Learn more about {offer['service']} student benefits")
    
    # Add custom student tip
    st.markdown("---")
    st.markdown("### 💡 Student Money-Saving Tips")
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f0f9ff, #e0f2fe); padding: 1.5rem; border-radius: 1rem; border-left: 4px solid #3B82F6;">
        <h4 style="color: #1e293b; margin-top: 0;">Pro Tips for Students</h4>
        <ul style="color: #64748b; line-height: 1.6;">
            <li><strong>Always verify your student status:</strong> Keep your .edu email active</li>
            <li><strong>Stack discounts:</strong> Combine student discounts with promo codes</li>
            <li><strong>Set reminders:</strong> Many student discounts expire annually</li>
            <li><strong>Share with friends:</strong> Some offers work for group purchases</li>
            <li><strong>Read the fine print:</strong> Understand renewal terms and conditions</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()