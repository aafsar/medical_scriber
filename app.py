import streamlit as st

from config import APP_MODE

st.set_page_config(page_title="Angy Voice", layout="wide")

pages = [st.Page("consultation.py", title="Consultation", default=True)]
if APP_MODE == "dev":
    pages.append(st.Page("pages/test_runner.py", title="Test Runner"))

pg = st.navigation(pages)
pg.run()
