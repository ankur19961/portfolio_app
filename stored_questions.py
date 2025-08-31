# stored_questions.py
# Curated Q&A used by AnkBot before calling the LLM.
# Keep answers concise, factual, and aligned with the portfolio app content.

# stored_questions.py
# Curated Q&A used by AnkBot before calling the LLM.

var = {
    # === CONTACT / PROFILES ===
    "contact": (
        "You can reach Ankur at:\n"
        "- Email (preferred): ankurshukla19961@gmail.com\n"
        "- LinkedIn: https://www.linkedin.com/in/ankurshukla1996/\n"
        "- GitHub: https://github.com/ankur19961"
    ),
    "how can i contact you": (
        "You can reach Ankur at:\n"
        "- Email (preferred): ankurshukla19961@gmail.com\n"
        "- LinkedIn: https://www.linkedin.com/in/ankurshukla1996/\n"
        "- GitHub: https://github.com/ankur19961"
    ),
    "contact information": (
        "You can reach Ankur at:\n"
        "- Email (preferred): ankurshukla19961@gmail.com\n"
        "- LinkedIn: https://www.linkedin.com/in/ankurshukla1996/\n"
        "- GitHub: https://github.com/ankur19961"
    ),
    
    # === EMAIL VARIATIONS ===
    "email": "Email: ankurshukla19961@gmail.com",
    "email address": "Email: ankurshukla19961@gmail.com",
    "email id": "Email: ankurshukla19961@gmail.com",
    "his email": "Email: ankurshukla19961@gmail.com",
    "his email id": "Email: ankurshukla19961@gmail.com",
    "his email address": "Email: ankurshukla19961@gmail.com",
    "what is his email": "Email: ankurshukla19961@gmail.com",
    "what is his email id": "Email: ankurshukla19961@gmail.com",
    "what is his email address": "Email: ankurshukla19961@gmail.com",
    "can you provide his email": "Email: ankurshukla19961@gmail.com",
    "can you provide his email id": "Email: ankurshukla19961@gmail.com",
    "can you provide his email address": "Email: ankurshukla19961@gmail.com",
    "provide his email": "Email: ankurshukla19961@gmail.com",
    "provide his email id": "Email: ankurshukla19961@gmail.com",
    "give me his email": "Email: ankurshukla19961@gmail.com",
    "give me his email id": "Email: ankurshukla19961@gmail.com",
    "ankur email": "Email: ankurshukla19961@gmail.com",
    "ankur email id": "Email: ankurshukla19961@gmail.com",
    "ankur email address": "Email: ankurshukla19961@gmail.com",
    
    # Common typos
    "emai": "Email: ankurshukla19961@gmail.com",
    "emial": "Email: ankurshukla19961@gmail.com",
    "mail": "Email: ankurshukla19961@gmail.com",
    "mail id": "Email: ankurshukla19961@gmail.com",
    
    "linkedin": "LinkedIn: https://www.linkedin.com/in/ankurshukla1996/",
    "github": "GitHub: https://github.com/ankur19961",

    # === SUMMARY / HEADLINE ===
    "summary": (
        "Senior Data Scientist (6+ years) focused on ML, NLP, and Generative AI.\n"
        "- Experienced with LLMs, RAG, LangChain/LangGraph, and AI Agents\n"
        "- Productionizing with PyTorch, Docker, FastAPI, and AWS\n"
        "- Built scalable inference services, automated workflows, and ensured compliance"
    ),
    "about": (
        "Senior Data Scientist (6+ years) focused on ML, NLP, and Generative AI.\n"
        "- Experienced with LLMs, RAG, LangChain/LangGraph, and AI Agents\n"
        "- Productionizing with PyTorch, Docker, FastAPI, and AWS\n"
        "- Built scalable inference services, automated workflows, and ensured compliance"
    ),

    # === CURRENT ROLE ===
    "current role": (
        "Senior Data Scientist at Fractal Analytics (Apr 2025 – Present).\n"
        "- AI-based prescription alerting for high-risk PV1 transactions\n"
        "- LightGBM with temporal features; 30% fewer manual interventions\n"
        "- LLM-powered semantic clustering on pharmacist notes (+28% labeling accuracy)\n"
        "- Real-time alerts via FastAPI; sub-300ms latency"
    ),
    "where do you work now": (
        "Senior Data Scientist at Fractal Analytics (Apr 2025 – Present).\n"
        "- AI-based prescription alerting for high-risk PV1 transactions\n"
        "- LightGBM with temporal features; 30% fewer manual interventions\n"
        "- LLM-powered semantic clustering on pharmacist notes (+28% labeling accuracy)\n"
        "- Real-time alerts via FastAPI; sub-300ms latency"
    ),

    # === WORK EXPERIENCE ===
    "work experience": (
        "Work Experience:\n\n"
        "- Fractal Analytics — Senior Data Scientist (Apr 2025 – Present)\n"
        "  - AI prescription alerting; temporal LightGBM; LLM semantic clustering; FastAPI real-time alerts\n\n"
        "- Tata Consultancy Services — Senior ML Data Analyst (Apr 2021 – Apr 2025)\n"
        "  - GenAI chatbot with LangChain/LangGraph + RAG (automated ~80% queries)\n"
        "  - AI Agents; 92% flow completion; Lamini fine-tuning on 10K+ docs (+38% precision)\n"
        "  - Semantic search with OCR, MiniLM, FAISS, Pinecone; reduced hallucinations by 31% via RAGAS\n\n"
        "- Tata Consultancy Services — IT Analyst (Dec 2018 – Mar 2021)\n"
        "  - Credit eligibility scoring; LightGBM + SMOTE (AUC-ROC ~0.89; recall ~0.82)\n"
        "  - Feature consolidation (60% reduction); SHAP explainability; post-COVID drift monitoring"
    ),
    "professional experience": (
        "Work Experience:\n\n"
        "- Fractal Analytics — Senior Data Scientist (Apr 2025 – Present)\n"
        "- Tata Consultancy Services — Senior ML Data Analyst (Apr 2021 – Apr 2025)\n"
        "- Tata Consultancy Services — IT Analyst (Dec 2018 – Mar 2021)"
    ),
    "experience": (
        "- Fractal Analytics — Senior Data Scientist (Apr 2025 – Present)\n"
        "- Tata Consultancy Services — Senior ML Data Analyst (Apr 2021 – Apr 2025)\n"
        "- Tata Consultancy Services — IT Analyst (Dec 2018 – Mar 2021)"
    ),

    # === PROJECTS ===
    "projects": (
        "Selected Projects:\n"
        "- Redfin Housing Data Pipeline & Visualization — Data Engineering\n"
        "- Kafka Real-Time Data Pipeline — Streaming Analytics\n"
        "- Layoffs Data Visualization — ETL & BI\n"
        "- Fraud Transaction Detection — Machine Learning\n"
        "- Movie Recommendation System — NLP"
    ),
    "list your projects": (
        "Selected Projects:\n"
        "- Redfin Housing Data Pipeline & Visualization — Data Engineering\n"
        "- Kafka Real-Time Data Pipeline — Streaming Analytics\n"
        "- Layoffs Data Visualization — ETL & BI\n"
        "- Fraud Transaction Detection — Machine Learning\n"
        "- Movie Recommendation System — NLP"
    ),
    "most impressive project": (
        "AI-based prescription alerting (Fractal Analytics):\n"
        "- Flags high-risk PV1 transactions using historical QRE and Near Miss data\n"
        "- Temporal LightGBM; LLM semantic clustering on notes (+28% labeling accuracy)\n"
        "- FastAPI real-time serving; sub-300ms latency"
    ),

    # === SKILLS ===
    "skills": (
        "Core Skills:\n"
        "- GenAI & LLMs: RAG, LangChain, LangGraph, AI Agents, Lamini fine-tuning\n"
        "- ML: LightGBM, SMOTE, SHAP, time-series features, model monitoring\n"
        "- Search: OCR, MiniLM embeddings, FAISS, Pinecone, RAGAS evaluation\n"
        "- Platforms: PyTorch, FastAPI, Docker, AWS\n"
        "- Use cases: Chatbots, anomaly detection, credit scoring, semantic clustering"
    ),
    "technical skills": (
        "Core Skills:\n"
        "- GenAI & LLMs: RAG, LangChain, LangGraph, AI Agents, Lamini fine-tuning\n"
        "- ML: LightGBM, SMOTE, SHAP, time-series features, model monitoring\n"
        "- Search: OCR, MiniLM embeddings, FAISS, Pinecone, RAGAS evaluation\n"
        "- Platforms: PyTorch, FastAPI, Docker, AWS\n"
        "- Use cases: Chatbots, anomaly detection, credit scoring, semantic clustering"
    ),

    # === TOOLS / FRAMEWORKS ===
    "tools": (
        "Tools & Frameworks:\n"
        "- Python, PyTorch, FastAPI\n"
        "- LangChain, LangGraph, Lamini\n"
        "- FAISS, Pinecone, OCR (Tesseract/vision stack), MiniLM embeddings\n"
        "- Docker, Git, CI/CD basics\n"
        "- AWS (selected services)"
    ),

    # === EDUCATION / CERTS (placeholder-safe) ===
    "education": (
        "Education details are not listed in the app content.\n"
        "- Please contact Ankur at ankurshukla19961@gmail.com for specifics."
    ),
    "certifications": (
        "Certification details are not listed in the app content.\n"
        "- Please contact Ankur at ankurshukla19961@gmail.com for specifics."
    ),

    # === VISA / WORK AUTH (safe default) ===
    "visa": (
        "Visa/work authorization information isn't provided in the portfolio.\n"
        "- Please contact Ankur at ankurshukla19961@gmail.com for details."
    ),
    "visa status": (
        "Visa/work authorization information isn't provided in the portfolio.\n"
        "- Please contact Ankur at ankurshukla19961@gmail.com for details."
    ),
}