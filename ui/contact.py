import re
from pathlib import Path
import requests
import streamlit as st
from .side_panel import side_page


def render_contact(base_dir: Path):
    col1, _, col3 = st.columns([7, 1, 20])
    with col1:
        side_page(base_dir)
    with col3:

        st.markdown("<h1 style='margin-bottom: 20px;'>Contact</h1>", unsafe_allow_html=True)
        st.markdown(
            """
            <section class="mapbox">
                <figure>
                    <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d241317.1160983341!2d72.7410992!3d19.0821978!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3be7b63b0f0aaf2f%3A0x3a1f6f6f6f6f6f6f!2sMumbai%2C%20Maharashtra%2C%20India!5e0!3m2!1sen!2sin!4v1717596151210!5m2!1sen!2sin"
                        width="100%" height="300" style="border:0; border-radius:10px;" allowfullscreen="" loading="lazy"></iframe>
                </figure>
            </section>
            """,
            unsafe_allow_html=True,
        )

        with st.form("contact_form", clear_on_submit=False):
            full_name = st.text_input("Full Name", placeholder="Enter your full name")
            email = st.text_input("Email Address", placeholder="Enter your email address")
            message = st.text_area("Message", placeholder="Type your message here…")
            submitted = st.form_submit_button("Send Message")

        if submitted:
            if not (full_name and email and message):
                st.error("Please fill out all fields before submitting.")
            elif not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
                st.error("Please enter a valid email address.")
            else:
                formspree_url = "https://formspree.io/f/mldwrvyr"  # your endpoint
                data = {
                    "fullname": full_name,
                    "email": email,
                    "message": message,
                    "_subject": f"New message from {full_name} via Portfolio",
                }
                headers = {"Accept": "application/json"}

                with st.spinner("Sending your message…"):
                    try:
                        r = requests.post(formspree_url, data=data, headers=headers, timeout=10)
                        if 200 <= r.status_code < 300:
                            st.success("Your message has been sent successfully!")
                            # Clear fields
                            st.session_state["Full Name"] = ""
                            st.session_state["Email Address"] = ""
                            st.session_state["Message"] = ""
                        else:
                            st.error(f"Failed to send your message (HTTP {r.status_code}).")
                    except Exception as e:
                        st.error(f"Failed to send your message. {e}")
