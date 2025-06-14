import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
import os
import openai

# --- Set API key securely
openai.api_key = st.secrets["OPENAI_API_KEY"]

# --- Career Paths Definition
career_paths = {
    "STEM": ["technology", "engineering", "math", "science", "research"],
    "Arts": ["drawing", "writing", "music", "design", "film", "painting", "poetry"],
    "Business": ["marketing", "sales", "entrepreneurship", "finance"],
    "Sports": ["football", "fitness", "athletics", "coaching"],
    "Healthcare": ["medicine", "nursing", "psychology", "therapy"],
    "Social Work": ["nonprofits", "community service", "education"]
}

# --- Initialize OpenAI LLM
llm = ChatOpenAI(model="gpt-4", temperature=0.7)

# --- Prompt Template for Preference Extraction
extract_prompt = PromptTemplate.from_template("""
You are a career assistant. Based on the conversation below, extract the user's interests, skills, and personality traits.

Conversation:
{conversation}

Return JSON:
{{
  "interests": [...],
  "skills": [...],
  "personality_traits": [...]
}}
""")

# --- Prompt Template for Career Path Mapping
mapping_prompt = PromptTemplate.from_template("""
You are a career advisor. Based on this user profile, recommend 1–2 relevant career paths from the following list:
STEM, Arts, Business, Sports, Healthcare, Social Work.

Profile:
{profile}

Return JSON:
[
  {{
    "path": "STEM",
    "reason": "..."
  }}
]
""")

# --- Prompt Template for Fallback Clarification
fallback_prompt = """
I couldn't determine your interests clearly. Please answer these questions:
- What subjects or activities do you enjoy?
- Do you prefer working with people, data, or tools?
- What are your favorite hobbies?
"""

# --- Streamlit UI
st.set_page_config(page_title="Career Path", page_icon="🧭")
st.title("🧭 Career Path Recommendation")
st.markdown("Tell me about yourself, your interests, or what you enjoy doing.")

conversation = st.text_area("🗣️ Start typing your conversation here...", height=250)

if st.button("🔍 Get Recommendation"):
    if conversation.strip() == "":
        st.warning("Please enter some conversation text.")
    else:
        with st.spinner("Analyzing..."):
            # Step 1: Extract interests
            extract_input = extract_prompt.format(conversation=conversation)
            extraction = llm([HumanMessage(content=extract_input)]).content

            st.subheader("🔎 Extracted Info")
            st.code(extraction, language="json")

            if '"interests": []' in extraction:
                st.warning("Couldn't extract enough info. Please clarify:")
                st.markdown(fallback_prompt)
            else:
                # Step 2: Recommend career path
                mapping_input = mapping_prompt.format(profile=extraction)
                mapping = llm([HumanMessage(content=mapping_input)]).content

                st.subheader("🎯 Career Recommendation")
                st.code(mapping, language="json")
