import streamlit as st
import json
from model import pipe

st.set_page_config(page_title="Tone Classification", layout="centered")

# Custom CSS for black background and white text
st.markdown(
    """
    <style>
    body, .stApp {
        background-color: #000000;
        color: #FFFFFF;
    }
    .stTextInput > div > input {
        color: #FFFFFF !important;
        background-color: #222222 !important;
    }
    .stButton > button {
        color: #FFFFFF !important;
        background-color: #333333 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Tone Classification App")

st.markdown(
    """
    ### Instructions
    This app classifies the tone of your text into one of the following categories:
    - **Uplifting**
    - **Motivational**
    - **Practical**
    - **Informative**
    - **Reflective**
    - **Optimistic**
    - **Thoughtful**
    
    **How to use:**
    1. Enter your text in the input box below.
    2. Click the **Classify** button.
    3. The predicted tone will be displayed and saved for future reference.
    """
)

text_input = st.text_input("Enter text to classify:", "", key="text_input")

if st.button("Classify"):
    if text_input.strip():
        result = pipe(text_input)
        label = result[0]["label"] if result and "label" in result[0] else str(result)
        st.markdown(f"**Predicted Tone:** {label}")
        # Append to jsonl file
        data = {"text": text_input, "label": label}
        with open("classified_data.jsonl", "a") as f:
            f.write(json.dumps(data) + "\n")
    else:
        st.warning("Please enter some text.")
