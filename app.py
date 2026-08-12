import streamlit as st
import re
import os
import tempfile
from collections import Counter
from pypdf import PdfReader

# ---------------------------------------------------------
# UI CONFIGURATION & STYLING
# ---------------------------------------------------------
st.set_page_config(page_title="Deterministic Presentation Architect", page_icon="📊", layout="wide")

st.title("Extractive NLP Presentation Generator")
st.markdown("Upload source materials (PDFs/TXT) and generate a presentation using deterministic statistical summarization (Zero Generative AI).")

with st.sidebar:
    st.header("⚙️ Configuration")
    slide_count = st.slider("Target Slide Count", min_value=5, max_value=25, value=10)
    visual_style = st.selectbox("Visual Theme", ["default", "gaia", "uncover"])
    st.markdown("---")
    st.markdown("**Engine**: Pure Python Extractive NLP\n**Render Strategy**: Marp Markdown")

# ---------------------------------------------------------
# DETERMINISTIC NLP LOGIC (EXTRACTIVE SUMMARIZATION)
# ---------------------------------------------------------
def extract_text(uploaded_files) -> str:
    """Extracts raw text from uploaded PDF and TXT files."""
    combined_text = ""
    for uploaded_file in uploaded_files:
        if uploaded_file.name.endswith('.pdf'):
            pdf_reader = PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    combined_text += text + "\n "
        elif uploaded_file.name.endswith('.txt'):
            combined_text += uploaded_file.getvalue().decode("utf-8") + "\n "
    return combined_text

def extractive_summarization(text: str, num_sentences: int) -> list:
    """
    Uses mathematical word frequency to score and extract the most important sentences.
    This guarantees 0% hallucination as it only pulls exact quotes from the text.
    """
    # 1. Clean and split into sentences based on punctuation
    text = text.replace('\n', ' ')
    sentences = re.split(r'(?<=[.!?]) +', text)
    
    # 2. Define basic stopwords to ignore in scoring
    stopwords = {'the', 'is', 'in', 'and', 'to', 'of', 'a', 'with', 'for', 'on', 'as', 'by', 'an', 'that', 'this', 'it', 'are', 'from', 'be', 'or'}
    
    # 3. Calculate word frequencies across the entire document
    words = re.findall(r'\w+', text.lower())
    word_counts = Counter(w for w in words if w not in stopwords)
    
    # 4. Score each sentence based on the frequency of its words
    scores = {}
    for i, sentence in enumerate(sentences):
        sentence_words = re.findall(r'\w+', sentence.lower())
        score = sum(word_counts.get(w, 0) for w in sentence_words)
        
        # Normalize by length to favor medium-length, dense sentences (avoiding 3-word or 100-word sentences)
        word_count = len(sentence_words)
        if 8 < word_count < 35: 
            scores[i] = score / word_count
        else:
            scores[i] = 0

    # 5. Extract the top-scoring sentences and sort them back into chronological order
    top_indices = sorted(scores, key=scores.get, reverse=True)[:num_sentences]
    top_indices.sort() 
    
    return [sentences[i].strip() for i in top_indices if sentences[i].strip()]

def build_marp_presentation(sentences: list, target_slides: int, theme: str) -> str:
    """Chunks the extracted sentences into Markdown presentation slides."""
    
    # Standard Marp YAML Frontmatter
    md = f"---\nmarp: true\ntheme: {theme}\npaginate: true\n---\n\n"
    md += "# Executive Summary\n\n*An automatic extraction from source documents.*\n\n---\n\n"
    
    # Calculate how many sentences to put on each slide (approx 3-4 per slide)
    sentences_per_slide = max(1, len(sentences) // target_slides)
    
    slide_number = 1
    for i in range(0, len(sentences), sentences_per_slide):
        chunk = sentences[i:i + sentences_per_slide]
        if not chunk:
            continue
            
        md += f"## Key Findings: Section {slide_number}\n\n"
        for sentence in chunk:
            md += f"- {sentence}\n"
        md += "\n---\n\n"
        slide_number += 1
        
    # Remove the very last '---' separator to cleanly end the file
    return md.strip().rstrip("---").strip()

# ---------------------------------------------------------
# MAIN INTERFACE
# ---------------------------------------------------------
st.markdown("### 1. Upload Source Materials (Required)")
uploaded_source_files = st.file_uploader(
    "Upload PDFs or Text files (.txt). The algorithm will extract the most mathematically significant sentences.", 
    accept_multiple_files=True,
    type=['pdf', 'txt']
)

if st.button("🚀 Generate Deterministic Presentation"):
    if not uploaded_source_files:
        st.warning("Please upload at least one source file to process.")
    else:
        with st.spinner("Analyzing document statistics and extracting data..."):
            try:
                # Step 1: Extract Text
                raw_text = extract_text(uploaded_source_files)
                
                if len(raw_text.strip()) < 100:
                    st.error("Not enough text could be extracted from these files. Ensure PDFs are text-searchable (not just images).")
                else:
                    # Step 2: Calculate target sentences (e.g., 10 slides * 3 bullet points = 30 sentences)
                    target_sentences = slide_count * 3
                    
                    # Step 3: Extractive Summarization
                    top_sentences = extractive_summarization(raw_text, target_sentences)
                    
                    # Step 4: Build Presentation
                    final_markdown = build_marp_presentation(top_sentences, slide_count, visual_style)
                    
                    st.success("✅ Presentation successfully generated based purely on document data!")
                    
                    # Display output
                    st.markdown("### Marp Markdown Source")
                    st.code(final_markdown, language="markdown")
                    
                    # Provide Download Button
                    st.download_button(
                        label="📥 Download .md File (Ready for Marp)",
                        data=final_markdown,
                        file_name="extractive_presentation.md",
                        mime="text/markdown"
                    )

            except Exception as e:
                st.error(f"Processing Error: {str(e)}")
