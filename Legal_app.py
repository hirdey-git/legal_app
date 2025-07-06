import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
import re


# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Build structured legal prompt
def build_legal_prompt(jurisdiction, area_of_law, user_role, user_question):
    prompt = f"""
You are a legally accurate AI assistant. Your task is to answer questions using **only reliable, publicly available legal sources**. You must follow these restrictions:

Use only:
- U.S. Code (https://uscode.house.gov)
- Code of Federal Regulations (CFR)
- Official state statutes and constitutions
- Court decisions (via Justia, CourtListener, or court websites)
- Guidance from U.S. agencies (e.g., DOJ, FTC, IRS, EEOC)
- Legal Information Institute (Cornell)
- American Bar Association (publicly available resources)
- Congressional Research Service (CRS)
Do **NOT** use proprietary databases like Westlaw or LexisNexis or unverified commentary. Do **NOT** give legal advice.

---

Context:
- **Jurisdiction**: {jurisdiction}
- **Legal Domain**: {area_of_law}
- **User Role**: {user_role}

User Question:
\"\"\"{user_question.strip()}\"\"\"

---

Follow this format:

*Answer:* [Provide a legally accurate and well-cited answer]  
*Confidence Level:* [High / Medium / Low]  
*Supporting Sources Used:* [List public legal sources]  
*Validation Notes:* [Explain how the answer was validated or any limitations]  
*Citation Links:* [Direct links to the sources if available]
"""
    return prompt

# Call OpenAI with constructed prompt
def get_legal_answer(prompt):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500,
        temperature=0.0
    )
    return response.choices[0].message.content.strip()

# Streamlit UI
st.set_page_config(page_title="Legal QA Assistant", layout="centered")
st.title("⚖️ Legal QA Assistant")

st.markdown("""
Provide key details below so the assistant can give a **precise, jurisdiction-aware** response based on **public legal sources** only.
""")

jurisdiction = st.text_input("🔍 Jurisdiction (e.g., California, U.S. Federal, New York)", value="U.S. Federal")
area_of_law = st.selectbox("📚 Area of Law", [
    "Contract Law", "Employment Law", "Criminal Law", "Family Law",
    "Intellectual Property", "Civil Procedure", "Corporate Law",
    "Tax Law", "Real Estate Law", "Immigration Law", "Other"
])
user_role = st.selectbox("👤 Your Role", [
    "Attorney", "Paralegal", "Law Student", "Compliance Officer", "In-house Counsel", "General Research"
])
user_question = st.text_area("📝 Enter your legal question or issue:", height=180)

if st.button("Get Answer") and user_question.strip():
    with st.spinner("Generating a legally verified response..."):
        try:
            prompt = build_legal_prompt(jurisdiction, area_of_law, user_role, user_question)
            answer = get_legal_answer(prompt)
            st.success("Response:")
            st.markdown(answer)
        except Exception as e:
            st.error(f"Error: {str(e)}")
else:
    st.info("Please fill all fields and click 'Get Answer'.")

