import streamlit as st
from PIL import ImageDraw
import tempfile
import os

@st.dialog("Label Objects")
def AddLabel(image=None):
    data_label = st.text_input("Data label")
    
    # Initialize bbox coordinates
    top_x = top_y = bottom_x = bottom_y = 0
    
    # Image preview section with rectangle overlay (no external component)
    if image is not None:
        st.write("Preview: draw rectangle via inputs; overlay updates live.")
    
    # Bounding box inputs (auto-filled when a rectangle is drawn)
    st.write("Bounding box (auto-filled from drawing):")
    s_left, c1, c2, c3, c4, s_right = st.columns([1, 2, 2, 2, 2, 1])
    with c1:
        top_x = st.number_input("Top X", min_value=0, value=top_x, step=1)
    with c2:
        top_y = st.number_input("Top Y", min_value=0, value=top_y, step=1)
    with c3:
        bottom_x = st.number_input("Bottom X", min_value=0, value=bottom_x, step=1)
    with c4:
        bottom_y = st.number_input("Bottom Y", min_value=0, value=bottom_y, step=1)

    # Live preview overlay using PIL
    if image is not None and bottom_x > top_x and bottom_y > top_y:
        preview_img = image.copy()
        drawer = ImageDraw.Draw(preview_img)
        drawer.rectangle([(top_x, top_y), (bottom_x, bottom_y)], outline="red", width=3)
        st.image(preview_img, caption="Preview with rectangle", use_container_width=True)



    if st.button("Submit"):
        # Basic bbox validation: bottom should be greater than top
        if bottom_x <= top_x or bottom_y <= top_y:
            st.error("Invalid bounding box: bottom values must be greater than top values.")
            return
        st.session_state['label_form'] = {
            "data_label": data_label,
            "bbox": {
                "top_x": top_x,
                "top_y": top_y,
                "bottom_x": bottom_x,
                "bottom_y": bottom_y
            }
        }
        st.rerun()
