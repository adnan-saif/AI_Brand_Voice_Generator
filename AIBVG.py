import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import pyperclip
import os

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    st.error("❌ No API key found. Please add it to your .env file.")

model = genai.GenerativeModel("gemini-2.0-flash")

# FUNCTIONS
def learn_brand_voice(sample_texts):
    prompt = (
        "You are an AI marketing writer. Analyze these samples to deeply learn their tone, "
        "vocabulary, emotional style, and sentence rhythm.\n\n"
    )
    for i, text in enumerate(sample_texts, start=1):
        prompt += f"Example {i}: {text.strip()}\n"
    prompt += (
        "\nFrom these examples, infer the following:\n"
        "- Writing tone (e.g., formal, playful, confident)\n"
        "- Emotional attitude (e.g., inspiring, friendly, authoritative)\n"
        "- Vocabulary patterns (e.g., simple, descriptive)\n"
        "- Sentence rhythm and perspective\n"
        "\nUse this style in all future content generations. Do not output analysis unless asked."
    )
    return prompt


def generate_brand_content(brand_prompt, brand_name, purpose, content_type):
    topic = f"{brand_name} - {purpose}"

    templates = {
    "Social Media Post": f"""
Example 1:
Brand: TrendyTech
Post: "Looking to make your home smarter? \TrendyTech brings the future to your fingertips with the latest in smart home technology! 🏠✨
With our cutting-edge devices, you can automate lights, security systems, thermostats, and appliances effortlessly. Imagine controlling your entire home 🏡 from a single app 📱, saving time, energy, and reducing stress. Whether it’s setting the perfect lighting mood ✨ for a cozy evening 🌙, or ensuring your home is secure while you’re away 🔒, TrendyTech makes life easier and more enjoyable.
Upgrade your lifestyle today and experience the ultimate in modern living 🌟. Explore our range now and transform your home into a smart, connected haven!
#SmartHome #Innovation #TrendyTech #SmartLiving #HomeAutomation #FutureReady"

Example 2:
Brand: HealthBuddy
Post: "Struggling to stay on track with your fitness goals? 🌿 HealthBuddy makes wellness simple and fun, helping you take control of your health journey! 💪✨
Track your daily progress, get personalized tips, and receive motivation tailored to your lifestyle. From workout reminders 🏃‍♂️ to nutrition guidance, HealthBuddy supports you every step of the way. Feel empowered, stay consistent, and make healthy living an enjoyable habit.
Start your wellness journey today! 🌟 Join thousands already improving their health, staying active, and feeling their best with HealthBuddy.
#HealthBuddy #Wellness #FitnessJourney #HealthyLife #StayMotivated #LiveWell"

Now create a social media post about '{topic}'.
- Start with a hook that grabs attention.
- Include storytelling, benefits, or value in the middle.
- End with a clear call-to-action.
- Add some emojis in paragraphs.
- Maximum of 2-3 paragraphs.
- Do NOT use bold words.
- Ends with multiple relevant hashtags.
- Only output the post; do NOT include analysis or explanations.
""",

    "Email": f"""
Example 1:
Brand: TrendyTech
Subject: Upgrade Your Home Today with TrendyTech
Dear [Recipient],
Looking to simplify and elevate your daily life? TrendyTech brings the latest in smart home technology right to your fingertips. Our devices allow you to automate lights, security systems, thermostats, and appliances effortlessly, giving you more time to focus on what matters most. Imagine arriving home to the perfect ambiance every day, or checking your security systems while on the go – all from a single, easy-to-use app.
Experience the convenience, efficiency, and peace of mind that comes with a fully connected home. TrendyTech is designed to make your life easier, safer, and more enjoyable, whether you’re relaxing at home or managing your day remotely.
Explore our range of smart home solutions today and take the first step towards a smarter, more connected lifestyle. Don’t wait – transform your home into a hub of comfort and innovation now!
Best regards,
TrendyTech Team

Example 2:
Brand: HealthBuddy
Subject: Take Charge of Your Health with HealthBuddy
Hello [Recipient],
Achieving your wellness goals just got simpler and more effective with HealthBuddy. Our platform helps you track your daily progress, stay motivated with personalized tips, and maintain healthy habits with ease. Whether your focus is fitness, nutrition, or overall wellbeing, HealthBuddy provides the guidance and support you need every step of the way.
Join thousands of users who are improving their health, staying consistent with their routines, and feeling their best every day. With HealthBuddy, you’ll have the tools and encouragement to turn your goals into lasting habits.
Sign up today to start your personalized health journey and unlock the full potential of a healthier, more vibrant lifestyle. Your best self is waiting – take the first step now!
Warm regards,
HealthBuddy Team

Write a professional marketing email about '{topic}'.
Format:
Subject: <catchy subject line>
Greeting: Dear [Recipient],
Body: <well-structured paragraphs with appealing contents>
Call-to-action: <what the reader should do>
Sign-off: Best regards, [Brand Name]
Only output the email; do NOT include analysis, explanations and do NOT include the formate headings (Greeting, Body, Call-to-action, Sign-off).
""",

    "Tagline": f"""
Example 1:
Brand: TrendyTech
Taglines:
1. "Smart Living, Simplified"
2. "Innovation at Your Fingertips"
3. "Tomorrow’s Home Today"

Example 2:
Brand: HealthBuddy
Taglines:
1. "Your Health, Your Way"
2. "Wellness Made Easy"
3. "Stay Motivated, Stay Healthy"

Now create 3 short, catchy taglines for '{topic}' in the brand voice.
- Label each tagline with option.
- Only output the taglines.
- Do NOT use bold words.
""",

    "Ad Headline": f"""
Example 1:
Brand: TrendyTech
Headlines:
Option 1: "Transform Your Home with Smart Innovation Today"
Option 2: "Experience Effortless Living with TrendyTech Devices"
Option 3: "Upgrade Every Corner of Your Home Instantly"

Example 2:
Brand: HealthBuddy
Headlines:
Option 1: "Take Control of Your Health and Wellness Now"
Option 2: "Stay Fit, Stay Motivated, Achieve Your Goals"
Option 3: "Your Personalized Health Journey Starts Today"

Now generate 3 catchy ad headlines for '{topic}'.
- Each headline under 10 words.
- Focus on clarity, emotion, and curiosity.
- Label each as "Option 1", "Option 2", "Option 3".
- Only output the headlines; do NOT include analysis or explanations.
""",

    "Blog Intro": f"""
Example 1:
Brand: TrendyTech
Intro: "Smart homes are no longer the future—they’re here. TrendyTech offers innovative devices that make daily life effortless and enjoyable."

Example 2:
Brand: HealthBuddy
Intro: "Maintaining wellness can be challenging, but HealthBuddy simplifies the process with tools and guidance to stay on track every day."

Now write an engaging introduction for a blog post about '{topic}'.
- Hook the reader and provide context.
- Only output the blog intro.
- Do NOT include heading like (Brand:).
- Do NOT use bold words.
"""
}
    content_template = templates.get(content_type, templates["Social Media Post"])
    final_prompt = f"{brand_prompt}\n\n{content_template}"

    try:
        response = model.generate_content(final_prompt)
        return response.text.strip()
    except Exception as e:
        return f"[Error] Failed to generate content: {str(e)}"

# STREAMLIT UI
st.set_page_config(page_title="AI Brand Voice Generator", layout="wide", page_icon="🤖")

# MAIN PAGE
st.title("🤖 AI Brand Voice Generator")
st.markdown("""
Welcome to the **AI Brand Voice Generator** — a powerful tool that helps you instantly create high-quality, brand-consistent marketing content.

Provide a few examples of your brand's voice, and the AI will generate:
- 📢 Social media posts
- 📧 Professional emails
- 📝 Blog intros
- 🔤 Taglines & Ad Headlines

Perfect for marketers, founders, and content creators who want speed without losing the brand feel.
""")

# SIDEBAR
with st.sidebar:
    st.header("⚙️ Content Settings")

    brand_name = st.text_input("Brand Name", placeholder="e.g., TrendyTech")
    purpose = st.text_input("Campaign Purpose / Topic", placeholder="e.g., Launching new product")

    sample_text_input = st.text_area(
        "Sample Brand Texts (one per line)",
        placeholder="Example:\nSmart Living, Simplified\nInnovation at your fingertips\nUpgrade your home effortlessly",
        height=175
    )
    sample_texts = [s.strip() for s in sample_text_input.split("\n") if s.strip()]

    content_type = st.selectbox(
        "Content Type",
        ["Social Media Post", "Email", "Tagline", "Ad Headline", "Blog Intro"]
    )

    generate_btn = st.button("🚀  Generate Content")

# OUTPUT SECTION
st.subheader("Generated Content")

generated_text = st.session_state.get("generated_text", "")

generated_text = st.text_area(
    "Generated Output",
    value=generated_text,
    height=350,
    placeholder="Your generated content will appear here..."
)

if generate_btn:
    if not brand_name or not purpose or not sample_texts:
        st.warning("⚠️ Please fill in all the fields to generate content.")
    else:
        with st.spinner("Learning brand voice and generating content..."):
            brand_prompt = learn_brand_voice(sample_texts)
            generated_text = generate_brand_content(
                brand_prompt, brand_name, purpose, content_type
            )
            st.session_state.generated_text = generated_text

        st.rerun()

if st.button("📋 Copy to Clipboard") and generated_text:
    try:
        pyperclip.copy(generated_text)
        st.success("✅ Text copied to clipboard!")
    except Exception as e:
        st.error(f"❌ Could not copy text: {e}")


# CHANGES SECTION
st.subheader("Edit Section")

feedback_text = st.text_area(
    "Provide your feedback or suggested changes for the generated content:",
    height=100,
    placeholder="E.g., make it more playful, add more emojis, shorten paragraphs..."
)

if st.button("🔄 Apply Changes") and generated_text and feedback_text:
    with st.spinner("Applying feedback and updating content..."):
        feedback_prompt = (
            f"Original Content:\n{generated_text}\n\n"
            f"Feedback / Changes Requested:\n{feedback_text}\n\n"
            "Revise the original content to reflect the feedback while keeping the brand voice. "
            "Only output the revised content, do NOT include explanations or analysis."
        )
        try:
            revised_response = model.generate_content(feedback_prompt)
            revised_text = revised_response.text.strip()
            st.session_state.generated_text = revised_text
            st.rerun() 
        except Exception as e:
            st.error(f"❌ Failed to apply feedback: {e}")


# ABOUT SECTION
st.markdown("---")
st.markdown(
    '<h2 style="text-align: center;">About This Project</h2>',
    unsafe_allow_html=True
)

st.markdown("""
An intelligent tool designed to help marketers, startups, and creators produce professional, brand-consistent marketing content in seconds.

This project leverages the power of **Google Gemini** to **analyze your brand’s tone, vocabulary, emotional style, and rhythm** through sample texts you provide. Using this understanding, it can generate a variety of marketing content that stays true to your unique voice — saving time while maintaining quality.

#### 🎯 **What This App Does**
- **Understands Your Brand Voice:** Learns from your sample taglines, posts, or emails.
- **Generates Multiple Content Formats:** Instantly create social media posts, emails, taglines, ad headlines, and blog intros.
- **Keeps Consistency:** Ensures every output matches your original tone and style.
- **Boosts Productivity:** Perfect for marketing teams, freelancers, or businesses wanting to scale their content creation.

#### 🚀 **How It Works**
1. Enter your **brand name** and **campaign purpose**.
2. Provide **sample brand texts** (e.g., taglines, past emails, posts).
3. Choose the **type of content** you want to generate.
4. The app uses Google Gemini to generate content that reflects your brand's identity.

#### 🛠️ **Tech Stack**
- **Google Generative AI (Gemini)** – for natural language generation
- **Streamlit** – for the interactive and clean user interface
- **Python** – for backend logic and prompt construction

This tool is ideal for creating compelling marketing materials quickly while maintaining the authentic voice of your brand.
Feel free to experiment, iterate, and build your next campaign effortlessly!
""")

