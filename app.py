import streamlit as st
import re
import os
import tempfile
import time
from google import genai

# ---------------------------------------------------------
# UI CONFIGURATION & STYLING
# ---------------------------------------------------------
st.set_page_config(page_title="Multimodal Presentation AI", page_icon="🎬", layout="wide")

st.title("Multimodal Animated Presentation Architect")
st.markdown("Upload Videos, Images, and PDFs. The AI will analyze the media and generate a cinematic, animated Reveal.js HTML presentation.")

# ---------------------------------------------------------
# SIDEBAR: CREDENTIALS & SETTINGS
# ---------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Gemini API Key", type="password", help="Required to process Videos and Images.")
    active_model = st.text_input("Agentic Model", value="gemini-2.5-flash", help="Flash is highly optimized for video/multimodal processing.")
    theme = st.selectbox("Presentation Theme", ["dracula", "moon", "night", "league", "white", "black"])
    transition = st.selectbox("Animation Style", ["zoom", "slide", "convex", "concave", "fade"])
    st.markdown("---")
    st.markdown("**Output Engine**: Reveal.js HTML (Cinematic Web Presentation)")

# ---------------------------------------------------------
# MULTIMODAL AGENT LOGIC
# ---------------------------------------------------------
def generate_animated_presentation(api_key: str, prompt: str, theme: str, transition: str, model_id: str, source_files: list) -> str:
    """Uploads multimodal files to Gemini and generates a Reveal.js HTML presentation."""
    
    client = genai.Client(api_key=api_key)
    gemini_uploaded_files = []
    
    try:
        # Step 1: Upload Files to Gemini API
        if source_files:
            st.info(f"📤 Securely uploading {len(source_files)} media file(s) for AI analysis...")
            
            # Create a progress bar for the upload/processing phase
            progress_bar = st.progress(0)
            
            for i, uploaded_file in enumerate(source_files):
                file_extension = os.path.splitext(uploaded_file.name)[1]
                with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
                    temp_file.write(uploaded_file.read())
                    temp_file_path = temp_file.name

                # Upload to Gemini
                g_file = client.files.upload(file=temp_file_path, config={'display_name': uploaded_file.name})
                gemini_uploaded_files.append(g_file)
                os.remove(temp_file_path) 
                
                progress_bar.progress((i + 1) / len(source_files))

            # Step 2: Poll for Video Processing Completion
            st.info("⏳ AI is watching videos and analyzing images/PDFs... (This may take a minute for large videos)")
            for i, g_file in enumerate(gemini_uploaded_files):
                def get_state(f): return f.state.name if hasattr(f.state, 'name') else f.state
                
                while get_state(g_file) == "PROCESSING":
                    time.sleep(3)
                    g_file = client.files.get(name=g_file.name)
                    gemini_uploaded_files[i] = g_file 
                
                if get_state(g_file) == "FAILED":
                    st.warning(f"⚠️ Media {g_file.display_name} could not be processed.")

        # Step 3: Prompting the Agent for Reveal.js Generation
        st.info(f"🎬 Synthesizing knowledge and writing Animated Reveal.js Code...")
        
        system_instruction = (
            "You are a master Web Developer and Presentation Designer. "
            "Your task is to analyze the provided documents, images, and videos, and synthesize them into a highly engaging, "
            "animated Reveal.js HTML presentation based on the user's topic.\n\n"
            "STRICT REQUIREMENTS:\n"
            f"1. Create a complete, standalone HTML file using the Reveal.js CDN.\n"
            f"2. Use the '{theme}' theme and '{transition}' slide transitions.\n"
            f"3. Organize the content logically into `<section>` tags.\n"
            f"4. Format the text beautifully using standard HTML elements (h1, h2, ul, li).\n"
            f"5. OUTPUT ONLY VALID HTML CODE. Do not include markdown formatting like ```html. Start exactly with <!DOCTYPE html>."
        )

        user_instruction = f"Slide Topic / Instructions: {prompt}"
        
        # Combine uploaded media files and the text prompt
        contents = gemini_uploaded_files + [system_instruction, user_instruction]
        
        response = client.models.generate_content(
            model=model_id,
            contents=contents
        )
        
        # Clean markdown formatting if the model accidentally includes it
        html_output = response.text
        if html_output.startswith("```html"):
            html_output = html_output.replace("```html", "", 1)
        if html_output.endswith("```"):
            html_output = html_output[::-1].replace("```", "", 1)[::-1]
            
        return html_output.strip()

    finally:
        # Step 4: Cleanup API Files to save quota
        if gemini_uploaded_files:
            st.info("🧹 Wiping media from AI servers...")
            for g_file in gemini_uploaded_files:
