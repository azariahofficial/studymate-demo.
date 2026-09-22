import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import re
from datetime import date, timedelta

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Configure client to use Gemini via OpenAI-compatible endpoint
client = OpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Page configuration
st.set_page_config(
    page_title="StudyMate | AI Academic Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== CUSTOM CSS =====
st.markdown("""
<style>
    /* Main container styling */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #6B7280;
        margin-top: 0;
        margin-bottom: 2rem;
    }
    
    /* Task card styling */
    .task-card {
        background: linear-gradient(135deg, #F3F4F6 0%, #FFFFFF 100%);
        border-left: 5px solid #3B82F6;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .task-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .task-number {
        display: inline-block;
        background: #3B82F6;
        color: white;
        width: 28px;
        height: 28px;
        line-height: 28px;
        text-align: center;
        border-radius: 50%;
        font-weight: 600;
        font-size: 0.85rem;
        margin-right: 0.8rem;
    }
    .task-desc {
        font-weight: 600;
        color: #1F2937;
        font-size: 1rem;
    }
    .task-hours {
        float: right;
        background: #DBEAFE;
        color: #1E40AF;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    
    /* Metric card styling */
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border-top: 4px solid #3B82F6;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin: 0.3rem 0;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Schedule box */
    .schedule-box {
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
        border-radius: 10px;
        padding: 1.5rem;
        border-left: 5px solid #3B82F6;
    }
    
    /* Success message */
    .success-banner {
        background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
        border-left: 5px solid #10B981;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        font-weight: 600;
        color: #065F46;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1E3A8A 0%, #1E40AF 100%);
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #3B82F6 0%, #1E40AF 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.7rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ===== SIDEBAR =====
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <div style="font-size: 3rem;">📚</div>
        <h2 style="margin: 0.5rem 0; color: white;">StudyMate</h2>
        <p style="font-size: 0.85rem; opacity: 0.8;">AI-Powered Academic Assistant</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    ### 🎯 Core Features
    - **Smart Task Decomposition**
    - **Personalized Study Plans**
    - **Adaptive Reminders**
    - **Progress Tracking**
    """)
    
    st.markdown("---")
    
    st.markdown("""
    ### 🧠 Powered By
    - Google Gemini AI
    - Natural Language Processing
    - Machine Learning
    """)
    
    st.markdown("---")
    st.caption("CSC 401 Project | 2026")
    st.caption("Design and Implementation of an AI-Powered Academic Assistant")

# ===== MAIN CONTENT =====
st.markdown('<h1 class="main-header">📚 StudyMate</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Transform your assignments into actionable study plans with AI</p>', unsafe_allow_html=True)

# Create tabs
tab1, tab2, tab3 = st.tabs(["🚀 Decompose Assignment", "📊 My Progress", "ℹ️ About"])

# ===== TAB 1: DECOMPOSE =====
with tab1:
    st.markdown("### Step 1: Enter Your Assignment")
    st.markdown("Paste your assignment description below and let StudyMate break it down for you.")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        assignment_description = st.text_area(
            "Assignment Description",
            placeholder="Example: Write a 10-page research paper on the effects of social media on adolescent mental health. Include at least 15 academic sources, a literature review, methodology, findings, and conclusion.",
            height=180,
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown("**Due Date**")
        due_date = st.date_input("Due Date", value=date.today() + timedelta(days=14), label_visibility="collapsed")
        st.markdown("**Difficulty**")
        difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"], label_visibility="collapsed")
    
    st.markdown("")
    
    if st.button("🔍 Decompose Assignment", type="primary", use_container_width=True):
        if not assignment_description:
            st.error("⚠️ Please enter an assignment description.")
        elif not API_KEY:
            st.error("⚠️ API key not found. Please check your configuration.")
        else:
            with st.spinner("🧠 StudyMate is analyzing your assignment..."):
                try:
                    prompt = f"""
                    You are an academic assistant helping students plan their work.
                    
                    Decompose the following assignment into 5 to 8 manageable subtasks.
                    For each subtask, provide a clear description and an estimated number of hours to complete it.
                    
                    Assignment: {assignment_description}
                    Due Date: {due_date}
                    Difficulty: {difficulty}
                    
                    Return ONLY a valid JSON array. Do not include any text before or after the JSON.
                    Do not include line breaks inside the description strings.
                    
                    Format:
                    [
                        {{"description": "Task description here", "estimated_hours": 3}},
                        {{"description": "Another task here", "estimated_hours": 2}}
                    ]
                    """
                    
                    response = client.chat.completions.create(
                        model="gemini-3.6-flash",
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=1000
                    )
                    
                    content = response.choices[0].message.content
                    
                    start_idx = content.find('[')
                    end_idx = content.rfind(']') + 1
                    
                    if start_idx == -1 or end_idx == 0:
                        st.error("Could not parse the response. Please try again.")
                        st.text(content)
                    else:
                        json_str = content[start_idx:end_idx]
                        json_str = re.sub(r'[\x00-\x1f\x7f-\x9f]', ' ', json_str)
                        subtasks = json.loads(json_str, strict=False)
                        
                        # Success banner
                        st.markdown("""
                        <div class="success-banner">
                            ✅ Assignment decomposed successfully! Here is your personalized study plan.
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Metrics row
                        total_hours = sum(task['estimated_hours'] for task in subtasks)
                        days_until_due = (due_date - date.today()).days
                        
                        m1, m2, m3 = st.columns(3)
                        with m1:
                            st.markdown(f"""
                            <div class="metric-card">
                                <div class="metric-label">Total Subtasks</div>
                                <div class="metric-value">{len(subtasks)}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        with m2:
                            st.markdown(f"""
                            <div class="metric-card">
                                <div class="metric-label">Total Hours</div>
                                <div class="metric-value">{total_hours}h</div>
                            </div>
                            """, unsafe_allow_html=True)
                        with m3:
                            st.markdown(f"""
                            <div class="metric-card">
                                <div class="metric-label">Days Until Due</div>
                                <div class="metric-value">{days_until_due}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.markdown("### 📋 Your Study Plan")
                        
                        # Display subtasks as cards
                        for i, task in enumerate(subtasks, 1):
                            st.markdown(f"""
                            <div class="task-card">
                                <span class="task-hours">{task['estimated_hours']}h</span>
                                <span class="task-number">{i}</span>
                                <span class="task-desc">{task['description']}</span>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Schedule recommendation
                        st.markdown("### 📅 Recommended Schedule")
                        if days_until_due > 0:
                            hours_per_day = total_hours / days_until_due
                            st.markdown(f"""
                            <div class="schedule-box">
                                <h4 style="margin-top: 0; color: #1E3A8A;">Your Daily Study Plan</h4>
                                <p style="font-size: 1.1rem; margin-bottom: 0.5rem;">
                                    With <strong>{total_hours} total hours</strong> and <strong>{days_until_due} days</strong> available, 
                                    aim for <strong>{hours_per_day:.1f} hours per day</strong>.
                                </p>
                                <p style="margin-bottom: 0; color: #4B5563;">
                                    💡 <em>Tip: Break this into focused sessions of 45-60 minutes with short breaks in between.</em>
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.warning("The due date has passed. Please select a future date.")
                        
                except json.JSONDecodeError as e:
                    st.error(f"Failed to parse AI response: {e}")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

# ===== TAB 2: PROGRESS =====
with tab2:
    st.markdown("### 📊 Your Progress Dashboard")
    st.info("This section will display your progress tracking, including completed tasks and study statistics. Available after you create your first study plan.")
    
    # Placeholder metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Active Plans</div>
            <div class="metric-value">0</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Tasks Completed</div>
            <div class="metric-value">0</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Hours Studied</div>
            <div class="metric-value">0</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">On-Time Rate</div>
            <div class="metric-value">--</div>
        </div>
        """, unsafe_allow_html=True)

# ===== TAB 3: ABOUT =====
with tab3:
    st.markdown("### ℹ️ About StudyMate")
    st.markdown("""
    **StudyMate** is an AI-powered academic assistant designed to help university students manage their academic tasks more effectively.
    
    #### 🎯 The Problem
    University students struggle to break down complex assignments into manageable tasks. Existing tools like Trello, MyStudyLife, and Canvas are passive—they require students to do the planning themselves.
    
    #### 💡 The Solution
    StudyMate uses artificial intelligence to:
    - **Automatically decompose** assignments into actionable subtasks with time estimates
    - **Learn from your behavior** to personalize future recommendations
    - **Adapt study plans** based on your progress and changing circumstances
    
    #### 🧠 AI Components
    | Component | Technology | Purpose |
    |-----------|-----------|---------|
    | Task Decomposition | Google Gemini AI | Break down complex assignments |
    | Memory System | PostgreSQL + Redis | Store user preferences and habits |
    | Adaptive Planning | Reinforcement-like adaptation | Adjust schedules based on behavior |
    | Chat Interface | Natural Language Processing | Conversational interaction |
    
    #### 🛠️ Technology Stack
    - **Frontend:** React.js, Next.js
    - **Backend:** Python, FastAPI
    - **Database:** PostgreSQL, Redis
    - **AI:** Google Gemini, LangChain
    - **Deployment:** Vercel, Heroku
    
    #### 📚 References
    This project builds upon research in self-regulated learning theory, cognitive load theory, and personalized learning. Key references include Broadbent & Poon (2015), Sweller (1988), and Zimmerman (2002).
    """)
    
    st.markdown("---")
    st.caption("CSC 401 Project | Design and Implementation of an AI-Powered Academic Assistant | 2026")

# ===== FOOTER =====
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #9CA3AF; font-size: 0.85rem;">
    StudyMate v1.0 | CSC 401 Project | Powered by Google Gemini AI
</div>
""", unsafe_allow_html=True)
