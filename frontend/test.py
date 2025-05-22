import streamlit as st
import requests
import json
import pandas as pd

# Initialize session state for extraction results if it doesn't exist
if 'extraction_result' not in st.session_state:
    st.session_state.extraction_result = None
if 'doc_index' not in st.session_state:
    st.session_state.doc_index = 0

uploaded_file = st.file_uploader("Upload PDF document", type="pdf")
process_button = st.button("Process Document")

if uploaded_file and process_button:
    with st.spinner("Processing document..."):
        try:
            files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
            response = requests.post("http://localhost:8000/extract_info", files=files, timeout=100000)
            st.success("✅ Extraction Complete!")
            try:
                result = response.json()
                # Store entire response in session_state for navigation
                st.session_state.extraction_result = result
                # Reset doc_index when new extraction done
                st.session_state.doc_index = 0
            except json.JSONDecodeError:
                st.error("⚠️ Response is not valid JSON.")
                st.session_state.extraction_result = None
        except requests.exceptions.ConnectionError:
            st.error("🚫 Could not connect to FastAPI backend. Make sure it's running.")
            st.session_state.extraction_result = None

# Now use stored extraction_result for navigation and display
if 'extraction_result' in st.session_state and st.session_state.extraction_result:
    result = st.session_state.extraction_result
    doc_keys = sorted(result.keys(), key=lambda x: int(x))
    
    if len(doc_keys) > 1:
        col_nav1, col_nav2, col_nav3 = st.columns([1, 2, 1])
        with col_nav1:
            if st.button("◀️ Previous") and st.session_state.doc_index > 0:
                st.session_state.doc_index -= 1
        with col_nav3:
            if st.button("Next ▶️") and st.session_state.doc_index < len(doc_keys) - 1:
                st.session_state.doc_index += 1
        current_doc = doc_keys[st.session_state.doc_index]
        st.markdown(f"### 📄 Document: {st.session_state.doc_index + 1} of {len(doc_keys)}")
    else:
        current_doc = doc_keys[0]
        st.markdown(f"### 📄 Document: {current_doc}")
    
    parsed_data = json.loads(result[current_doc])
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