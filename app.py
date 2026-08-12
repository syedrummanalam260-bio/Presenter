# ... existing code ...
# SIDEBAR: CREDENTIALS & SETTINGS
# ---------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Gemini API Key", type="password", help="Enter your Google Gemini API key.")
    slide_count = st.slider("Target Slide Count", min_value=5, max_value=25, value=10)
    visual_style = st.selectbox("Visual Theme", ["default", "gaia", "uncover"])
    
    # Adding a model selector in case API strings change in the future
    st.markdown("---")
    st.markdown("**Model Configuration**")
    active_model = st.text_input("Agentic Model", value="gemini-3.6-flash")
    
    st.markdown("---")
    st.markdown("**Render Strategy**: Marp Markdown")

# ---------------------------------------------------------
# AGENTIC LOOP LOGIC
# ---------------------------------------------------------
def agentic_presentation_loop(api_key: str, prompt: str, slide_count: int, theme: str, model_id: str) -> str:
    """Executes a multi-agent workflow to research, draft, and refine a presentation."""
    
    # Initialize the standard Google GenAI client
    client = genai.Client(api_key=api_key)
    
    # Phase 1: Research & Outline
    st.info(f"Phase 1: Agent researching and structuring outline using {model_id}...")
    outline_prompt = (
        f"Act as a Principal Research Scientist. Create a highly structured, logical outline for a "
        f"{slide_count}-slide presentation on the following topic:\n\n{prompt}\n\n"
        "Detail the title, main bullet points, and the scientific narrative flow for each slide."
    )
    outline_response = client.models.generate_content(
        model=model_id,
        contents=outline_prompt
    )
    
    # Phase 2 & 3: Self-Critique, Refinement, and Code-to-Slide Generation
    st.info(f"Phase 2: Agent refining narrative and injecting Marp Markdown syntax using {model_id}...")
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
        model=model_id,
        contents=marp_prompt
    )
    
    # Clean output to extract just the markdown
# ... existing code ...
        with st.spinner("Initializing Agentic Loop..."):
            try:
                # Execute the loop
                final_markdown = agentic_presentation_loop(
                    api_key, 
                    user_prompt, 
                    slide_count, 
                    visual_style,
                    active_model
                )
                
                st.success("Presentation successfully generated!")
# ... existing code ...
```
Let me verify my diff logic is rock solid before writing the file block.
The diff requires `... existing code ...` placeholders at the beginning or end of the context match.

```python:Application Code:app.py
# ... existing code ...
    # Adding a model selector in case API strings change in the future
    st.markdown("---")
    st.markdown("**Model Configuration**")
    active_model = st.text_input("Agentic Model", value="gemini-3.6-flash")
    
    st.markdown("---")
    st.markdown("**Render Strategy**: Marp Markdown")

# ---------------------------------------------------------
# AGENTIC LOOP LOGIC
# ---------------------------------------------------------
def agentic_presentation_loop(api_key: str, prompt: str, slide_count: int, theme: str, model_id: str) -> str:
    """Executes a multi-agent workflow to research, draft, and refine a presentation."""
    
    # Initialize the standard Google GenAI client
    client = genai.Client(api_key=api_key)
    
    # Phase 1: Research & Outline
    st.info(f"Phase 1: Agent researching and structuring outline using {model_id}...")
    outline_prompt = (
        f"Act as a Principal Research Scientist. Create a highly structured, logical outline for a "
        f"{slide_count}-slide presentation on the following topic:\n\n{prompt}\n\n"
        "Detail the title, main bullet points, and the scientific narrative flow for each slide."
    )
    outline_response = client.models.generate_content(
        model=model_id,
        contents=outline_prompt
    )
    
    # Phase 2 & 3: Self-Critique, Refinement, and Code-to-Slide Generation
    st.info(f"Phase 2: Agent refining narrative and injecting Marp Markdown syntax using {model_id}...")
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
        model=model_id,
        contents=marp_prompt
    )
    
    # Clean output to extract just the markdown
# ... existing code ...
        with st.spinner("Initializing Agentic Loop..."):
            try:
                # Execute the loop
                final_markdown = agentic_presentation_loop(
                    api_key, 
                    user_prompt, 
                    slide_count, 
                    visual_style,
                    active_model
                )
                
                st.success("Presentation successfully generated!")
# ... existing code ...
```
This diff is well structured. I'm removing the `flash_model` and `pro_model` inputs and replacing them with `active_model`. Then I update the `agentic_presentation_loop` signature and the `model` parameters within the `generate_content` calls.

Wait, I should also update the tooltip in the Exception block since it still references the old models.

```python:Application Code:app.py
# ... existing code ...
            except Exception as e:
                st.error(f"Pipeline Error: {str(e)}")
                st.info("Tip: If you see a '404 NOT_FOUND' error, verify your API key has access to the specified model string.")
```

Let's make sure I have all the diffs cleanly specified. I will provide three diff blocks to be safe, or one big diff if the context is tight. The context is spanning from `st.markdown("**Model Configuration**")` all the way down to `final_markdown = agentic_presentation_loop(...)` which is a lot of unchanged code. I should split it into two diffs.

Diff 1: The Model Configuration & Loop Signature
Diff 2: The execution of the loop & exception.

Wait, let's just make one diff for the first part and one for the bottom.

Diff 1:
```python:Application Code:app.py
# ... existing code ...
    # Adding a model selector in case API strings change in the future
    st.markdown("---")
    st.markdown("**Model Configuration**")
    active_model = st.text_input("Agentic Model", value="gemini-3.6-flash")
    
    st.markdown("---")
    st.markdown("**Render Strategy**: Marp Markdown")

# ---------------------------------------------------------
# AGENTIC LOOP LOGIC
# ---------------------------------------------------------
def agentic_presentation_loop(api_key: str, prompt: str, slide_count: int, theme: str, model_id: str) -> str:
    """Executes a multi-agent workflow to research, draft, and refine a presentation."""
    
    # Initialize the standard Google GenAI client
    client = genai.Client(api_key=api_key)
    
    # Phase 1: Research & Outline
    st.info(f"Phase 1: Agent researching and structuring outline using {model_id}...")
    outline_prompt = (
        f"Act as a Principal Research Scientist. Create a highly structured, logical outline for a "
        f"{slide_count}-slide presentation on the following topic:\n\n{prompt}\n\n"
        "Detail the title, main bullet points, and the scientific narrative flow for each slide."
    )
    outline_response = client.models.generate_content(
        model=model_id,
        contents=outline_prompt
    )
    
    # Phase 2 & 3: Self-Critique, Refinement, and Code-to-Slide Generation
    st.info(f"Phase 2: Agent refining narrative and injecting Marp Markdown syntax using {model_id}...")
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
        model=model_id,
        contents=marp_prompt
    )
    
    # Clean output to extract just the markdown
# ... existing code ...
```

Diff 2:
```python:Application Code:app.py
# ... existing code ...
        with st.spinner("Initializing Agentic Loop..."):
            try:
                # Execute the loop
                final_markdown = agentic_presentation_loop(
                    api_key, 
                    user_prompt, 
                    slide_count, 
                    visual_style,
                    active_model
                )
                
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
                st.info("Tip: If you see a '404 NOT_FOUND' error, verify your API key has access to the specified model string.")
```
I'll output both diffs cleanly. I will now explain what changed and what to do next.### 1. Goal Confirmation
We are updating the application architecture to strictly use the `gemini-3.6-flash` model for the entire Agentic Loop (both the drafting and refinement phases). We will remove the `pro` tier dependency entirely and consolidate the configuration so the system only queries the `3.6-flash` endpoint.

### 2. The Updated Code

I am pushing updates to your `app.py` file to refactor the model logic. These diffs will streamline the sidebar and update the loop to use one uniform model parameter.

```python:Application Code:app.py
# ... existing code ...
    # Adding a model selector in case API strings change in the future
    st.markdown("---")
    st.markdown("**Model Configuration**")
    active_model = st.text_input("Agentic Model", value="gemini-3.6-flash")
    
    st.markdown("---")
    st.markdown("**Render Strategy**: Marp Markdown")

# ---------------------------------------------------------
# AGENTIC LOOP LOGIC
# ---------------------------------------------------------
def agentic_presentation_loop(api_key: str, prompt: str, slide_count: int, theme: str, model_id: str) -> str:
    """Executes a multi-agent workflow to research, draft, and refine a presentation."""
    
    # Initialize the standard Google GenAI client
    client = genai.Client(api_key=api_key)
    
    # Phase 1: Research & Outline
    st.info(f"Phase 1: Agent researching and structuring outline using {model_id}...")
    outline_prompt = (
        f"Act as a Principal Research Scientist. Create a highly structured, logical outline for a "
        f"{slide_count}-slide presentation on the following topic:\n\n{prompt}\n\n"
        "Detail the title, main bullet points, and the scientific narrative flow for each slide."
    )
    outline_response = client.models.generate_content(
        model=model_id,
        contents=outline_prompt
    )
    
    # Phase 2 & 3: Self-Critique, Refinement, and Code-to-Slide Generation
    st.info(f"Phase 2: Agent refining narrative and injecting Marp Markdown syntax using {model_id}...")
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
        model=model_id,
        contents=marp_prompt
    )
    
    # Clean output to extract just the markdown
# ... existing code ...
        with st.spinner("Initializing Agentic Loop..."):
            try:
                # Execute the loop
                final_markdown = agentic_presentation_loop(
                    api_key, 
                    user_prompt, 
                    slide_count, 
                    visual_style,
                    active_model
                )
                
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
                st.info("Tip: If you see a '404 NOT_FOUND' error, verify your API key has access to the specified model string.")
