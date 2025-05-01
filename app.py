import streamlit as st
import requests

# Set Streamlit page config
st.set_page_config(page_title="🚀 TrendWhiz", page_icon="🎯")

st.title("🚀 TrendWhiz")
st.markdown("AI-Powered Content & Campaign Idea Generator 🌟")

# User Inputs
brand = st.text_input("📝 Brand or Product Name")
audience = st.selectbox(
    "🎯 Target Audience",
    ("Gen Z (18-24)", "Millennials (25-40)", "Gen X (41-56)", "Boomers (57+)", "Parents", "Students", "Professionals")
)
platform = st.selectbox(
    "📱 Social Media Platform",
    ("Instagram", "Facebook", "TikTok", "YouTube", "LinkedIn", "Pinterest", "Twitter / X")
)
goal = st.text_area("🎯 Campaign Goal", placeholder="e.g., Increase brand awareness, drive engagement...")

# Groq API Key (Put your key here or use Streamlit secrets)
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY")

# Function to call Groq API with Llama3
def generate_campaign_ideas(brand, audience, platform, goal):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {
                "role": "system",
                "content": "You are a professional social media marketing expert. Generate exactly 5 unique, creative, and actionable campaign ideas. Each idea should suggest post formats, influencer collaboration, and engagement tips. Use fun and engaging language with emojis."
            },
            {
                "role": "user",
                "content": f"""Generate exactly 5 creative social media campaign ideas for brand '{brand}', targeting '{audience}' on '{platform}'.
Goal: {goal}.
Format ideas clearly as:
1. 🎯 Idea 1...
2. 🚀 Idea 2...
3. 🌟 Idea 3...
4. 🎉 Idea 4...
5. 💡 Idea 5...
Each idea must be actionable and unique."""
            }
        ],
        "temperature": 0.7,
        "max_tokens": 800,
        "top_p": 0.95
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
    return result['choices'][0]['message']['content']

# Generate Button
if st.button("✨ Generate  Campaign Ideas"):
    if not brand or not goal:
        st.warning("⚠️ Please enter both the Brand Name and Campaign Goal.")
    else:
        with st.spinner("💡 Generating creative ideas... please wait..."):
            try:
                output = generate_campaign_ideas(brand, audience, platform, goal)
                st.success("🎉 Generated 5 unique campaign ideas!")
                st.markdown(output)
                st.balloons()
            except Exception as e:
                st.error(f"⚠️ Error: {e}")
