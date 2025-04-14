
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import traceback
import uuid
import json

st.set_page_config(page_title="HoliRisk", layout="centered")

# --- Existing app code remains unchanged up to the Google Sheets section ---

st.header("☁️ Anonymized Data Submission")

st.markdown("""
> ℹ️ **Why are we collecting this data?** 
> Your input helps us understand how the tool is being used and what to improve next.

📝 Please feel free to leave a comment or describe your professional background.
""")

job_role = st.text_input("💼 What is your job role? (e.g., Microbiologist, Quality Manager, Food Safety Officer, Student)")
institution = st.text_input("🏠 What is your home institution? (e.g. Company, University, Governative Agency)")
years_experience = st.number_input("📅 Years of experience in the field:", min_value=0, step=1)

st.markdown("⚠️ **The following field is intended for anonymous feedback only. Please do not include personal information such as your name, email, or any other personal information.**")

user_feedback = st.text_area("💬 Share your suggestions or difficulties using this tool:", height=70, key="user_feedback_box")

st.markdown(
    "**Data Privacy Notice**  \n"
    "The input and data you provide will be stored anonymously and used only to improve this tool.  \n"
    "We do not collect any personal or identifying information. By submitting your input, you agree to their usage in developing **HoliRisk**."
)

suspicious_words = ["@", "email", "telefono", "number", "call", "card", "telephone","+", "tel", "mi chiamo", "sono di", "contattami", ".it", ".com", "scrivimi", "chiamami"]
if any(w in user_feedback.lower() for w in suspicious_words):
    st.warning("⚠️ Your feedback seems to contain personal information. Please remove names, emails, or contact details before submitting.")
    st.stop()

if "data_sent" not in st.session_state:
    st.session_state["data_sent"] = False

if st.button("📤 Save Anonymized Data to Google Sheets"):
    try:
        if selected_preset != "Custom":
            st.warning("⚠️ Only custom scenarios can be submitted. Please select 'Custom' to proceed.")
            st.stop()

        if st.session_state["data_sent"]:
            st.warning("⚠️ Data has already been submitted in this session.")
            st.stop()

        default_values = {
            'rr_score': 50,
            'base': 1.0,
            'exponent': 5,
            'total_population': 60000000,
            'economic_choice': list(economic_levels.keys())[0],
            'political_choice': list(political_levels.keys())[0],
            'trust_choice': list(trust_levels.keys())[0],
            'market_choice': list(market_levels.keys())[0],
            'health_weight_choice': list(health_weight_levels.keys())[0],
            'econ_weight_choice': list(econ_weight_levels.keys())[0],
            'pol_weight_choice': list(pol_weight_levels.keys())[0],
            'trust_weight_choice': list(trust_weight_levels.keys())[0],
            'market_weight_choice': list(market_weight_levels.keys())[0],
        }

        user_values = {
            'rr_score': rr_score,
            'base': base,
            'exponent': exponent,
            'total_population': total_population,
            'economic_choice': economic_choice,
            'political_choice': political_choice,
            'trust_choice': trust_choice,
            'market_choice': market_choice,
            'health_weight_choice': health_weight_choice,
            'econ_weight_choice': econ_weight_choice,
            'pol_weight_choice': pol_weight_choice,
            'trust_weight_choice': trust_weight_choice,
            'market_weight_choice': market_weight_choice,
        }

        if all(user_values[k] == default_values[k] for k in default_values) and not user_feedback.strip():
            st.warning("⚠️ Data not saved: no values were changed and no feedback was provided.")
            st.stop()

        with st.spinner("⏳ Saving your data... Please do not close the page."):
            scope = [
                "https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ]

            creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["google_service_account"], scope)
            client = gspread.authorize(creds)
            sheet = client.open("HoliRisk Data Logger").sheet1

            session_id = str(uuid.uuid4())
            row = [
                datetime.datetime.now().isoformat(),
                session_id,
                selected_preset,
                rr_score,
                base,
                exponent,
                total_population,
                economic_choice,
                political_choice,
                trust_choice,
                market_choice,
                health_weight_choice,
                econ_weight_choice,
                pol_weight_choice,
                trust_weight_choice,
                market_weight_choice,
                illness_factor,
                risk_level,
                final_score,
                job_role,
                institution,
                years_experience,
                user_feedback
            ]

            sheet.append_row(row, value_input_option="USER_ENTERED")
            st.session_state["data_sent"] = True
            st.success("✅ Your custom scenario has been saved successfully. Thank you for your contribution!")

    except Exception as e:
        st.error("❌ An error occurred while saving the data.")
        st.code(traceback.format_exc())



# --- Anonymized Data Submission Section ---
st.header("☁️ Anonymized Data Submission")

st.markdown("""
> ℹ️ **Why are we collecting this data?** 
> Your input helps us understand how the tool is being used and what to improve next.

📝 Please feel free to leave a comment or describe your professional background.
""")

job_role = st.text_input("💼 What is your job role? (e.g., Microbiologist, Quality Manager, Food Safety Officer, Student)")
institution = st.text_input("🏠 What is your home institution? (e.g. Company, University, Governative Agency)")
years_experience = st.number_input("📅 Years of experience in the field:", min_value=0, step=1)

st.markdown("⚠️ **The following field is intended for anonymous feedback only. Please do not include personal information such as your name, email, or any other personal information.**")

user_feedback = st.text_area("💬 Share your suggestions or difficulties using this tool:", height=70, key="user_feedback_box")

st.markdown(
    "**Data Privacy Notice**  \n"
    "The input and data you provide will be stored anonymously and used only to improve this tool.  \n"
    "We do not collect any personal or identifying information. By submitting your input, you agree to their usage in developing **HoliRisk**."
)

suspicious_words = ["@", "email", "telefono", "number", "call", "card", "telephone","+", "tel", "mi chiamo", "sono di", "contattami", ".it", ".com", "scrivimi", "chiamami"]
if any(w in user_feedback.lower() for w in suspicious_words):
    st.warning("⚠️ Your feedback seems to contain personal information. Please remove names, emails, or contact details before submitting.")
    st.stop()

if "data_sent" not in st.session_state:
    st.session_state["data_sent"] = False

if st.button("📤 Save Anonymized Data to Google Sheets"):
    try:
        if selected_preset != "Custom":
            st.warning("⚠️ Only custom scenarios can be submitted. Please select 'Custom' to proceed.")
            st.stop()

        if st.session_state["data_sent"]:
            st.warning("⚠️ Data has already been submitted in this session.")
            st.stop()

        default_values = {
            'rr_score': 50,
            'base': 1.0,
            'exponent': 5,
            'total_population': 60000000,
            'economic_choice': list(economic_levels.keys())[0],
            'political_choice': list(political_levels.keys())[0],
            'trust_choice': list(trust_levels.keys())[0],
            'market_choice': list(market_levels.keys())[0],
            'health_weight_choice': list(health_weight_levels.keys())[0],
            'econ_weight_choice': list(econ_weight_levels.keys())[0],
            'pol_weight_choice': list(pol_weight_levels.keys())[0],
            'trust_weight_choice': list(trust_weight_levels.keys())[0],
            'market_weight_choice': list(market_weight_levels.keys())[0],
        }

        user_values = {
            'rr_score': rr_score,
            'base': base,
            'exponent': exponent,
            'total_population': total_population,
            'economic_choice': economic_choice,
            'political_choice': political_choice,
            'trust_choice': trust_choice,
            'market_choice': market_choice,
            'health_weight_choice': health_weight_choice,
            'econ_weight_choice': econ_weight_choice,
            'pol_weight_choice': pol_weight_choice,
            'trust_weight_choice': trust_weight_choice,
            'market_weight_choice': market_weight_choice,
        }

        if all(user_values[k] == default_values[k] for k in default_values) and not user_feedback.strip():
            st.warning("⚠️ Data not saved: no values were changed and no feedback was provided.")
            st.stop()

        with st.spinner("⏳ Saving your data... Please do not close the page."):
            scope = [
                "https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ]

            creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["google_service_account"], scope)
            client = gspread.authorize(creds)
            sheet = client.open("HoliRisk Data Logger").sheet1

            session_id = str(uuid.uuid4())
            row = [
                datetime.datetime.now().isoformat(),
                session_id,
                selected_preset,
                rr_score,
                base,
                exponent,
                total_population,
                economic_choice,
                political_choice,
                trust_choice,
                market_choice,
                health_weight_choice,
                econ_weight_choice,
                pol_weight_choice,
                trust_weight_choice,
                market_weight_choice,
                illness_factor,
                risk_level,
                final_score,
                job_role,
                institution,
                years_experience,
                user_feedback
            ]

            sheet.append_row(row, value_input_option="USER_ENTERED")
            st.session_state["data_sent"] = True
            st.success("✅ Your custom scenario has been saved successfully. Thank you for your contribution!")

    except Exception as e:
        st.error("❌ An error occurred while saving the data.")
        st.code(traceback.format_exc())
