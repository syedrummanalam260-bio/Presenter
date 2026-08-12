import streamlit as st
import re
from google import genai
from google.genai import types

# ---------------------------------------------------------
# UI CONFIGURATION & STYLING
# ---------------------------------------------------------
st.set_page_config(page_title="AI Presentation Architect", page_icon="🧬", layout="wide")

st.title("Autonomous AI Presentation Generator")
st.markdown("Generate publication-ready slide decks using the Agentic Loop and Marp Markdown engine.")

# ---------------------------------------------------------
# SIDEBAR: CREDENTIALS & SETTINGS
# ---------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Gemini API Key", type="password", help="Enter your Google Gemini API key.")
    slide_count = st.slider("Target Slide Count", min_value=5, max_value=25, value=10)
    visual_style = st.selectbox("Visual Theme", ["default", "gaia", "uncover"])
    st.markdown("---")
    st.markdown("**Engine**: Gemini 3.6 Flash / Pro\n**Render Strategy**: Marp Markdown")

# ---------------------------------------------------------
# AGENTIC LOOP LOGIC
# ---------------------------------------------------------
def agentic_presentation_loop(api_key: str, prompt: str, slide_count: int, theme: str) -> str:
    """Executes a multi-agent workflow to research, draft, and refine a presentation."""
    
    # Initialize the standard Google GenAI client
    client = genai.Client(api_key=api_key)
    
    # Phase 1: Research & Outline (Simulating standard flash for speed)
    st.info("Phase 1: Agent researching and structuring outline...")
    outline_prompt = (
        f"Act as a Principal Research Scientist. Create a highly structured, logical outline for a "
        f"{slide_count}-slide presentation on the following topic:\n\n{prompt}\n\n"
        "Detail the title, main bullet points, and the scientific narrative flow for each slide."
    )
    outline_response = client.models.generate_content(
        model='gemini-3.6-flash',
        contents=outline_prompt
    )
    
    # Phase 2 & 3: Self-Critique, Refinement, and Code-to-Slide Generation (Simulating pro for complex formatting)
    st.info("Phase 2: Agent refining narrative and injecting Marp Markdown syntax...")
    marp_prompt = (
        f"Review the following presentation outline for scientific accuracy and flow:\n\n"
        f"{outline_response.text}\n\n"
        f"Now, convert this into a finalized, highly professional presentation using Marp Markdown format. "
        f"Strict Requirements:\n"
        f"1. Start with YAML frontmatter: `marp: true`, `theme: {theme}`, `paginate: true`.\n"
        f"2. Separate each slide with `---`.\n"
        f"3. Do not clutter slides with too much text. Use bullet points.\n"
        f"4. Where a diagram or chart is conceptually needed, use standard markdown image syntax with a placeholder: "
        f"![width:600px](https://via.placeholder.com/600x400?text=Insert+Diagram+Here).\n"
        f"Output ONLY the raw markdown block. Do not include conversational text."
    )
    
    final_response = client.models.generate_content(
        model='gemini-3.6-pro',
        contents=marp_prompt
    )
    
    # Clean output to extract just the markdown
    match = re.search(r"```markdown\n(.*?)```", final_response.text, re.DOTALL)
    if match:
        return match.group(1)
    
    # Fallback if the model didn't use code fences
    return final_response.text

# ---------------------------------------------------------
# MAIN INTERFACE
# ---------------------------------------------------------
user_prompt = st.text_area(
    "Enter your presentation topic or research abstract:",
    value="The Role of MicroRNA in Abiotic Stress Regulation: Special Emphasis on Millets",
    height=150
)

if st.button("🚀 Architect Presentation"):
    if not api_key:
        st.error("Please enter your Gemini API Key in the sidebar.")
    elif not user_prompt:
        st.warning("Please provide a presentation prompt.")
    else:
        with st.spinner("Initializing Agentic Loop..."):
            try:
                # Execute the loop
                final_markdown = agentic_presentation_loop(api_key, user_prompt, slide_count, visual_style)
                
                st.success("Presentation successfully generated!")
                
                # Display output
                st.markdown("### Marp Markdown Source")
                st.code(final_markdown, language="markdown")
                
                # Provide Download Button
                st.download_button(
                    label="📥 Download .md File (Ready for Marp)",
                    data=final_markdown,
                    file_name="scientific_presentation.md",
                    mime="text/markdown"
                )
                
                st.markdown(
                    "> **Next Step:** Install the [Marp for VS Code](https://marp.app/) extension, "
                    "open the downloaded `.md` file, and click the Marp icon to instantly export "
                    "to a beautifully animated PDF, HTML, or PowerPoint `.pptx` file."
                )

            except Exception as e:
                st.error(f"Pipeline Error: {str(e)}")
