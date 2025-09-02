from pathlib import Path
import streamlit as st
from .side_panel import side_page


def render_resume(base_dir: Path):
    col1, _, col3 = st.columns([7, 1, 20])
    with col1:
        side_page(base_dir)
    with col3:
        st.markdown("## Resume\n")
        resume_url = "https://drive.google.com/file/d/1a313QsCO9tekx-oiPl6gh8B5W4r5jpb_/view?usp=drivesdk"
        st.link_button("Open Resume in New Tab", resume_url, use_container_width=False)
        st.caption("If the link doesn't open, copy & paste: " + resume_url)