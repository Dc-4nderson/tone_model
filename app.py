import streamlit as st
import json
import importlib

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

if "pipe" not in st.session_state:
    st.session_state["pipe"] = None

if st.button("Classify"):
    if text_input.strip():
        # Lazy load the model
        if st.session_state["pipe"] is None:
            model_module = importlib.import_module("model")
            st.session_state["pipe"] = model_module.get_pipe()
        pipe = st.session_state["pipe"]
        result = pipe(text_input)
        label = result[0]["label"] if result and "label" in result[0] else str(result)
        st.markdown(f"**Predicted Tone:** {label}")
        st.markdown(f"**Model Confidence:** {result[0]['score']}" if result and "score" in result[0] else "")
        # Section for user feedback
        st.markdown("---")
        st.markdown("#### Was the predicted tone correct?")
        correct = st.radio("Select an option:", ["Yes", "No"], key="correct_radio")
        corrected_label = ""
        if correct == "No":
            corrected_label = st.text_input("Enter the correct tone:", "", key="corrected_label")
        if st.button("Save Result"):
            final_label = corrected_label if correct == "No" and corrected_label else label
            data = {"text": text_input, "label": final_label}
            # Overwrite jsonl if correction, else append
            if correct == "No" and corrected_label:
                # Read all lines, replace last entry
                try:
                    with open("classified_data.jsonl", "r") as f:
                        lines = f.readlines()
                    if lines:
                        lines[-1] = json.dumps(data) + "\n"
                        with open("classified_data.jsonl", "w") as f:
                            f.writelines(lines)
                    else:
                        with open("classified_data.jsonl", "a") as f:
                            f.write(json.dumps(data) + "\n")
                except FileNotFoundError:
                    with open("classified_data.jsonl", "a") as f:
                        f.write(json.dumps(data) + "\n")
            else:
                with open("classified_data.jsonl", "a") as f:
                    f.write(json.dumps(data) + "\n")
            st.success(f"Saved: {data}")
    else:
        st.warning("Please enter some text.")
