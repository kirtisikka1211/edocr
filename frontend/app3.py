import streamlit as st
import requests
import json
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="EDOCR", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set up styling
st.markdown("""
<style>
.stApp {
        background-color: black;
    }
h1, h2, h3 { font-family: 'Helvetica Neue', sans-serif; color: white; }
.upload-area {
    border-radius: 10px;
    padding: 2rem;
    text-align: center;
    margin: 2.5rem 0 1rem 1;
}
.stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    font-weight: bold;
    border: none;
    transition: all 0.3s;
}
.stButton>button:hover {
    background-color: #3e8e41;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}
.logo-text {
    font-size: 3.5rem;
    font-weight: bold;
    background: linear-gradient(90deg, #4CAF50, #2196F3);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'extracted_response' not in st.session_state:
    st.session_state['extracted_response'] = None
if 'uploaded_filename' not in st.session_state:
    st.session_state['uploaded_filename'] = None

# Sidebar with branding and navigation
with st.sidebar:
    st.markdown('<div class="logo-text">EDOCR</div>', unsafe_allow_html=True)
    st.markdown("---")
    selected = st.radio("Navigation", ["Home", "Upload & Extract", "Search"])
    st.markdown("---")
    st.markdown("### About")
    st.write("EDOCR is a document extraction and search platform.")
    st.markdown("---")
    st.markdown("### Help")
    st.write("Upload a PDF file and extract information or search through previously extracted data.")

# Home Page
if selected == "Home":
    st.markdown('<div class="content-card fade-in">', unsafe_allow_html=True)
    st.markdown('<h1 class="logo-text">EDOCR</h1>', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Document Extraction & Search Platform</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    for col, icon, title, desc in zip(
        [col1, col2, col3],
        ["📄", "🔍", "🔎"],
        ["Upload", "Extract", "Search"],
        [
            "Upload your PDF documents for information extraction",
            "Automatically extract structured data",
            "Search through your extracted document data"
        ]
    ):
        with col:
            st.markdown(f"<div style='text-align: center; padding: 1rem;'><h3>{icon} {title}</h3><p>{desc}</p></div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Upload & Extract Page
elif selected == "Upload & Extract":
    st.markdown("<h2>📄 Upload PDF for Information Extraction</h2>", unsafe_allow_html=True)
    st.markdown('<div class="upload-area">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", label_visibility="collapsed")

    if uploaded_file is not None:
        if uploaded_file.name != st.session_state['uploaded_filename']:
            st.session_state['uploaded_filename'] = uploaded_file.name
            st.session_state['extracted_response'] = None  # Clear previous response

        st.success(f"Uploaded: {uploaded_file.name}")
    else:
        st.markdown("<p>Drop your PDF file here or click to browse</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        process_button = st.button("Extract Information", use_container_width=True)

    if uploaded_file is not None and process_button:
        with st.spinner("Processing document..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                response = requests.post("http://localhost:8000/extract_info", files=files, timeout=100)
                st.success("✅ Extraction Complete!")
                st.session_state['extracted_response'] = response.json()

            except requests.exceptions.ConnectionError:
                st.error("🚫 Could not connect to FastAPI backend.")
            except Exception as e:
                st.error(f"❌ An error occurred: {e}")

    if st.session_state['extracted_response'] is not None:
        result = st.session_state['extracted_response']
        with st.expander("🧾 View JSON Output"):
            st.json(result)

        try:
            parsed_data = json.loads(result["1"])
            extracted_data = parsed_data.get("ExtractedData", {})

            if extracted_data:
                st.markdown("### 📋 Extracted Information")
                main_data = {k: v for k, v in extracted_data.items() if k != "Notes"}
                df_main = pd.DataFrame(main_data.items(), columns=["Field", "Value"])
                st.table(df_main)

                notes = extracted_data.get("Notes", {}).get("Note", [])
                if notes:
                    st.markdown("### 🗒️ Notes")
                    df_notes = pd.DataFrame(notes, columns=["Notes"])
                    st.table(df_notes)
                else:
                    st.info("No notes found.")
            else:
                st.warning("No 'ExtractedData' found.")
        except Exception as e:
            st.error(f"Error parsing extracted data: {e}")

# Search Page
elif selected == "Search":
    st.markdown('<div class="content-card fade-in">', unsafe_allow_html=True)
    st.markdown("<h2>🔎 Search Extracted Data</h2>", unsafe_allow_html=True)

    filter_expander = st.checkbox("⚙️", key="filter_toggle", help="Show filters")
    product_number = product_family = drawing_number = engineer_name = ""
    if filter_expander:
        with st.expander("Filter Search Options", expanded=True):
            col_a, col_b = st.columns(2)
            with col_a:
                product_number = st.text_input("🔢 Product Number")
                product_family = st.text_input("🏷️ Product Family")
            with col_b:
                drawing_number = st.text_input("🖼️ Drawing Number")
                engineer_name = st.text_input("👷 Engineer Name")

    search_clicked = st.button("🔍 Search", use_container_width=True)

    if search_clicked:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        if st.session_state['extracted_response'] is not None:
            st.markdown("### Results from last extracted document")
            parsed_data = json.loads(st.session_state['extracted_response']["1"])
            extracted_data = parsed_data.get("ExtractedData", {})
            df_main = pd.DataFrame({k: v for k, v in extracted_data.items() if k != "Notes"}.items(), columns=["Field", "Value"])
            st.table(df_main)
        else:
            st.info("No extracted data available. Please upload and extract a document first.")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; color: #6c757d;">
            <i class="fas fa-search" style="font-size: 3rem;"></i>
            <p style="margin-top: 1rem;">Enter a search term or use filters, then click 'Search'</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
