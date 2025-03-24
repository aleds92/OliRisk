
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Societal Risk Merger Tool", layout="centered")
st.title("🧮 Societal Risk Merger Tool")

# ---------------- PRESETS ----------------
st.sidebar.header("🎯 Select Preset Scenario")

presets = {
    "Custom": None,
    "RTE Salad – Simulation 1": {
        "rr_score": 72,
        "illness_base": 2.34,
        "illness_exponent": 5,
        "population": 60000000,
        "economic": "Moderate – National product withdrawal (e.g., cheese recall)",
        "political": "Medium – National media attention (e.g., press release)",
        "trust": "Moderate – Notable drop in trust or loyalty",
        "market": "Moderate – Withdrawal from major retailers",
        "weights": {
            "health": "Significant to public health",
            "economic": "Budgetary consideration",
            "political": "National political/media relevance",
            "trust": "Could impact perception or loyalty",
            "market": "Regional disruption possible"
        }
    }
}

selected_preset = st.sidebar.selectbox("Choose scenario", list(presets.keys()))
preset = presets[selected_preset]

# ---------------- STEP 1 ----------------
st.header("Step 1: Microbiological Inputs")

rr_score = st.slider("Risk Ranger Score (0–100)", 0, 100, value=preset["rr_score"] if preset else 50)

col1, col2, col3 = st.columns([1, 0.3, 1])
with col1:
    base = st.number_input("Estimated Illness (Base)", min_value=0.0, value=preset["illness_base"] if preset else 1.0)
with col2:
    st.markdown('<p style="text-align:center; font-size:18px; margin-top:10px;">× 10^</p>', unsafe_allow_html=True)
with col3:
    exponent = st.number_input("Exponent", min_value=0, max_value=12, value=preset["illness_exponent"] if preset else 5)

total_population = st.number_input("Total Population at Risk", min_value=1, value=preset["population"] if preset else 60000000)

# ---------------- STEP 2 ----------------
st.header("Step 2: Contextual Impact")
st.info("❓ Not sure how to choose the right impact values? Click the tip below for guidance.")
with st.expander("💡 Tips"):
    st.markdown("""
    **🔸 Economic Impact**  
    - Use **75–100** if national recalls, legal consequences, or multi-country disruptions occur.  
    - **50** fits limited regional withdrawals or financial losses.  
    - **25** is appropriate for batch-level product reprocessing or negligible financial cost.

    **🔸 Political/Media Sensitivity**  
    - **75–100** when national or international media is involved, or if public officials respond.  
    - Use **50** for local coverage or niche media interest.  
    - **25** for internal issues with no media attention.

    **🔸 Consumer Trust Loss**  
    - **75–100** if consumer backlash, social media storm, or boycotts are likely.  
    - **50** for reputational concern or increased customer service demand.  
    - **25** when customers are unlikely to notice or care.

    **🔸 Market Disruption**  
    - Choose **75–100** if large-scale product removal or barriers to trade exist.  
    - **50** for limited retailer or distributor withdrawal.  
    - **25** if the product remains widely available.

    💬 *Think in terms of visibility and scale: who is affected, how publicly, and how widely?*
    """)


economic_levels = {
    "Insignificant – No cost or loss (e.g., no recall)": 25,
    "Limited – Local supplier loss (e.g., bakery batch recall)": 50,
    "Moderate – National product withdrawal (e.g., cheese recall)": 75,
    "Severe – EU-wide recall or legal sanctions": 100
}
political_levels = {
    "Insignificant – Not publicly visible": 25,
    "Low – Local media coverage": 50,
    "Medium – National media attention (e.g., press release)": 75,
    "High – EU-wide attention, parliamentary debate": 100
}
trust_levels = {
    "Insignificant – No public awareness": 25,
    "Low – Minor social media concern": 50,
    "Moderate – Notable drop in trust or loyalty": 75,
    "High – Public backlash, boycott, lawsuits": 100
}
market_levels = {
    "Insignificant – No disruption to market access": 25,
    "Mild – Removal from single shop or site": 50,
    "Moderate – Withdrawal from major retailers": 75,
    "Severe – Multi-country recall, trade barriers": 100
}

economic_choice = st.selectbox("💸 Economic Impact", list(economic_levels.keys()),
    index=list(economic_levels.keys()).index(preset["economic"]) if preset else 0)
economic = economic_levels[economic_choice]

political_choice = st.selectbox("📢 Political/Media Sensitivity", list(political_levels.keys()),
    index=list(political_levels.keys()).index(preset["political"]) if preset else 0)
political = political_levels[political_choice]

trust_choice = st.selectbox("🛒 Consumer Trust Loss", list(trust_levels.keys()),
    index=list(trust_levels.keys()).index(preset["trust"]) if preset else 0)
trust = trust_levels[trust_choice]

market_choice = st.selectbox("🔗 Market Disruption", list(market_levels.keys()),
    index=list(market_levels.keys()).index(preset["market"]) if preset else 0)
market = market_levels[market_choice]

# ---------------- STEP 3 ----------------
st.header("Step 3: Weights (Importance)")
st.info("❓ Unsure about weight selection? Expand the tip below to help balance your priorities.")
with st.expander("💡 Tips"):
    st.markdown("""
    **Weights reflect how much importance each domain has** in your overall risk assessment.  
    Use high weights when a variable is **critical** to public health, policy, or perception.

    - **⚕️ Health** → Prioritize if illnesses are severe or difficult to treat.  
    - **💸 Economic** → Increase when business continuity or supply chains are at risk.  
    - **📢 Political/Media** → Use higher weight if reputational damage or governmental involvement is expected.  
    - **🛒 Consumer Trust** → Elevate when trust in brand or food safety systems is sensitive.  
    - **🔗 Market** → Increase if cross-border trade or broad distribution is involved.

    💡 *Balance matters: Don't just assign everything as 'Top Priority'. Use nuance.*
    """)


health_weight_levels = {
    "Not relevant – No impact on public health decision": 0,
    "Monitor but not critical": 25,
    "Significant to public health": 50,
    "Top priority for decision-makers": 100
}
econ_weight_levels = {
    "Negligible cost concern": 0,
    "Minor business impact": 25,
    "Budgetary consideration": 50,
    "Major economic consequence": 100
}
pol_weight_levels = {
    "Politically neutral": 0,
    "Local political interest only": 25,
    "National political/media relevance": 50,
    "Politically sensitive or explosive": 100
}
trust_weight_levels = {
    "Trust unaffected": 0,
    "Slight brand concern": 25,
    "Could impact perception or loyalty": 50,
    "Trust is key to public reaction": 100
}
market_weight_levels = {
    "Market not affected": 0,
    "Local distribution only": 25,
    "Regional disruption possible": 50,
    "Trade-wide or international effect": 100
}

health_weight_choice = st.selectbox("⚕️ Health Weight", list(health_weight_levels.keys()),
    index=list(health_weight_levels.keys()).index(preset["weights"]["health"]) if preset else 0)
w_health = health_weight_levels[health_weight_choice]

econ_weight_choice = st.selectbox("💸 Economic Weight", list(econ_weight_levels.keys()),
    index=list(econ_weight_levels.keys()).index(preset["weights"]["economic"]) if preset else 0)
w_econ = econ_weight_levels[econ_weight_choice]

pol_weight_choice = st.selectbox("📢 Political Weight", list(pol_weight_levels.keys()),
    index=list(pol_weight_levels.keys()).index(preset["weights"]["political"]) if preset else 0)
w_pol = pol_weight_levels[pol_weight_choice]

trust_weight_choice = st.selectbox("🛒 Consumer Trust Weight", list(trust_weight_levels.keys()),
    index=list(trust_weight_levels.keys()).index(preset["weights"]["trust"]) if preset else 0)
w_trust = trust_weight_levels[trust_weight_choice]

market_weight_choice = st.selectbox("🔗 Market Weight", list(market_weight_levels.keys()),
    index=list(market_weight_levels.keys()).index(preset["weights"]["market"]) if preset else 0)
w_market = market_weight_levels[market_weight_choice]

# ---------------- STEP 4 ----------------
st.header("Step 4: Results")

estimated_cases = base * (10 ** exponent)
illness_factor = (estimated_cases / total_population) * 100

# Logistic multiplier between 0 and 1
L = 1.0
x0 = 0.2
k = 5
multiplier = L / (1 + math.exp(-k * (illness_factor - x0)))

# Risk category for display
if illness_factor < 0.01:
    category = "🟢 Minimal Risk"
elif illness_factor < 0.1:
    category = "🟡 Low Risk"
elif illness_factor < 0.5:
    category = "🟠 Moderate Risk"
elif illness_factor <= 1.0:
    category = "🔴 High Risk"
else:
    category = "🔴🚨 Critical Risk"

rr_scaled = rr_score * multiplier

alpha = 1.5
beta = 1.5
health_contrib = rr_scaled * ((w_health / 100) ** alpha)
econ_contrib = rr_scaled * ((w_econ / 100) ** alpha) * ((economic / 100) ** beta)
pol_contrib = rr_scaled * ((w_pol / 100) ** alpha) * ((political / 100) ** beta)
trust_contrib = rr_scaled * ((w_trust / 100) ** alpha) * ((trust / 100) ** beta)
market_contrib = rr_scaled * ((w_market / 100) ** alpha) * ((market / 100) ** beta)

# Normalize contributions
total_contrib = health_contrib + econ_contrib + pol_contrib + trust_contrib + market_contrib
if total_contrib > 0:
    norm_health = (health_contrib / total_contrib) * 100
    norm_econ = (econ_contrib / total_contrib) * 100
    norm_pol = (pol_contrib / total_contrib) * 100
    norm_trust = (trust_contrib / total_contrib) * 100
    norm_market = (market_contrib / total_contrib) * 100
else:
    norm_health = norm_econ = norm_pol = norm_trust = norm_market = 0.0

final_score = min(total_contrib, 100)

if final_score < 40:
    risk_level = "🟢 Low Societal Risk"
elif final_score < 70:
    risk_level = "🟡 Moderate Societal Risk"
else:
    risk_level = "🔴 High Societal Risk"

st.subheader("📊 Final Score")
st.metric(label="Composite Risk Score", value=f"{final_score:.2f} / 100", delta=risk_level)

st.markdown(f"""
**Illness Factor:** `{illness_factor:.6f}%`  
**Category:** {category}  
**Illness Multiplier:** `{multiplier:.3f}`  
**RR Scaled:** `{rr_scaled:.2f}`
""")

with st.expander("📥 Contribution by Domain (Normalized to 100)", expanded=True):
    st.write(f"⚕️ Health: {norm_health:.1f}")
    st.write(f"💸 Economic: {norm_econ:.1f}")
    st.write(f"📢 Political: {norm_pol:.1f}")
    st.write(f"🛒 Trust: {norm_trust:.1f}")
    st.write(f"🔗 Market: {norm_market:.1f}")

# ---------------- CHARTS ----------------
st.subheader("📊 Normalized Domain Contribution – Bar Chart")

labels = ["⚕️ Health", "💸 Economic", "📢 Political", "🛒 Trust", "🔗 Market"]
values = [norm_health, norm_econ, norm_pol, norm_trust, norm_market]

fig_bar, ax_bar = plt.subplots()
ax_bar.barh(labels, values, color="skyblue")
ax_bar.set_xlabel("Normalized Contribution (0–100)")
ax_bar.set_xlim(0, 100)
for i, v in enumerate(values):
    ax_bar.text(v + 1, i, f"{v:.1f}", va="center")
st.pyplot(fig_bar)

# PIE CHART
st.subheader("🧁 Contextual Risk Breakdown (Excludes Health) – Normalized")

labels_context = ["⚕️ Health", "💸 Economic", "📢 Political", "🛒 Trust", "🔗 Market"]
values_context = [norm_health, norm_econ, norm_pol, norm_trust, norm_market]

filtered_labels = []
filtered_values = []
for label, value in zip(labels_context, values_context):
    if not (value is None or np.isnan(value) or value == 0):
        filtered_labels.append(label)
        filtered_values.append(value)

def autopct_no_percent(pct):
    return f"{pct:.1f}"

if filtered_values:
    fig_pie, ax_pie = plt.subplots()
    ax_pie.pie(filtered_values, labels=filtered_labels, autopct=autopct_no_percent, startangle=140)
    ax_pie.axis("equal")
    st.pyplot(fig_pie)
else:
    st.warning("⚠️ Cannot display pie chart – all contextual contributions are zero or missing.")
