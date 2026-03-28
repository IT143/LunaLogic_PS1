import streamlit as st
import re

# -------------------------------
# Buzzwords list
# -------------------------------
buzzwords = [
    "eco-friendly", "natural", "green", "organic",
    "sustainable", "non-toxic", "biodegradable"
]

# -------------------------------
# Detect buzzwords
# -------------------------------
def detect_buzzwords(text):
    return [word for word in buzzwords if word in text.lower()]

# -------------------------------
# Check proof (certifications/data)
# -------------------------------
def has_proof(text):
    proof_keywords = [
        "certified", "ISO", "GOTS", "FSC",
        "%", "recycled", "carbon neutral"
    ]
    return any(word.lower() in text.lower() for word in proof_keywords)

# -------------------------------
# Detect numbers (extra smart feature)
# -------------------------------
def has_numbers(text):
    return bool(re.search(r'\d', text))

# -------------------------------
# Generate explanation
# -------------------------------
def generate_reason(found_buzz, proof):
    if found_buzz and not proof:
        return f"This product uses vague terms like {', '.join(found_buzz)} without any real proof."
    elif proof:
        return "This product includes certifications or measurable sustainability data."
    else:
        return "The claim is unclear and lacks sufficient details."

# -------------------------------
# UI STARTS HERE
# -------------------------------
st.title("🌱 Green-Truth Auditor")
st.write("Detect greenwashing in product descriptions")

# Input box
user_input = st.text_area("Enter product description:")

# Button
if st.button("Analyze"):

    if user_input.strip() == "":
        st.warning("Please enter some text")

    else:
        # Process
        found_buzz = detect_buzzwords(user_input)
        proof = has_proof(user_input)
        numbers = has_numbers(user_input)

        # Score system
        score = 100

        if found_buzz:
            score -= 40

        if not proof:
            score -= 40

        if numbers:
            score += 10

        # Classification
        if found_buzz and not proof:
            result = "❌ Greenwashing"
        elif proof:
            result = "✅ Genuine"
        else:
            result = "⚠️ Unclear"

        # Explanation
        reason = generate_reason(found_buzz, proof)

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
        st.progress(score / 100)

        st.write(f"💡 Reason: {reason}")

        if found_buzz:
            st.write("⚠️ Buzzwords detected:", ", ".join(found_buzz))