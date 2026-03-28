🌿 Green-Truth Auditor
An AI-powered sustainability and greenwashing detection system that analyzes brands, websites, and product descriptions to determine whether environmental claims are genuine, suspicious, or greenwashing.

Project Overview
Green-Truth Auditor uses a hybrid AI system combining:
Transformer-based Natural Language Inference (NLI) model
Rule-based keyword detection
Verified brand database matching

a)Datasets Used and Preprocessing:-

The project uses a custom dataset:
🔹 brands.csv
Contains verified brand information.linke brand, certification,website
we have used pre process data

b) model and its accuracy/performance metrics:
BART large MNLI model(used for test classifivcatin) classification


Performance Metrics
🎯 Uses confidence scores (probability values) instead of fixed accuracy
📈 Outputs label with highest probability
🧠 Strong performance in understanding semantic meaning
⚡ No training required for custom labels (zero-shot capability)

c)key features:
🔍 AI Claim Detection – Classifies text as Marketing Fluff or Evidence-Based Claim using BART MNLI model
🏢 Brand Verification – Checks brands using a certified CSV database and website domain matching
🌐 Web Scraping – Extracts and analyzes real website content
🧠 Hybrid AI System – Combines AI model + rule-based logic + certification checks
📊 Trust Score (0–100) – Generates final credibility score for sustainability claims
🚩 Buzzword Detection – Identifies misleading green marketing terms
📊 Proof Detection – Detects certified/evidence-based keywords
🖥️ Streamlit UI – Simple interactive dashboard for input and results
🎯 Final Verdict – Outputs GENUINE / SUSPICIOUS / GREENWASHING status
🧾 Explainable Results – Shows reasoning behind AI decision
