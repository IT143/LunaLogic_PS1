import streamlit as st
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

# -------------------------------
# Buzzwords (expanded but not over-noisy)
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
st.caption("Rule-based NLP with sentence-level analysis + brand verification (RAG-ready)")

user_input = st.text_area("Enter product description")
url = st.text_input("Or paste product URL")
brand = st.text_input("Enter brand (optional)")

# -------------------------------
# Analyze
# -------------------------------
if st.button("Analyze"):
    text = user_input.strip()

    # URL extraction
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
    # Weighted scoring (balanced)
    # -------------------------------
    score = 100

    # buzzword density penalty
    score -= min(len(found_buzz) * 8, 40)

    # no proof penalty
    if not proof:
        score -= 30

    # negative signal penalty
    if negative:
        score -= 20

    # quantitative claims bonus
    if numbers:
        score += 8

    score = max(0, min(score, 100))

    # -------------------------------
    # Classification (handles mixed)
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
        reason = "Verifiable evidence/certifications found without reliance on vague buzzwords."
    elif result == "⚠️ Mixed Claim":
        reason = f"Contains evidence but also uses vague terms: {', '.join(found_buzz)}."
    elif result == "❌ Greenwashing":
        reason = f"Relies on buzzwords without proof: {', '.join(found_buzz)}."
    elif result == "❌ Risky Claim":
        reason = "Contains negative or risky environmental signals."
    else:
        reason = "Insufficient information to verify sustainability."

    # -------------------------------
    # Output
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

    # Verdict
    if score >= 70:
        st.success("🌟 Verdict: Trustable")
    elif score >= 40:
        st.warning("⚠️ Verdict: Needs Verification")
    else:
        st.error("❌ Verdict: High Greenwashing Risk")

    if found_buzz:
        st.write("⚠️ Buzzwords detected:", ", ".join(found_buzz))

    # -------------------------------
    # Brand check (CSV RAG)
    # -------------------------------
    try:
        df = pd.read_csv("brands.csv")
        if brand.strip():
            match = df[df["brand"].str.lower() == brand.lower()]
            if not match.empty:
                b = match.iloc[0]
                st.info(
                    f"Brand: {b['brand']}\n\n"
                    f"Certification: {b['certified']}\n\n"
                    f"Category: {b['category']}\n\n"
                    f"Notes: {b['notes']}"
                )
            else:
                st.warning("Brand not found in database")
    except:
        st.warning("brands.csv not found")

    # Debug (for judges)
    with st.expander("🔎 What we detected"):
        st.write("Buzzwords:", found_buzz if found_buzz else "None")
        st.write("Proof present:", proof)
        st.write("Negative signals:", negative)
        st.write("Numbers present:", numbers)
