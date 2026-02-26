import streamlit as st
import pandas as pd

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


def main():
    try:
        if "aws_credentials" not in st.session_state:
            st.session_state["aws_credentials"] = None

        if st.session_state["aws_credentials"] is None:

            aws_access_key = st.text_input(
                "Enter AWS Access Key", type="password", key="aws_access_key"
            )
            aws_secret_key = st.text_input(
                "Enter AWS Secret Key", type="password", key="aws_secret_key"
            )
            aws_session_token = st.text_input(
                "Enter AWS Session Token (if applicable)",
                type="password",
                key="aws_session_token",
            )

            if st.button("✅ Save Credentials"):
                if not aws_access_key or not aws_secret_key:
                    st.error("Access key and secret key are required")
                else:
                    st.session_state["aws_credentials"] = {
                        "aws_access_key": aws_access_key,
                        "aws_secret_key": aws_secret_key,
                        "aws_session_token": aws_session_token,
                    }
                    st.success("Credentials saved")
                    st.rerun()

        if st.session_state["aws_credentials"] is not None:
            pages = {
                "Submission 1": [
                    st.Page("acord.py", title="ACORD application"),
                    # st.Page("lossrun.py", title="Loss Run"),
                    st.Page("application.py", title="Supplemental application"),
                        
                ],
            }

            pg = st.navigation(pages)

            pg.run()

    # st.sidebar.write("Add Submission")
    # uploaded_files = st.sidebar.file_uploader(
    #     "Add Submission", accept_multiple_files="directory", type=["csv", "pdf"]
    # )

            # Instructions in sidebar
            with st.sidebar:

                if st.button("🔄 Change Credentials"):
                    st.session_state["aws_credentials"] = None
                    st.rerun()

    except Exception as e:
        st.error(f"Error capturing AWS credentials: {str(e)}")
        return
    

if __name__ == "__main__":
    main()