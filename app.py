import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math
st.set_page_config(page_title="OliRisk", layout="centered")

# ---------------- CONFIG ----------------
st.title("🧮 HoliRisk")

# ---------------- PRESETS ----------------
st.sidebar.header("🎯 Select Preset Scenario")

presets = {
    "Custom": None,
    "RTE Salad – Standard": {
        "rr_score": 60,
        "illness_base": 2.34,
        "illness_exponent": 3,
        "population": 60000000,
        "economic": "Limited – Local supplier loss (e.g., bakery batch recall)",
        "political": "Low – Local media coverage",
        "trust": "Moderate – Notable drop in trust or loyalty",
        "market": "Moderate – Withdrawal from major retailers",
        "weights": {
            "health": "Significant to public health",
            "economic": "Minor business impact",
            "political": "Local political interest only",
            "trust": "Could impact perception or loyalty",
            "market": "Regional disruption possible"
        }
    },
    "RTE Salad – Simulation 1": {
        "rr_score": 72,
        "illness_base": 2.34,
        "illness_exponent": 5,
        "population": 60000000,
        "economic": "Moderate – National product withdrawal (e.g., cheese recall)",
        "political": "Medium – National media attention (e.g., press release)",
        "trust": "High – Public backlash, boycott, lawsuits",
        "market": "Severe – Multi-country recall, trade barriers",
        "weights": {
            "health": "Top priority for decision-makers",
            "economic": "Budgetary consideration",
            "political": "National political/media relevance",
            "trust": "Trust is key to public reaction",
            "market": "Trade-wide or international effect"
        }
    },
    "RTE Salad – Simulation 2": {
        "rr_score": 62,
        "illness_base": 4.68,
        "illness_exponent": 3,
        "population": 60000000,
        "economic": "Moderate – National product withdrawal (e.g., cheese recall)",
        "political": "Medium – National media attention (e.g., press release)",
        "trust": "Moderate – Notable drop in trust or loyalty",
        "market": "Severe – Multi-country recall, trade barriers",
        "weights": {
            "health": "Significant to public health",
            "economic": "Budgetary consideration",
            "political": "National political/media relevance",
            "trust": "Could impact perception or loyalty",
            "market": "Trade-wide or international effect"
        }
    },
    "RTE Chicken – Standard": {
        "rr_score": 45,
        "illness_base": 5.85,
        "illness_exponent": 2,
        "population": 60000000,
        "economic": "Limited – Local supplier loss (e.g., bakery batch recall)",
        "political": "Low – Local media coverage",
        "trust": "Low – Minor social media concern",
        "market": "Mild – Removal from single shop or site",
        "weights": {
            "health": "Significant to public health",
            "economic": "Minor business impact",
            "political": "Local political interest only",
            "trust": "Slight brand concern",
            "market": "Local distribution only"
        }
    },
    "RTE Chicken – Simulation 1": {
        "rr_score": 58,
        "illness_base": 8.78,
        "illness_exponent": 4,
        "population": 60000000,
        "economic": "Severe – EU-wide recall or legal sanctions",
        "political": "Medium – National media attention (e.g., press release)",
        "trust": "Moderate – Notable drop in trust or loyalty",
        "market": "Moderate – Withdrawal from major retailers",
        "weights": {
            "health": "Top priority for decision-makers",
            "economic": "Major economic consequence",
            "political": "National political/media relevance",
            "trust": "Could impact perception or loyalty",
            "market": "Regional disruption possible"
        }
    },
    "RTE Chicken – Simulation 2": {
        "rr_score": 57,
        "illness_base": 5.87,
        "illness_exponent": 4,
        "population": 60000000,
        "economic": "Severe – EU-wide recall or legal sanctions",
        "political": "Medium – National media attention (e.g., press release)",
        "trust": "Moderate – Notable drop in trust or loyalty",
        "market": "Moderate – Withdrawal from major retailers",
        "weights": {
            "health": "Top priority for decision-makers",
            "economic": "Budgetary consideration",
            "political": "National political/media relevance",
            "trust": "Could impact perception or loyalty",
            "market": "Regional disruption possible"
        }
    },
    "RTE Tiramisu – Standard": {
        "rr_score": 49,
        "illness_base": 2.34,
        "illness_exponent": 3,
        "population": 60000000,
        "economic": "Limited – Local supplier loss (e.g., bakery batch recall)",
        "political": "Medium – National media attention (e.g., press release)",
        "trust": "Moderate – Notable drop in trust or loyalty",
        "market": "Mild – Removal from single shop or site",
        "weights": {
            "health": "Significant to public health",
            "economic": "Minor business impact",
            "political": "National political/media relevance",
            "trust": "Could impact perception or loyalty",
            "market": "Local distribution only"
        }
    },
    "RTE Tiramisu – Simulation 1": {
        "rr_score": 60,
        "illness_base": 2.43,
        "illness_exponent": 5,
        "population": 60000000,
        "economic": "Moderate – National product withdrawal (e.g., cheese recall)",
        "political": "High – EU-wide attention, parliamentary debate",
        "trust": "High – Public backlash, boycott, lawsuits",
        "market": "Moderate – Withdrawal from major retailers",
        "weights": {
            "health": "Top priority for decision-makers",
            "economic": "Budgetary consideration",
            "political": "Politically sensitive or explosive",
            "trust": "Trust is key to public reaction",
            "market": "Regional disruption possible"
        }
    },
    "RTE Tiramisu – Simulation 2": {
        "rr_score": 60,
        "illness_base": 2.43,
        "illness_exponent": 5,
        "population": 60000000,
        "economic": "Moderate – National product withdrawal (e.g., cheese recall)",
        "political": "High – EU-wide attention, parliamentary debate",
        "trust": "High – Public backlash, boycott, lawsuits",
        "market": "Moderate – Withdrawal from major retailers",
        "weights": {
            "health": "Top priority for decision-makers",
            "economic": "Budgetary consideration",
            "political": "Politically sensitive or explosive",
            "trust": "Trust is key to public reaction",
            "market": "Regional disruption possible"
        }
    },
    
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
    st.markdown('<p style="text-align:center; font-size:18px; margin-top:33px;">× 10^</p>', unsafe_allow_html=True)
with col3:
    exponent = st.number_input("Exponent", min_value=0, max_value=12, value=preset["illness_exponent"] if preset else 5)

total_population = st.number_input("Total Population at Risk", min_value=1, value=preset["population"] if preset else 60000000)

# ---------------- STEP 2 ----------------
st.header("Step 2: Contextual Impact")
st.info("❓ Not sure how to choose the right impact values? Click the tip below for guidance.")
with st.expander("💡 Tips"):
    st.markdown("""
    **🔸 Economic Impact**  
    - Use **Limited to Severe** if national recalls, legal consequences, or multi-country disruptions occur.  
    - **Moderate to Limited** fits limited regional withdrawals or financial losses.  
    - **Insignificant to Moderate** is appropriate for batch-level product reprocessing or negligible financial cost.

    **🔸 Political/Media Sensitivity**  
   
    - Use **Insignificant to Low** for internal issues with no media attention.
    - **Low to Medium** for local coverage or niche media interest.  
    - **Medium to High** when national or international media is involved, or if public officials respond.  

    **🔸 Consumer Trust Loss**  
    - Use **Insignificant to Low** when customers are unlikely to notice or care.   
    - **Low to Medium** for reputational concern or increased customer service demand.  
    - **Medium  to High** if consumer backlash, social media storm, or boycotts are likely.

    **🔸 Market Disruption**  
    - Use **Insignificant to Low** if the product remains widely available.  
    - **Low to Medium** for limited retailer or distributor withdrawal.  
    - **Moderate to Severe** if large-scale product removal or barriers to trade exist.

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
st.subheader("📊 Domain Contributions – Bar Chart")

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
st.subheader("📊 Contextual Risk Breakdown")

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
  
  # ---------------- FEEDBACK + PDF REPORT ----------------
st.header("📝 User Feedback & PDF Report")

# Feedback Text Area
user_feedback = st.text_area("💬 Share your suggestions or difficulties using this tool:", height=150)

# Generate PDF Button
generate_report = st.button("📄 Generate Risk Report (PDF)")

if generate_report:
    from io import BytesIO
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import ImageReader

    buffer = BytesIO()
    pie_buffer = BytesIO()

    # Save pie chart to BytesIO
    if filtered_values:
        fig_pie.savefig(pie_buffer, format='png', bbox_inches='tight')
        pie_buffer.seek(0)
        pie_image = ImageReader(pie_buffer)
    else:
        pie_image = None

    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 40

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "📄 OliRisk – Risk Assessment Report")
    y -= 30

    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Selected Scenario: {selected_preset}")
    y -= 20

    # Step 1 – Microbiological Inputs
    c.drawString(50, y, "🧮 Microbiological Inputs:")
    y -= 15
    c.drawString(70, y, f"Risk Ranger Score: {rr_score}")
    y -= 15
    c.drawString(70, y, f"Estimated Illness Base: {base}")
    y -= 15
    c.drawString(70, y, f"Exponent: {exponent}")
    y -= 15
    c.drawString(70, y, f"Total Population at Risk: {total_population}")
    y -= 25

    # Step 2 – Contextual Impacts
    c.drawString(50, y, "🌍 Contextual Impact Selections:")
    y -= 15
    c.drawString(70, y, f"Economic Impact: {economic_choice}")
    y -= 15
    c.drawString(70, y, f"Political Sensitivity: {political_choice}")
    y -= 15
    c.drawString(70, y, f"Consumer Trust Loss: {trust_choice}")
    y -= 15
    c.drawString(70, y, f"Market Disruption: {market_choice}")
    y -= 25

    # Step 3 – Weights
    c.drawString(50, y, "⚖️ Importance Weights:")
    y -= 15
    c.drawString(70, y, f"Health Weight: {health_weight_choice}")
    y -= 15
    c.drawString(70, y, f"Economic Weight: {econ_weight_choice}")
    y -= 15
    c.drawString(70, y, f"Political Weight: {pol_weight_choice}")
    y -= 15
    c.drawString(70, y, f"Trust Weight: {trust_weight_choice}")
    y -= 15
    c.drawString(70, y, f"Market Weight: {market_weight_choice}")
    y -= 25

    # Step 4 – Final Results
    c.drawString(50, y, "📊 Final Results:")
    y -= 15
    c.drawString(70, y, f"Composite Risk Score: {final_score:.2f} / 100 – {risk_level}")
    y -= 15

    # Normalized Contributions
    c.drawString(50, y, "🔹 Factors contributions:")
    y -= 15
    c.drawString(70, y, f"⚕️ Health: {norm_health:.1f}%")
    y -= 15
    c.drawString(70, y, f"💸 Economic: {norm_econ:.1f}%")
    y -= 15
    c.drawString(70, y, f"📢 Political: {norm_pol:.1f}%")
    y -= 15
    c.drawString(70, y, f"🛒 Trust: {norm_trust:.1f}%")
    y -= 15
    c.drawString(70, y, f"🔗 Market: {norm_market:.1f}%")
    y -= 25

    # Insert Pie Chart if available
    if pie_image and y > 250:
        c.drawString(50, y, "🥧 Contextual Risk Pie Chart:")
        y -= 10
        c.drawImage(pie_image, 100, y - 180, width=300, height=180)
        y -= 200
    elif pie_image:
        c.showPage()
        y = height - 40
        c.drawString(50, y, "🥧 Contextual Risk Pie Chart (continued):")
        y -= 10
        c.drawImage(pie_image, 100, y - 180, width=300, height=300)
        y -= 200
    else:
        c.drawString(50, y, "⚠️ No contextual contributions to generate a pie chart.")
        y -= 30

    # Feedback Section
    if user_feedback:
        if y < 100:
            c.showPage()
            y = height - 40
        c.drawString(50, y, "✍️ User Feedback:")
        y -= 20
        text = c.beginText(70, y)
        text.setFont("Helvetica-Oblique", 10)
        for line in user_feedback.splitlines():
            text.textLine(line)
            y -= 14
        c.drawText(text)

    c.save()
    buffer.seek(0)

    st.success("✅ PDF report generated successfully!")
    st.download_button(
        label="📥 Download Risk Report (PDF)",
        data=buffer,
        file_name="OliRisk_Risk_Report.pdf",
        mime="application/pdf"
    )
