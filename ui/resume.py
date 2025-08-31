from pathlib import Path
import streamlit as st
from .side_panel import side_page


def render_resume(base_dir: Path):
    col1, _, col3 = st.columns([7, 1, 20])
    with col1:
        side_page(base_dir)
    with col3:
        st.markdown("## Resume\n")
        resume_url = "https://drive.google.com/file/d/1ZHL_eMg-m4d8EH4rKVMSXNAwmENtFkfi/view"
        st.link_button("Open Resume in New Tab", resume_url, use_container_width=False)
        st.caption("If the link doesn't open, copy & paste: " + resume_url)