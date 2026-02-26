import streamlit as st
import pandas as pd
import json
import os
# add_logo("logo-blue.png", height=10)
st.markdown("""
<style>

# @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

# /* ===== GLOBAL FONT (Inter) ===== */
# html, body, [class*="css"]  {
#     font-family: 'Inter', sans-serif !important;
# }

# section[data-testid="stSidebar"] {
#     width: 300px !important;  /* Change 300px to whatever width you want */
#     min-width: 300px !important;
#     max-width: 300px !important;
# }

# /* ===== RIGHT SIDE MAIN PANEL (WHITE) ===== */
# .stApp {
#     background: white !important;
#     color: #000000 !important;
# }

# /* ===== LEFT SIDEBAR GRADIENT ===== */
# section[data-testid="stSidebar"] {
#     background: linear-gradient(to bottom, #4A5166, #4A5166) !important;
#     color: white !important;
#     padding-top: 20px !important;
# }

# /* Hide default Streamlit sidebar header */
# [data-testid="stSidebarHeader"] {
#     display: none !important;
# }

# section[data-testid="stSidebar"] code {
#     background-color: transparent !important;
#     color: #fff !important;
#     padding: 0 !important;
# }

# /* Make sidebar components readable */
# section[data-testid="stSidebar"] * {
#     color: white !important;
# }

# /* Optional: round sidebar edges */
# section[data-testid="stSidebar"] > div {
#     border-radius: 0px 12px 12px 0px;
# }

# section[data-testid="stSidebar"] * {
#     color: white !important;
# }

# /* Change select background color */
# section[data-testid="stSidebar"] details > summary {
#     background-color: #4A5166 !important;
#     border-radius: 6px !important;
#     padding: 12px !important;
#     cursor: pointer !important;
# }
# /* OPTIONAL: Change hover */
# section[data-testid="stSidebar"] details > summary:hover {
#     background-color: #2E374F !important;
# }

# /* Unselected tab labels */
# .stTabs [data-baseweb="tab"] {
#     color: #4A5166 !important;
# }

# .stTabs [data-baseweb="tab"][aria-selected="true"] {
#     color: #85ae41 !important;
#     font-wight: 600 !important;
# }

# /* Selectbox container */
# /* MAIN SELECT COMPONENT WRAPPER */
# div[data-baseweb="select"] {
#     background-color: #4A5166 !important;
#     border-radius: 6px !important;
#     color: white !important;
# }
# /* INNER BOX THAT SHOWS THE SELECTED VALUE */
# div[data-baseweb="select"] > div {
#     background-color: #4A5166 !important;
#     border-radius: 6px !important;
#     cursor: pointer !important;
# }
# /* SELECTED VALUE TEXT */
# div[data-baseweb="select"] .st-d9 {
#     background-color: #4A5166 !important;
#     color: white !important;
# }

# * Make Streamlit logo bigger */
# [data-testid="stSidebarHeader"] img[src*="DocsLens_WhiteText.svg"] {
#     width: 250px !important;
#     height: auto !important;
# }

# /* Main multi-select container */
# div[data-testid="stMultiSelect"] > div > div[data-baseweb="select"] > div {
#     background-color: #f5f5f5 !important;
#     cursor: pointer !important;
# }
# /* Placeholder text ("Choose options") */
# div[data-baseweb="select"] > div > div[aria-hidden="true"] span {
#     color: white !important;
# }


</style>
""", unsafe_allow_html=True)
# st.markdown(
#     """
#     <style>
#         [data-testid="stSidebarHeader"] {
#             background-image: "DocsLens_WhiteText.svg";
#             background-repeat: no-repeat;
#             padding-top: 60px;
#             background-position: 20px 20px;
#         }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )
pages = {
    "Submission 1": [
        st.Page("acord.py", title="ACORD application"),
        st.Page("lossrun.py", title="Loss Run"),
        st.Page("application.py", title="Supplemental application"),
             
    ],
}

pg = st.navigation(pages)

pg.run()

# st.sidebar.write("Add Submission")
uploaded_files = st.sidebar.file_uploader(
    "Add Submission", accept_multiple_files="directory", type=["csv", "pdf"]
)

# st.session_state.acord_chat = []
# for file in uploaded_files:
    
# -----------------------------
# Init routing state
# -----------------------------
# if "page" not in st.session_state:
#     st.session_state.page = "website_summary"

# -----------------------------
# Sidebar
# -----------------------------
# with st.sidebar:
#     # st.text_input("Search")

#     # st.markdown("### Overview")
#     # if st.button("Overview", use_container_width=True):
#     #     st.session_state.page = "overview"

#     st.markdown("## Business Data")
#     if st.button("ACORD Application", use_container_width=True):
#         st.session_state.page = "acord"
#     if st.button("Supplemental Application", use_container_width=True):
#         st.session_state.page = "supplemental"

# def acord():
#     df = pd.read_csv("acord.csv")
#     st.logo("DocsLens_WhiteText.svg")

#     # pdf_viewer("Acord-125-Commercial-Insurance.pdf", zoom_level=1.0)
#     # csv_col1, csv_col2 = st.columns(spec=[10, 8], gap="xlarge", width=2000)
#     tab1, tab2 = st.tabs(["**Document View**", "**Extracted Data**"])
#     with tab1 :
#         # st.subheader("Document view")
#         st.pdf("Acord-125-Commercial-Insurance.pdf", height=600)
#     with tab2:
#         st.subheader("Data")
#         st.write(df)
# def quote():
#     with open("quote.json", 'r') as f:
#         data = json.load(f)
#     # pdf_viewer("Acord-125-Commercial-Insurance.pdf", zoom_level=1.0)
#     csv_col1, csv_col2 = st.columns(spec=[10, 8], gap="xlarge", width=2000)
#     with csv_col1:
#         st.subheader("Document view**")
#         st.pdf("Limousine_Quotation_Application_Fleet_fillable.pdf", height=600)
#     with csv_col2:
#         st.subheader("Quotation Data")
#         # st.write(df)
#         st.json(data)
