import streamlit as st

uploaded_files = st.file_uploader(
    "Choose a h5 file to upload", accept_multiple_files=True, type=['h5']
)

for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    with open(uploaded_file.name+".h5", "wb") as f:
        f.write(bytes_data)
    st.info(uploaded_file.name+".h5 upload success!")
