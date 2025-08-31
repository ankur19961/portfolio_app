import base64
import os
from pathlib import Path
import streamlit as st


def side_page(base_dir: Path):
    def get_image_base64(image_path: str) -> str:
        if not os.path.exists(image_path):
            return ""
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    img_b64 = get_image_base64("assets/images/photo.png")

    st.markdown(
        """
        <style>
          /* Side profile styling with proper theme support */
          .main-card {
            max-width: 500px;
            margin: 0 auto;
            padding: .5rem 0;
            background-color: transparent !important;
            border: none !important;
            color: var(--text-color) !important;
            text-align: center;
          }

          .profile-img {
            width: 200px;
            height: 200px;
            border-radius: 50%;
            object-fit: cover;
            margin-bottom: 1rem;
            border: none;
            box-shadow: 0 2px 12px rgba(0,0,0,.06);
          }

          .name {
            font-size: 2rem;
            font-weight: 800;
            margin: .25rem 0 .25rem;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--text-color) !important;
          }

          .title {
            color: var(--accent-color) !important;
            font-size: .95rem;
            font-weight: 500;
            margin-bottom: .5rem;
            background-color: transparent !important;
            padding: 0;
            border-radius: 0;
          }

          .contact-item {
            display: flex;
            align-items: flex-start;
            justify-content: center;
            gap: .6rem;
            margin-top: .9rem;
            color: var(--text-color) !important;
          }

          .contact-word {
            color: var(--accent-color) !important;
            letter-spacing: .04em;
            background: transparent !important;
          }

          .social-icons {
            display: flex;
            justify-content: center;
            gap: 1.1rem;
            margin-top: 1.0rem;
          }

          .social-icon {
            width: 28px; 
            height: 28px;
            transition: transform .2s ease;
          }
          
          .social-icon:hover { 
            transform: scale(1.06); 
          }
          
          /* Contact item text styling */
          .contact-item div {
            color: var(--text-color) !important;
          }
          
          .contact-item span {
            color: var(--text-color) !important;
          }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Photo and basic info
    st.markdown(
        f"""
        <div class="main-card">
            <div>
                <img src="data:image/png;base64,{img_b64}" class="profile-img" />
            </div>
            <div class="name">Ankur Shukla</div>
            <div class="title">Senior Data Scientist</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Contact information with improved styling
    st.markdown(
        """
        <div class="contact-item">
            <img src="https://img.icons8.com/color/48/email.png" width="20" />
            <div>
                <strong class="contact-word">EMAIL</strong><br>
                <span style="color: var(--text-color) !important;">ankurshukla19961@gmail.com</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="contact-item">
            <img src="https://img.icons8.com/color/48/phone.png" width="20" />
            <div>
                <strong class="contact-word">PHONE</strong><br>
                <span style="color: var(--text-color) !important;">+91 8097970726</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="contact-item">
            <img src="https://img.icons8.com/color/48/marker.png" width="20" />
            <div>
                <strong class="contact-word">LOCATION</strong><br>
                <span style="color: var(--text-color) !important;">Mumbai, India</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Social links
    st.markdown(
        """
        <div class="social-icons">
            <a href="https://www.linkedin.com/in/ankurshukla1996/" target="_blank">
                <img src="https://img.icons8.com/color/48/linkedin.png" class="social-icon" />
            </a>
            <a href="https://github.com/ankur19961" target="_blank">
                <img src="https://img.icons8.com/color/48/github.png" class="social-icon" />
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )
