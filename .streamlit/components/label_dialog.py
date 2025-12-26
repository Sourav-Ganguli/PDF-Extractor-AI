import streamlit as st
from PIL import Image, ImageDraw










@st.dialog("Label Objects")
def AddLabel(image=None):
    data_label = st.text_input("Data label")

    # Initialize bbox coordinates
    top_x = top_y = bottom_x = bottom_y = 0

    # Bounding box inputs
    st.write("Enter bounding box coordinates:")
    st.info("💡 Tip: Adjust the coordinates below and see the preview update in real-time.")
    
    # Get max values from image dimensions
    max_x = image.width if image is not None else 1000
    max_y = image.height if image is not None else 1000
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        top_x = st.slider("Top X", min_value=0, max_value=max_x, value=top_x, step=1)
    with c2:
        top_y = st.slider("Top Y", min_value=0, max_value=max_y, value=top_y, step=1)
    with c3:
        bottom_x = st.slider("Bottom X", min_value=0, max_value=max_x, value=bottom_x, step=1)
    with c4:
        bottom_y = st.slider("Bottom Y", min_value=0, max_value=max_y, value=bottom_y, step=1)
    
    # Preview with rectangle
    if image is not None:
        if top_x < bottom_x and top_y < bottom_y:
            preview_image = image.copy()
            draw = ImageDraw.Draw(preview_image)
            draw.rectangle(
                [(top_x, top_y), (bottom_x, bottom_y)],
                outline='red',
                width=3
            )
            st.image(preview_image, use_container_width=True, caption="Preview with rectangle")
        else:
            st.image(image, use_container_width=True, caption=f"Original image ({image.width}x{image.height})")


    if st.button("Submit"):
        # Basic bbox validation: bottom should be greater than top
        if bottom_x <= top_x or bottom_y <= top_y:
            st.error("Invalid bounding box: bottom values must be greater than top values.")
            return
        
        # Initialize default_boxes array if it doesn't exist
        if 'default_boxes' not in st.session_state:
            st.session_state['default_boxes'] = []
        
        # Append the new label and bbox to the array
        st.session_state['default_boxes'].append({
            "label": data_label,
            "box": [top_x, top_y, bottom_x, bottom_y]
        })
        
        st.rerun()
