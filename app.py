import streamlit as st
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

# -------------------------------
# Buzzwords
# -------------------------------
buzzwords = [
    "eco-friendly","environmentally friendly","green","natural","organic",
    "sustainable","sustainably","biodegradable","compostable","non-toxic",
    "clean","pure","chemical-free","eco","earth-friendly","planet-friendly",
    "low-impact","net zero","climate positive","eco conscious","eco-conscious",
    "green product","safe for nature","responsibly made","ethical","clean beauty"
]

# -------------------------------
# Negative signals
# -------------------------------
negative_words = [
    "no proof","not certified","unknown source","no evidence",
    "chemical","pollution","waste","fast fashion","toxic","hazardous"
]

# -------------------------------
# Helpers
# -------------------------------
def get_text_from_url(url):
    try:
        r = requests.get(url, timeout=5, headers={"User-Agent":"Mozilla/5.0"})
        soup = BeautifulSoup(r.text, "html.parser")
        return soup.get_text(" ", strip=True)
    except:
        return ""

def split_sentences(text):
    return [s.strip() for s in re.split(r'[.!?]', text) if s.strip()]

def detect_buzzwords(text):
    t = text.lower()
    return [w for w in buzzwords if w in t]

def has_proof(text):
    proof_keywords = [
        "certified","iso","gots","fsc","energy star","cradle to cradle",
        "carbon neutral","carbon-negative","verified","audit","lca",
        "life cycle analysis","%","recycled","recyclable","traceable",
        "third-party","third party","scope 1","scope 2","scope 3"
    ]
    t = text.lower()
    return any(k in t for k in proof_keywords)

def has_numbers(text):
    return bool(re.search(r'\d', text))

def has_negative(text):
    t = text.lower()
    return any(w in t for w in negative_words)

# -------------------------------
# UI
# -------------------------------
st.title("🌱 Green-Truth Auditor")
st.caption("Rule-based NLP with sentence-level analysis + brand verification")

user_input = st.text_area("Enter product description")
url = st.text_input("Or paste product URL")
brand = st.text_input("Enter brand (optional)")
advanced_mode = st.checkbox("🔮 Enable Advanced AI Mode (Future Feature)")

# -------------------------------
# Analyze
# -------------------------------
if st.button("Analyze"):
    text = user_input.strip()

    if url.strip():
        extracted = get_text_from_url(url)
        if extracted:
            text += " " + extracted
            st.info("Text extracted from URL")
        else:
            st.warning("Could not extract data from URL")

    if not text:
        st.warning("Please enter text or URL")
        st.stop()

    # -------------------------------
    # Sentence-level analysis
    # -------------------------------
    sentences = split_sentences(text)
    buzz_all = []
    proof_hits = 0

    for s in sentences:
        buzz_all += detect_buzzwords(s)
        if has_proof(s):
            proof_hits += 1

    found_buzz = list(set(buzz_all))
    proof = proof_hits > 0
    negative = has_negative(text)
    numbers = has_numbers(text)

    # -------------------------------
    # Scoring
    # -------------------------------
    score = 100
    score -= min(len(found_buzz) * 8, 40)

    if not proof:
        score -= 30

    if negative:
        score -= 20

    if numbers:
        score += 8

    score = max(0, min(score, 100))

    # -------------------------------
    # Classification
    # -------------------------------
    if proof and not found_buzz:
        result = "✅ Genuine"
    elif proof and found_buzz:
        result = "⚠️ Mixed Claim"
    elif found_buzz and not proof:
        result = "❌ Greenwashing"
    elif negative:
        result = "❌ Risky Claim"
    else:
        result = "⚠️ Unclear"

    # -------------------------------
    # Reason
    # -------------------------------
    if result == "✅ Genuine":
        reason = "Verifiable certifications found without vague claims."
    elif result == "⚠️ Mixed Claim":
        reason = f"Contains proof but also buzzwords: {', '.join(found_buzz)}."
    elif result == "❌ Greenwashing":
        reason = f"Uses buzzwords without evidence: {', '.join(found_buzz)}."
    elif result == "❌ Risky Claim":
        reason = "Contains risky environmental signals."
    else:
        reason = "Not enough information."

    # -------------------------------
    # OUTPUT
    # -------------------------------
    st.subheader("🔍 Result")

    if "Greenwashing" in result:
        st.error(result)
    elif "Genuine" in result:
        st.success(result)
    else:
        st.warning(result)

    st.write(f"🌍 Sustainability Score: {score}/100")
    st.progress(score/100)
    st.write(f"💡 Reason: {reason}")

    # -------------------------------
    # NEW FEATURES (WINNING PART)
    # -------------------------------

    # Scorecard
    st.markdown("### 📊 Sustainability Scorecard")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Buzzwords", len(found_buzz))
    with col2:
        st.metric("Evidence", "Yes" if proof else "No")
    with col3:
        st.metric("Risk Signals", "Yes" if negative else "No")

    # Sentence Analysis
    st.markdown("### 🔎 Sentence Analysis")
    for s in sentences:
        label = ""
        if detect_buzzwords(s):
            label += "⚠️ "
        if has_proof(s):
            label += "✅ "
        if has_negative(s):
            label += "❌ "
        if label:
            st.write(f"{label} → {s}")

    # Trust Badge
    if score >= 70:
        st.markdown("🟢 **Eco Trust Badge: VERIFIED**")
    elif score >= 40:
        st.markdown("🟡 **Eco Trust Badge: QUESTIONABLE**")
    else:
        st.markdown("🔴 **Eco Trust Badge: MISLEADING**")

    # Why it matters
    st.markdown("### 🌍 Why this matters")
    st.write("Helps users avoid greenwashing and promotes transparency.")

    # -------------------------------
    # Brand check
    # -------------------------------
    try:
        df = pd.read_csv("brands.csv")
        if brand.strip():
            match = df[df["brand"].str.lower() == brand.lower()]
            if not match.empty:
                b = match.iloc[0]
                st.info(f"""
Brand: {b['brand']}
Certification: {b['certified']}
Category: {b['category']}
Notes: {b['notes']}
""")
            else:
                st.warning("Brand not found")
    except:
        st.warning("brands.csv not found")

    # Debug
    with st.expander("🔎 Debug"):
        st.write("Buzzwords:", found_buzz)
        st.write("Proof:", proof)
        st.write("Negative:", negative)
