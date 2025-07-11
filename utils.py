import streamlit as st
import base64

def get_image_base64(image_path):
    """Encodes an image to base64 for embedding in HTML."""
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return encoded_string
    except FileNotFoundError:
        st.warning(f"Image not found at '{image_path}'.")
        return None

def display_footer():
    st.markdown("---")  # Separator line
    footer_logo_path = "Images/logo.jpg"
    encoded_string = get_image_base64(footer_logo_path)

    if encoded_string:
        footer_logo_html = f'<img src="data:image/jpeg;base64,{encoded_string}" style="height: 30px; vertical-align: middle; margin-right: 10px;">'  # Adjust height as needed
    else:
        footer_logo_html = "<span style='font-size: 1.1em; font-weight: bold; vertical-align: middle;'>Apexon Pulse</span>"

    # Using flexbox for robust alignment
    footer_html = f"""
    <div style="display: flex; justify-content: space-between; align-items: center; width: 100%;">
        <div style="display: flex; align-items: center;">
            {footer_logo_html}
            <span style='font-size: 1.1em; font-weight: bold;'>Apexon Pulse</span>
        </div>
        <p style='text-align: right; font-size: 1.1em; margin: 0;'>Built by The Mavericks</p>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)