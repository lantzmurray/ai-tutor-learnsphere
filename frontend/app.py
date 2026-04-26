"""
Frontend Application for AI Tutor & Quiz Generator.

This Streamlit app provides educational support through two main features:
1. Quiz Mode: Generate customized quizzes on any subject
2. Explain Mode: Get clear explanations of educational concepts
"""

import os
import sys

import streamlit as st
import requests

PACKAGE_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..")
)
if PACKAGE_ROOT not in sys.path:
    sys.path.insert(0, PACKAGE_ROOT)

from components import render_app_footer, run_with_status_updates

# Set the page title and configure the app layout
st.title("AI Tutor & Quiz Generator (Mistral + LLaMA 2)")

# Create two tabs for the two main features: Quiz Generator and Concept Explainer
tab1, tab2 = st.tabs(["Quiz Generator", "Concept Explainer"])

# Tab 1: Quiz Generator
with tab1:
    st.subheader("Generate a Custom Quiz")

    # User input: text field for quiz topic
    quiz_topic = st.text_input("Quiz Topic:", placeholder="e.g., Python Programming")

    # User input: slider to select number of questions (3-10, default 5)
    num_questions = st.slider("Number of Questions:", 3, 10, 5)

    # Trigger quiz generation when button is clicked
    if st.button("Generate Quiz"):
        if quiz_topic:
            # Send quiz request to FastAPI backend
            # Uses Form data to match FastAPI endpoint expectations
            response = run_with_status_updates(
                lambda: requests.post(
                    "http://localhost:8000/quiz/",
                    data={"topic": quiz_topic, "num_questions": num_questions}
                ),
                start_message="Generating the quiz..."
            )

            # Display the generated quiz or error message based on response
            if response.status_code == 200:
                quiz = response.json().get("quiz", "Error")
                st.subheader("Generated Quiz:")
                st.write(quiz)
            else:
                st.error("Error generating quiz. Make sure the backend is running.")
        else:
            st.warning("Please enter a quiz topic.")

# Tab 2: Concept Explainer
with tab2:
    st.subheader("Explain a Concept")

    # User input: text field for concept to explain
    explain_topic = st.text_input("Concept to Explain:", placeholder="e.g., Machine Learning")

    # Trigger explanation when button is clicked
    if st.button("Get Explanation"):
        if explain_topic:
            # Send explanation request to FastAPI backend
            # Uses Form data to match FastAPI endpoint expectations
            response = run_with_status_updates(
                lambda: requests.post(
                    "http://localhost:8000/explain/",
                    data={"topic": explain_topic}
                ),
                start_message="Generating the explanation..."
            )

            # Display the explanation or error message based on response
            if response.status_code == 200:
                explanation = response.json().get("explanation", "Error")
                st.subheader("Explanation:")
                st.write(explanation)
            else:
                st.error("Error getting explanation. Make sure the backend is running.")
        else:
            st.warning("Please enter a concept to explain.")


render_app_footer()
