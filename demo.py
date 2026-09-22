import streamlit as st
from dotenv import load_dotenv
import os
import json
import re
import requests
from datetime import date

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Page configuration
st.set_page_config(
    page_title="StudyMate Demo",
    page_icon="",
    layout="wide"
)

# Title
st.title("📚 StudyMate")
st.subheader("AI-Powered Academic Assistant")
st.markdown("---")

# Assignment Input Section
st.header("Step 1: Enter Your Assignment")

col1, col2 = st.columns([2, 1])

with col1:
    assignment_description = st.text_area(
        "Assignment Description",
        placeholder="Paste your assignment instructions here...",
        height=200
    )

with col2:
    due_date = st.date_input("Due Date")
    difficulty = st.selectbox(
        "Difficulty Level",
        ["Easy", "Medium", "Hard"]
    )

# Decompose Button
if st.button("🔍 Decompose Assignment", type="primary", use_container_width=True):
    if not assignment_description:
        st.error("⚠️ Please enter an assignment description.")
    elif not API_KEY:
        st.error("⚠️ API key not found. Please check your secrets.")
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
                
                # Build the URL with the API key as a query parameter
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key={API_KEY}"
                
                headers = {
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "contents": [{
                        "parts": [{
                            "text": prompt
                        }]
                    }]
                }
                
                # Make the API call
                response = requests.post(url, headers=headers, json=payload)
                
                if response.status_code != 200:
                    st.error(f"API Error ({response.status_code}): {response.text}")
                else:
                    data = response.json()
                    content = data['candidates'][0]['content']['parts'][0]['text']
                    
                    # Extract JSON from response
                    start_idx = content.find('[')
                    end_idx = content.rfind(']') + 1
                    
                    if start_idx == -1 or end_idx == 0:
                        st.error("Could not parse the response. Please try again.")
                        st.text(content)
                    else:
                        json_str = content[start_idx:end_idx]
                        
                        # Clean control characters from JSON string
                        json_str = re.sub(r'[\x00-\x1f\x7f-\x9f]', ' ', json_str)
                        
                        # Parse with strict=False to handle any remaining control characters
                        subtasks = json.loads(json_str, strict=False)
                        
                        # Display Results
                        st.success("✅ Assignment decomposed successfully!")
                        st.markdown("---")
                        st.header("Step 2: Your Study Plan")
                        
                        # Display subtasks
                        total_hours = 0
                        for i, task in enumerate(subtasks, 1):
                            with st.container():
                                col1, col2 = st.columns([5, 1])
                                with col1:
                                    st.markdown(f"**{i}. {task['description']}**")
                                with col2:
                                    st.markdown(f"**{task['estimated_hours']}h**")
                            total_hours += task['estimated_hours']
                        
                        # Summary
                        st.markdown("---")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total Subtasks", len(subtasks))
                        with col2:
                            st.metric("Total Hours", f"{total_hours}h")
                        with col3:
                            days_until_due = (due_date - date.today()).days
                            st.metric("Days Until Due", days_until_due)
                        
                        # Schedule Recommendation
                        st.subheader("📅 Recommended Schedule")
                        if days_until_due > 0:
                            hours_per_day = total_hours / days_until_due
                            st.info(f"With {total_hours} total hours and {days_until_due} days available, aim for **{hours_per_day:.1f} hours per day**.")
                        else:
                            st.warning("The due date has passed. Please select a future date.")
                        
            except json.JSONDecodeError as e:
                st.error(f"Failed to parse AI response: {e}")
                st.info("The AI returned a response that was not valid JSON. Please try again.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# Footer
st.markdown("---")
st.caption("StudyMate Demo v1.0 | CSC 401 Project | Powered by Google Gemini")
