import streamlit as st

@st.dialog("Label Objects")
def AddLabel():
    mode = st.radio("Mode", ["Text", "Table", "AI"], horizontal=True)
    data_label = st.text_input("Data label")
    s_left, c1, c2, c3, c4, s_right = st.columns([1, 2, 2, 2, 2, 1])
    with c1:
        top_x = st.number_input("Top X", min_value=0, value=0, step=1)
    with c2:
        top_y = st.number_input("Top Y", min_value=0, value=0, step=1)
    with c3:
        bottom_x = st.number_input("Bottom X", min_value=0, value=0, step=1)
    with c4:
        bottom_y = st.number_input("Bottom Y", min_value=0, value=0, step=1)

    if st.button("Submit"):
        st.session_state['label_form'] = {
            "mode": mode,
            "data_label": data_label,
            "bbox": {
                "top_x": top_x,
                "top_y": top_y,
                "bottom_x": bottom_x,
                "bottom_y": bottom_y
            }
        }
        st.rerun()
