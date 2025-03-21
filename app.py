import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Societal Risk Merger Tool", layout="centered")

st.title("🧮 Societal Risk Merger Tool (Based on Risk Ranger)")

st.markdown("""
This tool helps you assess the **overall societal risk** of a food-pathogen scenario by integrating:
- Microbiological Risk Ranger scores
- Economic and political dimensions
- Public trust and market disruption
""")

st.header("Step 1: Microbiological Inputs")

risk_ranger_score = st.slider("Risk Ranger Score (0–100)", 0, 100, 40)

st.markdown("### Estimated Cases per Year (Scientific Notation)")

col1, col2, col3 = st.columns([1, 0.3, 1])
with col1:
    base = st.number_input("", min_value=0.0, value=1.0, step=0.1, label_visibility="collapsed")
with col2:
    st.markdown('<p style="text-align:center; font-size:18px; margin-top:5px;">× 10<sup>^</sup></p>', unsafe_allow_html=True)
with col3:
    exponent = st.selectbox("", list(range(0, 13)), index=3, label_visibility="collapsed")

estimated_cases = base * (10 ** exponent)

st.markdown("### Population Reference for Scaling")
total_population = st.number_input("Total Population at Risk", min_value=1, value=60_000_000, step=100_000)

illness_factor = estimated_cases / total_population

st.markdown("### Health Hazard Severity (Clinical Impact)")
severity_index = st.selectbox("Select severity of the disease:", [
    ("Insignificant – No effect on health (e.g., benign spoilage microbes)", 0.0),
    ("Low – Minor discomfort (e.g., transient nausea from additives)", 0.01),
    ("Moderate – Non-hospitalized illness (e.g., mild salmonellosis in healthy adults)", 0.1),
    ("High – Hospitalization required (e.g., listeriosis or invasive E. coli O157:H7)", 0.5),
    ("Very High – Critical or fatal outcomes (e.g., botulism, neonatal listeriosis)", 1.0)
])[1]

st.markdown(
    f"**Estimated cases:** {estimated_cases:,.0f} "
    f"→ Illness factor: {illness_factor:.6f}"
)

st.header("Step 2: Contextual Impact Factors")

economic_impact = st.selectbox("💸 Economic Impact", [
    ("Insignificant – Insignificant cost or loss", 0.01),
    ("Limited – Local supplier recall (e.g., bakery product batch)", 0.25),
    ("Moderate – National product withdrawal (e.g., cheese recall)", 0.50),
    ("Severe – EU-wide recall or legal sanctions (e.g., dioxin incident)", 1.0)
])[1]

political_risk = st.selectbox("📢 Political/Media Sensitivity", [
    ("Insignificant – Not likely to reach public attention", 0.01),
    ("Low – Local media coverage only", 0.25),
    ("Medium – National media attention (e.g., press conferences)", 0.50),
    ("High – EU-wide or international impact, parliamentary debate", 1.0)
])[1]

market_disruption = st.selectbox("🔗 Market Disruption", [
    ("Insignificant – No impact on market channels", 0.01),
    ("Mild – Temporary removal from single retailer", 0.25),
    ("Moderate – Major retailer suspension or export restrictions", 0.50),
    ("Severe – Complete market recall across multiple countries", 1.0)
])[1]


consumer_trust = st.selectbox("🛒 Consumer Trust Loss", [
    ("Insignificant – No consumer reaction", 0.01),
    ("Low – Short-term concern (e.g., on social media)", 0.25),
    ("Moderate – Drop in brand preference or reputation", 0.50),
    ("High – Long-term distrust, boycotts, or lawsuits", 1.0)
])[1]

st.header("Step 3: Weighting Factors (0 to 100 Scale)")

col1, col2, col3 = st.columns(3)
with col1:
    weight_health = st.number_input("Health Risk", min_value=0.0, max_value=100.0, value=50.0, step=1.0)
with col2:
    weight_economic = st.number_input("Economic Impact", min_value=0.0, max_value=100.0, value=50.0, step=1.0)
with col3:
    weight_political = st.number_input("Political Sensitivity", min_value=0.0, max_value=100.0, value=50.0, step=1.0)

col4, col5, col6 = st.columns(3)
with col4:
    weight_consumer = st.number_input("Consumer Trust", min_value=0.0, max_value=100.0, value=50.0, step=1.0)
with col5:
    weight_market = st.number_input("Market Disruption", min_value=0.0, max_value=100.0, value=50.0, step=1.0)

st.header("Step 4: Results")

# Composite health risk
health_risk = (risk_ranger_score / 100) * illness_factor * severity_index * (weight_health / 100) * 100

# Final score
score = (
    health_risk +
    float(economic_impact) * (weight_economic / 100) * 100 +
    float(political_risk) * (weight_political / 100) * 100 +
    float(consumer_trust) * (weight_consumer / 100) * 100 +
    float(market_disruption) * (weight_market / 100) * 100
)

final_score = min(score, 100)

# Classification
if final_score < 40:
    level = "🟢 Low Societal Risk"
elif final_score < 70:
    level = "🟡 Moderate Societal Risk"
else:
    level = "🔴 High Societal Risk"

st.subheader("🧾 Composite Societal Risk Score")
st.markdown(f"**Final Score: {final_score:.2f} / 100** — {level}")

# Bar chart output
st.subheader("📊 Contribution by Risk Domain")

labels = [
    "Health Risk",
    "Economic Risk",
    "Political Risk",
    "Consumer Trust",
    "Market Impact"
]

values = [
    health_risk,
    float(economic_impact) * (weight_economic / 100) * 100,
    float(political_risk) * (weight_political / 100) * 100,
    float(consumer_trust) * (weight_consumer / 100) * 100,
    float(market_disruption) * (weight_market / 100) * 100
]

fig, ax = plt.subplots()
ax.barh(labels, values, color="skyblue")
ax.set_xlabel("Weighted Contribution (%)")
ax.set_xlim(0, 100)
st.pyplot(fig)

st.markdown("---")
