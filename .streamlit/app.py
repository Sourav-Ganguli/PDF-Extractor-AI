import streamlit as st
import fitz  # PyMuPDF
from PIL import Image, ImageDraw
from components.label_dialog import AddLabel
# Import and reload to avoid cache issues




# Set page configuration for screen size (must be first Streamlit command)
st.set_page_config(
	page_title="PDF Extractor AI",
	page_icon="😊",  # Smiley icon
	layout="wide",  # Options: "centered", "wide"
	initial_sidebar_state="expanded"  # Options: "auto", "expanded", "collapsed"
)

st.markdown(
	"""
	<style>
	.block-container {
		padding-top: 1rem !important;
	}
	header, .st-emotion-cache-18ni7ap {
		display: none;
	}
	</style>
	""",
	unsafe_allow_html=True
)

st.title("PDF Extractor AI")
st.write("Upload your PDF files to get started")
uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=False)

default_boxes = [
		{"name": "box1", "bbox": [100, 100, 100, 100]},
		{"name": "box2", "bbox": [200, 300, 300, 400]}
	]



if uploaded_files is not None:
	import json
	
	# Render first page of PDF to image using PyMuPDF (need this early for dialog)
	pdf_bytes = uploaded_files.read()
	doc = fitz.open(stream=pdf_bytes, filetype="pdf")
	page = doc.load_page(0)
	pix = page.get_pixmap()
	img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
	
	col1, col2 = st.columns([3, 1])
	# Default JSON for boxes

	with col2:
		zoom = st.slider("Zoom", min_value=0.2, max_value=3.0, value=1.0, step=0.05)
		st.markdown("### Edit Boxes JSON")
		
		if "AddLabel" not in st.session_state:
			if st.button("Label Objects"):
				AddLabel(image=img)


		boxes_json = st.text_area(
			"Edit boxes JSON",
			value=json.dumps(default_boxes, indent=2),
			height=200
		)
		try:
			boxes = json.loads(boxes_json)
		except Exception as e:
			st.error(f"Invalid JSON: {e}")
			boxes = default_boxes
			
   			


	with col1:
		draw = ImageDraw.Draw(img)
		for box in boxes:
			x, y, w_box, h_box = box["bbox"]
			draw.rectangle([x, y, x + w_box, y + h_box], outline="red", width=5)

		# Zoom controls for image
		
		img_resized = img.resize((int(img.width * zoom), int(img.height * zoom)))
		st.image(img_resized, caption="PDF with red boxes from JSON", use_container_width=False)