from pathlib import Path
import html
import streamlit as st
from .side_panel import side_page


def render_experience(base_dir: Path):
    col1, _, col3 = st.columns([7, 1, 20])
    with col1:
        side_page(base_dir)
    with col3:
        st.markdown("<h1 style='margin-bottom: 20px;'>Work Experience</h1>", unsafe_allow_html=True)
        # Replace the CSS in your render_research_experience() function with this:
        # Replace the CSS in your render_research_experience() function with this:
        st.markdown(
    """
    <style>
      .experience-block {
        display: flex;
        background: var(--panel-bg) !important;
        border: 1px solid var(--panel-border) !important;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,.04);
        overflow: hidden;
      }
      .experience-left {
        background-color: #F7C873 !important;    /* keep bright orange accent */
        padding: 20px;
        flex: 1;
        display: flex; 
        flex-direction: column; 
        justify-content: center; 
        align-items: center; 
        text-align: center;
        font-weight: bold; 
        color: #000000 !important;  /* always dark text on bright orange */
      }
      .experience-right { 
        padding: 20px; 
        flex: 3; 
        background: var(--panel-bg) !important; 
        color: var(--text-color) !important; 
      }
      .experience-details { 
        font-size: 16px; 
        line-height: 1.6; 
        color: var(--text-color) !important; 
      }
      .experience-details ul { 
        padding-left: 20px; 
        margin: 0; 
      }
      .experience-details li {
        margin-bottom: 10px;
        background: transparent !important;
        color: var(--text-color) !important;
      }
    </style>
    """,
    unsafe_allow_html=True,
)
        
        
        experiences = [
            {
                "title": "Senior Data Scientist",
                "subtitle": "Fractal Analytics",
                "date": "Apr 2025 - Present",
                "details": [
                    "Initiated an AI-based prescription alerting system to flag high-risk PV1 transactions using historical QRE and Near Miss data.",
                    "Designed a LightGBM model with temporal features to detect anomalies in drug, dose, and patient data, reducing manual interventions by 30%.",
                    "Applied LLM-powered semantic clustering on pharmacist notes, improving labeling accuracy by 28%.",
                    "Integrated real-time alerts into IRIS/Prodigy via FastAPI, achieving sub-300ms latency.",
                ],
            },
            {
                "title": "Senior ML Data Analyst",
                "subtitle": "Tata Consultancy Services",
                "date": "Apr 2021 - Apr 2025",
                "details": [
                    "Spearheaded a GenAI chatbot using LangChain, LangGraph, and RAG, automating 80% of customer queries.",
                    "Built modular conversational flows with LangGraph and AI Agents, achieving 92% completion accuracy.",
                    "Fine-tuned LLMs with Lamini on 10K+ documents, boosting precision by 38%.",
                    "Engineered semantic search using OCR, MiniLM, FAISS, and Pinecone; reduced hallucinations by 31% using RAGAS.",
                ],
            },
            {
                "title": "IT Analyst",
                "subtitle": "Tata Consultancy Services",
                "date": "Dec 2018 - Mar 2021",
                "details": [
                    "Developed ML-based credit eligibility scoring engine, lowering default rates by 18%.",
                    "Built data pipelines consolidating 50–64 features and reduced feature count by 60%.",
                    "Applied LightGBM with SMOTE, achieving 89% AUC-ROC and 82% recall.",
                    "Used SHAP for model explainability and monitored post-COVID drift.",
                ],
            },
        ]

        for exp in experiences:
            details_html = "".join(f"<li>{html.escape(d)}</li>" for d in exp["details"])
            st.markdown(
                f"""
                <div class="experience-block">
                    <div class="experience-left">
                        <div>{html.escape(exp['subtitle'])}</div>
                        <div>{html.escape(exp['title'])}</div>
                        <div>{html.escape(exp['date'])}</div>
                    </div>
                    <div class="experience-right">
                        <div class="experience-details">
                            <ul>{details_html}</ul>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
