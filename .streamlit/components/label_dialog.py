import streamlit as st
from streamlit_cropper import st_cropper

@st.dialog("Label Objects")
def AddLabel(image=None):
    data_label = st.text_input("Data label")

    def normalize_box(cb):
        if isinstance(cb, dict):
            left = float(cb.get("left", cb.get("x", 0)))
            top = float(cb.get("top", cb.get("y", 0)))
            right = float(cb.get("right", left + cb.get("width", 0)))
            bottom = float(cb.get("bottom", top + cb.get("height", 0)))
            return left, top, right, bottom
        if hasattr(cb, "left") and hasattr(cb, "top") and hasattr(cb, "right") and hasattr(cb, "bottom"):
            return float(cb.left), float(cb.top), float(cb.right), float(cb.bottom)
        if isinstance(cb, (list, tuple)) and len(cb) == 4:
            return tuple(float(v) for v in cb)
        return 0.0, 0.0, 0.0, 0.0

    # Initialize bbox coordinates
    top_x = top_y = bottom_x = bottom_y = 0

    if image is not None:
        st.write("Draw a rectangle; the bbox will auto-fill below.")
        crop_box = st_cropper(
            image,
            realtime_update=True,
            return_type="box",  # (left, top, right, bottom)
            box_color='#FF0000',
            aspect_ratio=None,
            key="cropper_bbox"
        )
        if crop_box:
            left, top, right, bottom = normalize_box(crop_box)
            top_x = int(max(0, left))
            top_y = int(max(0, top))
            bottom_x = int(max(0, right))
            bottom_y = int(max(0, bottom))

    # Bounding box inputs (auto-filled from cropper)
    st.write("Bounding box (auto-filled from cropper):")
    _, c1, c2, c3, c4, _ = st.columns([1, 2, 2, 2, 2, 1])
    with c1:
        top_x = st.number_input("Top X", min_value=0, value=top_x, step=1)
    with c2:
        top_y = st.number_input("Top Y", min_value=0, value=top_y, step=1)
    with c3:
        bottom_x = st.number_input("Bottom X", min_value=0, value=bottom_x, step=1)
    with c4:
        bottom_y = st.number_input("Bottom Y", min_value=0, value=bottom_y, step=1)

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
