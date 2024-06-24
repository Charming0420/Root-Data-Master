import streamlit as st
import os
import pandas as pd
from main import main  

st.title('VC Data CSV Generator')

url = st.text_input('Enter URL')

if st.button('Generate CSV'):
    if url:
        main(url)
        data_dir = os.path.join(os.path.dirname(__file__), '..', 'Data')
        latest_file = max([f for f in os.listdir(data_dir) if f.endswith('.csv')],
                          key=lambda f: os.path.getctime(os.path.join(data_dir, f)))
        with open(os.path.join(data_dir, latest_file), 'rb') as f:
            st.download_button('Download CSV', f, file_name=latest_file)