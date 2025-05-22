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


st.markdown("""
<style>
* Modern styling for the entire app */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Header styling */
    h1, h2, h3 {
        font-family: 'Helvetica Neue', sans-serif;
        color: white;
    }
    

    
    /* Upload area styling */
    .upload-area {
       
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
         margin: 2.5rem 0 1rem 1;
    }
    
    /* Button styling */
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
    
    /* Navigation pill styling */
    .nav-pills {
        display: flex;
        justify-content: center;
        margin-bottom: 2rem;
    }
    
    /* Logo styling */
    .logo-text {
        font-size: 3.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #4CAF50, #2196F3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    /* Sidebar custom styling */
    .css-1d391kg {
        background-color: #f1f3f4;
    }
    
    /* Search bar styling */
    .search-container input {
        border-radius: 20px;
        border: 1px solid #ddd;
        padding: 10px 15px;
    }
    
    /* Table styling */
    .stTable {
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* Hide default header decoration */
    .main .block-container {
        padding-top: 1rem;
    }
    
    /* Animation for transitions */
    .fade-in {
        animation: fadeIn 0.5s;
    }
    
    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

# Sidebar with branding and navigation
with st.sidebar:
    st.markdown('<div class="logo-text">EDOCR</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar Navigation
    selected = st.radio("Navigation", ["Home", "Upload & Extract", "Search"])
    
    st.markdown("---")
    st.markdown("### About")
    st.write("EDOCR is a document extraction and search platform.")
    st.markdown("---")
    st.markdown("### Help")
    st.write("Upload a PDF file and extract information or search through previously extracted data.")

# Main content area
if selected == "Home":
    st.markdown('<div class="content-card fade-in">', unsafe_allow_html=True)
    st.markdown('<h1 class="logo-text">EDOCR</h1>', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Document Extraction & Search Platform</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h3>📄 Upload</h3>
            <p>Upload your PDF documents for information extraction</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h3>🔍 Extract</h3>
            <p>Automatically extract structured data </p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h3>🔎 Search</h3>
            <p>Search through your extracted document data</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif selected == "Upload & Extract":
    # st.markdown('<div class="content-card fade-in">', unsafe_allow_html=True)
    st.markdown("<h2>📄 Upload PDF for Information Extraction</h2>", unsafe_allow_html=True)
    
    st.markdown('<div class="upload-area">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", label_visibility="collapsed")
    
    if uploaded_file is not None:
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
                st.markdown('<div class="content-card">', unsafe_allow_html=True)
                files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                response = requests.post("http://localhost:8000/extract_info", files=files, timeout=100000000)
                
                st.success("✅ Extraction Complete!")
                
                with st.expander("🔍 View Raw Response"):
                    st.text(response.text)
                
                try:
                    result = response.json()
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
                                st.info("No notes found in the extracted data.")
                        else:
                            st.warning("No 'ExtractedData' found in the response.")
                    except Exception as e:
                        st.error(f"Error parsing JSON response structure: {e}")
                
                except json.JSONDecodeError:
                    st.error("⚠️ Response is not valid JSON.")
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            except requests.exceptions.ConnectionError:
                st.error("🚫 Could not connect to FastAPI backend. Make sure it's running.")
    
    st.markdown('</div>', unsafe_allow_html=True)

elif selected == "Search":
    st.markdown('<div class="content-card fade-in">', unsafe_allow_html=True)
    st.markdown("<h2>🔎 Search Extracted Data</h2>", unsafe_allow_html=True)

    # Search bar and filter icon
 
    filter_expander = st.checkbox("⚙️", key="filter_toggle", help="Show filters")

    # Filters section
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

    # Search button
    search_clicked = st.button("🔍 Search", use_container_width=True)

    # Display results only after button is clicked
    if search_clicked:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)


        if search_query or any([product_number, product_family, drawing_number, engineer_name]):
            st.markdown(f"### Results for: '{search_query}'")
            st.info(f"No matching results found for your search criteria (yet).")
        else:
            st.warning("Please enter a search term or use at least one filter.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; color: #6c757d;">
            <i class="fas fa-search" style="font-size: 3rem;"></i>
            <p style="margin-top: 1rem;">Enter a search term or use filters, then click 'Search'</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


