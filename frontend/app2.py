# import streamlit as st
# import requests
# import json
# import pandas as pd

# # Page configuration
# st.set_page_config(
#     page_title="EDOCR", 
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Custom CSS for styling
# st.markdown("""
# <style>
#     .stApp {
#         background-color: black;
#     }
#     h1, h2, h3 {
#         font-family: 'Helvetica Neue', sans-serif;
#         color: white;
#     }
#     .upload-area {
#         border-radius: 10px;
#         padding: 2rem;
#         text-align: center;
#         margin: 2.5rem 0 1rem 1;
#     }
#     .stButton>button {
#         background-color: #4CAF50;
#         color: white;
#         border-radius: 8px;
#         padding: 0.5rem 1rem;
#         font-weight: bold;
#         border: none;
#         transition: all 0.3s;
#     }
#     .stButton>button:hover {
#         background-color: #3e8e41;
#         box-shadow: 0 4px 8px rgba(0,0,0,0.1);
#     }
#     .logo-text {
#         font-size: 3.5rem;
#         font-weight: bold;
#         background: linear-gradient(90deg, #4CAF50, #2196F3);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         text-align: center;
#         margin-bottom: 1rem;
#     }
#     .main .block-container {
#         padding-top: 1rem;
#     }
#     .fade-in {
#         animation: fadeIn 0.5s;
#     }
#     @keyframes fadeIn {
#         0% { opacity: 0; }
#         100% { opacity: 1; }
#     }
# </style>
# """, unsafe_allow_html=True)

# # Sidebar with branding and navigation
# with st.sidebar:
#     st.markdown('<div class="logo-text">EDOCR</div>', unsafe_allow_html=True)
#     st.markdown("---")
#     selected = st.radio("Navigation", ["Home", "Upload & Extract", "Search"])
#     st.markdown("---")
#     st.markdown("### About")
#     st.write("EDOCR is a document extraction and search platform.")
#     st.markdown("---")
#     st.markdown("### Help")
#     st.write("Upload a PDF file and extract information or search through previously extracted data.")

# # Main Pages
# if selected == "Home":
#     st.markdown('<div class="content-card fade-in">', unsafe_allow_html=True)
#     st.markdown('<h1 class="logo-text">EDOCR</h1>', unsafe_allow_html=True)
#     st.markdown("<h3 style='text-align: center;'>Document Extraction & Search Platform</h3>", unsafe_allow_html=True)
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         st.markdown("<div style='text-align: center; padding: 1rem;'><h3>📄 Upload</h3><p>Upload your PDF documents for information extraction</p></div>", unsafe_allow_html=True)
#     with col2:
#         st.markdown("<div style='text-align: center; padding: 1rem;'><h3>🔍 Extract</h3><p>Automatically extract structured data </p></div>", unsafe_allow_html=True)
#     with col3:
#         st.markdown("<div style='text-align: center; padding: 1rem;'><h3>🔎 Search</h3><p>Search through your extracted document data</p></div>", unsafe_allow_html=True)
#     st.markdown('</div>', unsafe_allow_html=True)

# elif selected == "Upload & Extract":
#     st.markdown("<h2>📄 Upload PDF for Information Extraction</h2>", unsafe_allow_html=True)
#     st.markdown('<div class="upload-area">', unsafe_allow_html=True)
#     uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", label_visibility="collapsed")

#     if uploaded_file:
#         st.success(f"Uploaded: {uploaded_file.name}")
#     else:
#         st.markdown("<p>Drop your PDF file here or click to browse</p>", unsafe_allow_html=True)

#     st.markdown('</div>', unsafe_allow_html=True)
#     col1, col2, col3 = st.columns([1, 1, 1])
#     with col2:
#         process_button = st.button("Extract Information", use_container_width=True)

#     if uploaded_file and process_button:
#         with st.spinner("Processing document..."):
#             try:
#                 files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
#                 response = requests.post("http://localhost:8000/extract_info", files=files, timeout=100000)
#                 st.success("✅ Extraction Complete!")

#                 with st.expander("🔍 View Raw Response"):
#                     st.text(response.text)

#                 try:
#                     result = response.json()
#                     with st.expander("🧾 View JSON Output"):
#                         st.json(result)

#                     st.markdown("### 📦 Extracted Results")
#                     for key in sorted(result.keys(), key=lambda x: int(x)):
#                         st.markdown(f"#### 📄 Document: {key}")
#                         try:
#                             parsed_data = json.loads(result[key])
#                             extracted_data = parsed_data.get("ExtractedData", {})

#                             if extracted_data:
#                                 main_data = {k: v for k, v in extracted_data.items() if k != "Notes"}
#                                 df_main = pd.DataFrame(main_data.items(), columns=["Field", "Value"])
#                                 st.table(df_main)

#                                 notes = extracted_data.get("Notes", {}).get("Note", [])
#                                 if notes:
#                                     st.markdown("##### 🗒️ Notes")
#                                     df_notes = pd.DataFrame(notes, columns=["Notes"])
#                                     st.table(df_notes)
#                                 else:
#                                     st.info("No notes found.")
#                             else:
#                                 st.warning(f"No 'ExtractedData' in response for document {key}.")

#                         except Exception as e:
#                             st.error(f"Error parsing key {key}: {e}")
#                 except json.JSONDecodeError:
#                     st.error("⚠️ Response is not valid JSON.")
#             except requests.exceptions.ConnectionError:
#                 st.error("🚫 Could not connect to FastAPI backend. Make sure it's running.")

# elif selected == "Search":
#     st.markdown('<div class="content-card fade-in">', unsafe_allow_html=True)
#     st.markdown("<h2>🔎 Search Extracted Data</h2>", unsafe_allow_html=True)
#     filter_expander = st.checkbox("⚙️", key="filter_toggle", help="Show filters")

#     product_number = product_family = drawing_number = engineer_name = ""
#     if filter_expander:
#         with st.expander("Filter Search Options", expanded=True):
#             col_a, col_b = st.columns(2)
#             with col_a:
#                 product_number = st.text_input("🔢 Product Number")
#                 product_family = st.text_input("🏷️ Product Family")
#             with col_b:
#                 drawing_number = st.text_input("🖼️ Drawing Number")
#                 engineer_name = st.text_input("👷 Engineer Name")

#     search_clicked = st.button("🔍 Search", use_container_width=True)

#     if search_clicked:
#         st.markdown('<div class="content-card">', unsafe_allow_html=True)
#         if any([product_number, product_family, drawing_number, engineer_name]):
#             st.markdown("### Results")
#             st.info("No matching results found for your search criteria (yet).")
#         else:
#             st.warning("Please enter a search term or use at least one filter.")
#         st.markdown('</div>', unsafe_allow_html=True)
#     else:
#         st.markdown("""
#         <div style="text-align: center; padding: 2rem; color: #6c757d;">
#             <i class="fas fa-search" style="font-size: 3rem;"></i>
#             <p style="margin-top: 1rem;">Enter a search term or use filters, then click 'Search'</p>
#         </div>
#         """, unsafe_allow_html=True)

#     st.markdown('</div>', unsafe_allow_html=True)
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

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background-color: black;
    }
    h1, h2, h3 {
        font-family: 'Helvetica Neue', sans-serif;
        color: white;
    }
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
    .main .block-container {
        padding-top: 1rem;
    }
    .fade-in {
        animation: fadeIn 0.5s;
    }
    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
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
    with col1:
        st.markdown("<div style='text-align: center; padding: 1rem;'><h3>📄 Upload</h3><p>Upload your PDF documents for information extraction</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div style='text-align: center; padding: 1rem;'><h3>🔍 Extract</h3><p>Automatically extract structured data</p></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div style='text-align: center; padding: 1rem;'><h3>🔎 Search</h3><p>Search through your extracted document data</p></div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Upload & Extract Page
# elif selected == "Upload & Extract":
#     st.markdown("<h2>📄 Upload PDF for Information Extraction</h2>", unsafe_allow_html=True)
#     st.markdown('<div class="upload-area">', unsafe_allow_html=True)
#     uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", label_visibility="collapsed")

#     if uploaded_file:
#         st.success(f"Uploaded: {uploaded_file.name}")
#     else:
#         st.markdown("<p>Drop your PDF file here or click to browse</p>", unsafe_allow_html=True)
#     st.markdown('</div>', unsafe_allow_html=True)

#     col1, col2, col3 = st.columns([1, 1, 1])
#     with col2:
#         process_button = st.button("Extract Information", use_container_width=True)

#     if uploaded_file and process_button:
#         with st.spinner("Processing document..."):
#             try:
#                 files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
#                 response = requests.post("http://localhost:8000/extract_info", files=files, timeout=100000)
#                 st.success("✅ Extraction Complete!")

#                 with st.expander("🔍 View Raw Response"):
#                     st.text(response.text)

#                 try:
#                     result = response.json()

#                     # Sort keys numerically
#                     doc_keys = sorted(result.keys(), key=lambda x: int(x))

#                     # Setup session state for navigation
#                     if 'doc_index' not in st.session_state:
#                         st.session_state.doc_index = 0

#                     # Navigation
#                     if len(doc_keys) > 1:
#                         col_nav1, col_nav2, col_nav3 = st.columns([1, 2, 1])
#                         with col_nav1:
#                             if st.button("◀️ Previous") and st.session_state.doc_index > 0:
#                                 st.session_state.doc_index -= 1
#                         with col_nav3:
#                             if st.button("Next ▶️") and st.session_state.doc_index < len(doc_keys) - 1:
#                                 st.session_state.doc_index += 1
#                         current_doc = doc_keys[st.session_state.doc_index]
#                         st.markdown(f"### 📄 Document: {current_doc} of {len(doc_keys)}")
#                     else:
#                         current_doc = doc_keys[0]
#                         st.markdown(f"### 📄 Document: {current_doc}")

#                     # Parse and display selected document
#                     parsed_data = json.loads(result[current_doc])
#                     extracted_data = parsed_data.get("ExtractedData", {})

#                     if extracted_data:
#                         main_data = {k: v for k, v in extracted_data.items() if k != "Notes"}
#                         df_main = pd.DataFrame(main_data.items(), columns=["Field", "Value"])
#                         st.table(df_main)

#                         notes = extracted_data.get("Notes", {}).get("Note", [])
#                         if notes:
#                             st.markdown("##### 🗒️ Notes")
#                             df_notes = pd.DataFrame(notes, columns=["Notes"])
#                             st.table(df_notes)
#                     else:
#                         st.warning(f"No 'ExtractedData' in response for document {current_doc}.")

#                 except json.JSONDecodeError:
#                     st.error("⚠️ Response is not valid JSON.")

#             except requests.exceptions.ConnectionError:
#                 st.error("🚫 Could not connect to FastAPI backend. Make sure it's running.")
# Upload & Extract Page
elif selected == "Upload & Extract":
    st.markdown("<h2>📄 Upload PDF for Information Extraction</h2>", unsafe_allow_html=True)
    st.markdown('<div class="upload-area">', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", label_visibility="collapsed")

    # Initialize session state variables
    for key in ["last_uploaded_file", "doc_index", "extracted_result", "doc_keys"]:
        if key not in st.session_state:
            st.session_state[key] = None if key == "last_uploaded_file" else 0 if key == "doc_index" else {}

    # Reset state on new upload
    if uploaded_file is not None:
        current_filename = uploaded_file.name
        if st.session_state.last_uploaded_file != current_filename:
            st.session_state.last_uploaded_file = current_filename
            st.session_state.doc_index = 0
            st.session_state.extracted_result = {}
            st.session_state.doc_keys = []

        st.success(f"Uploaded: {uploaded_file.name}")
    else:
        st.markdown("<p>Drop your PDF file here or click to browse</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        process_button = st.button("Extract Information", use_container_width=True)

    if uploaded_file and process_button:
        with st.spinner("Processing document..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                response = requests.post("http://localhost:8000/extract_info", files=files, timeout=100000)
                st.success("✅ Extraction Complete!")

                with st.expander("🔍 View Raw Response"):
                    st.text(response.text)

                try:
                    result = response.json()
                    doc_keys = sorted(result["extracted_entities"].keys(), key=lambda x: int(x))

                    # Save result to session state for persistence
                    st.session_state.extracted_result = result
                    st.session_state.doc_keys = doc_keys

                except json.JSONDecodeError:
                    st.error("⚠️ Response is not valid JSON.")
                    
            except requests.exceptions.ConnectionError:
                st.error("🚫 Could not connect to FastAPI backend. Make sure it's running.")
           

    # If we already have a result, allow navigation and display
    if st.session_state.extracted_result and st.session_state.doc_keys:
        result = st.session_state.extracted_result
        doc_keys = st.session_state.doc_keys

        # Navigation
        if len(doc_keys) > 1:
            col_nav1, col_nav2, col_nav3 = st.columns([1, 2, 1])
            with col_nav1:
                if st.button("◀️ Previous") and st.session_state.doc_index > 0:
                    st.session_state.doc_index -= 1
            with col_nav3:
                if st.button("Next ▶️") and st.session_state.doc_index < len(doc_keys) - 1:
                    st.session_state.doc_index += 1

            current_doc = doc_keys[st.session_state.doc_index]
            st.markdown(f"### 📄 Document: {current_doc} of {len(doc_keys)}")
        else:
            current_doc = doc_keys[0]
            st.markdown(f"### 📄 Document: {current_doc}")

        # Parse and display selected document
        try:
            parsed_data = json.loads(result["extracted_entities"][current_doc])
            extracted_data = parsed_data.get("ExtractedData", {})

            if extracted_data:
                main_data = {k: v for k, v in extracted_data.items() if k != "Notes"}
                df_main = pd.DataFrame(main_data.items(), columns=["Field", "Value"])
                st.table(df_main)

                notes = extracted_data.get("Notes", {}).get("Note", [])
                if notes:
                    st.markdown("##### 🗒️ Notes")
                    df_notes = pd.DataFrame(notes, columns=["Notes"])
                    st.table(df_notes)
            else:
                st.warning(f"No 'ExtractedData' in response for document {current_doc}.")

        except Exception as e:
            st.error(f"⚠️ Failed to parse extracted data: {e}")

        st.markdown("---")

        # Save to DB
        if st.button("💾 Save "):
            with st.spinner("⏳ Saving data to the database..."):
                try:
                    extracted_entities_clean = {
                        k: json.loads(v) for k, v in result.get("extracted_entities", {}).items()
                    }

                    save_payload = {
                        "filename": result.get("filename"),
                        "extracted_entities": extracted_entities_clean
                    }

                    save_response = requests.post("http://localhost:8000/save_db", json=save_payload, timeout=60)

                    if save_response.status_code == 200:
                        st.success("✅ Data successfully saved to database!")
                    else:
                        st.error(f"❌ Failed to save: {save_response.text}")
                except Exception as e:
                    st.error(f"⚠️ Error: {str(e)}")


      

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
        if any([product_number, product_family, drawing_number, engineer_name]):
            st.markdown("### Results")
            st.info("No matching results found for your search criteria (yet).")
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
