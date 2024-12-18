import streamlit as st
import sys
import io
from contextlib import redirect_stdout
from product_design.crew import ProductDesign

# Set page config
st.set_page_config(
    page_title="IKEA Innovation Assistant",
    page_icon="🏢",
    layout="wide"
)

# Custom CSS for IKEA branding
st.markdown("""
    <style>
    .stButton>button {
        background-color: #0051BA;
        color: white;
        transition: background-color 0.3s;
    }
    .stButton>button:hover {
        background-color: #003D8F;
        color: white;
    }
    .stButton>button:disabled {
        background-color: #FFDA1A !important;
        color: #333333 !important;
        cursor: not-allowed;
    }
    .title {
        color: #0051BA;
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 2rem;
    }
    .subtitle {
        color: #333333;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .agent-conversation {
        font-family: monospace;
        white-space: pre-wrap;
        background-color: #f5f5f5;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .loading-gif {
        display: flex;
        justify-content: center;
        margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown('<h1 class="title">IKEA Innovation Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Powered by AI Agents for Rapid Innovation Research</p>', unsafe_allow_html=True)

# Input section
st.markdown("### Enter Your Innovation Topic")
topic = st.text_area(
    "Describe your product concept or innovation idea in detail:",
    height=150,
    help="Enter a detailed description of your product concept, including key features, target audience, and objectives."
)

# Create a placeholder for the button
button_placeholder = st.empty()

# Run button with state handling
if button_placeholder.button("Generate Innovation Analysis", type="primary", disabled=False, key="generate_button"):
    if not topic:
        st.error("Please enter a topic before proceeding.")
    else:
        try:
            # Update button state to disabled
            button_placeholder.button("Processing...", type="primary", disabled=True, key="processing_button")
            
            # Create a progress container
            progress_container = st.empty()
            with progress_container:
                col1, col2, col3 = st.columns([1,2,1])
                with col2:
                    st.info("AI agents have started working on this. It will take a few minutes.")
                    st.markdown(
                        """
                        <div class="loading-gif">
                            <img src="https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExdWZ5bmpuZXFsbTcydmg2YTRiY3c1N2czNWJnZTh3YzJxMGRqa3J4YyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Je0awPS61D0F5FP6QX/giphy.webp" 
                            alt="Loading..." width="700">
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            # Create output capture
            output = io.StringIO()
            
            # Run the analysis with output capture
            with redirect_stdout(output):
                inputs = {'topic': topic}
                crew = ProductDesign().crew()
                results = crew.kickoff(inputs=inputs)

            # Clear the progress container
            progress_container.empty()

            # Reset button state
            button_placeholder.button("Generate Innovation Analysis", type="primary", disabled=False, key="reset_button")

            # Display the detailed output in a collapsible section with scrollable container
            with st.expander("View Detailed Agent Conversations", expanded=True):
                # Convert the output to markdown-friendly format
                conversation_text = output.getvalue()
                conversation_text = conversation_text.replace("```", "'''")  # Prevent markdown conflicts
                
                # Create a scrollable container with fixed height
                with st.container(height=400):
                    st.markdown(f"""```text
{conversation_text}
```""")

            # Display the results
            st.markdown("### Analysis Results")
            
            # Market Analysis
            st.markdown("#### 🎯 Market Analysis")
            with open("market_analysis.md", "r") as f:
                st.markdown(f.read())
            
            # Technical Assessment
            st.markdown("#### 🔧 Technical Assessment")
            with open("technical_assessment.md", "r") as f:
                st.markdown(f.read())
            
            # Feasibility Evaluation
            st.markdown("#### 📊 Feasibility Evaluation")
            with open("feasibility_evaluation.md", "r") as f:
                st.markdown(f.read())

        except Exception as e:
            # Reset button state in case of error
            button_placeholder.button("Generate Innovation Analysis", type="primary", disabled=False, key="error_button")
            st.error(f"An error occurred: {str(e)}")
            st.error("Please check if the API keys are properly configured in the Streamlit secrets.")

# Footer with instructions
with st.sidebar:
    st.markdown("### How to Use")
    st.markdown("""
    1. Enter your innovation topic or product concept in the text area
    2. Click 'Generate Innovation Analysis'
    3. View the detailed agent conversations
    4. Review the comprehensive analysis reports
    """)
    
    st.markdown("### About")
    st.markdown("""
    This tool leverages AI agents to perform:
    - Market Analysis
    - Technical Assessment
    - Feasibility Evaluation
    
    Perfect for rapid innovation research and concept validation.
    """) 