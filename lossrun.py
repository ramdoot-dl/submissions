# app.py
import streamlit as st
from main import ask_agent

import streamlit as st
import pandas as pd
import re

# st.markdown("""
# <style>

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
# [data-testid="stSidebar"] img[src*="DocsLens_WhiteText.svg"] {
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


# </style>
# """, unsafe_allow_html=True)
st.set_page_config(layout="wide")
tab1, tab2 = st.tabs(["📄**Document & Data View** ", "💬 **Loss Run Agent**"])



# st.set_page_config(page_title="Loss Run Agent", layout="centered")
#CSV_FILE = "UF Health Loss Run - 7.1.2024-2025PIIRemoved.csv"
CSV_FILE = "Loss Run.csv"
# CSV_FILE= "test.csv"
# CSV_FILE = "loss-run-redacted_10.csv"
IMAGE = "Scan_OCT_11.pdf"
IMAGE = "loss-run-cw.pdf"

st.logo("Doclens_logo.png", size="large")
# st.sidebar.image("DocsLens_WhiteText.svg", width=200)  # 3rem ≈ 48px

add_selectbox = st.sidebar.selectbox(
    'Select Loss Run document',
    (IMAGE, CSV_FILE)
)
if add_selectbox == CSV_FILE:
    st.session_state.filename = CSV_FILE
    df = pd.read_csv(CSV_FILE)
elif add_selectbox == IMAGE:
    IMAGE_CSV_FILE= "loss-run-cw.csv"
    st.session_state.filename = IMAGE_CSV_FILE
    df = pd.read_csv(IMAGE_CSV_FILE)
    
with tab1:
    if add_selectbox == IMAGE:
        # st.header("Image")
        col1, col2 = st.columns(spec=[2, 2], gap="xlarge", width=2000)
        with col1:
            st.pdf(IMAGE, height=800)
        with col2:
            st.subheader("Data Preview")
            st.dataframe(df, hide_index=True)
        # pdf_viewer(IMAGE, zoom_level=1.0)
        # st.image(IMAGE, caption='Loss Run Data Overview')       
        # csv_col1, csv_col2 = st.columns([6, 2])
        # with csv_col1:
        #     st.subheader("Data Preview")
        #     st.dataframe(df, hide_index=True)
        # with csv_col2:
        #     st.subheader("Columns")
        #     # st.write(df.dtypes)
        #     st.write(df.columns)

    elif add_selectbox == CSV_FILE:
        # st.header("CSV Data")
        csv_col1, csv_col2 = st.columns([6, 2])
        # print("csv", csv_col1)
        with csv_col2:
            st.subheader("Columns")
            # st.write(df.dtypes)
            # print(df.columns)
            st.write(df.columns)
        with csv_col1:
            st.subheader("Data Preview")
            st.dataframe(df, hide_index=True)
with tab2:

    st.title("Loss Run Agent")

    bt = ""
    extra_kw = []
    options = st.multiselect(
        "Select search terms",
        ["Death", "Birth", "Brain", "Neurological", "Fractures", "Anesthesia/resuscitation issues", "Other Deadly", "Abuse", "Batch/Class Actions", "Long Term Care"],
        default=["Death"],
    )
    col1, col2 = st.columns(2)
    value = None
    oper = "between"
    with col1:
        range = st.checkbox("$ Amount range")
        if range:
            value = st.slider("Select range to filter records", 0, 200000, (5000, 50000), step=5000)
            print(value)
    if st.button("Search"):
        if options != [] and value != None:
            bt = "List records related to  " + ", ".join(options) + " with total incurred between " + str(value[0]) + " and " + str(value[1]) + "."
        elif options != [] and value == None:
            bt = "List records related to " + ", ".join(options) + "."
        elif options == [] and value != None:
            bt = "List all records with total incurred between $" + str(value[0]) + " and $" + str(value[1]) + "."
        print(bt)
    # st.divider()

    # Free input
    # query = st.text_input("Ask the agent")
    with st.sidebar:
        help_expander = st.expander("Info & Examples", expanded=False)
        with help_expander:
            st.markdown("""
        **How to use this app**
        - **Select search terms & push the search button**.
        - **You may enter your own custom query in the chat. Example queries:**
            - **`Get total incurred for sepsis related incidents.`**
            - **`Get records for Liver Transplant and their total paid expenses.`**
        """)
    if add_selectbox == CSV_FILE or add_selectbox == IMAGE:
        if "csv_messages" not in st.session_state:
            st.session_state.csv_messages = []
        if "dataframes" not in st.session_state:
            st.session_state.dataframes = []
        if custom_text := st.chat_input("Enter your query here..."):
            print(custom_text)

        if custom_text or bt:
            if bt != "":
                prompt = bt
                use_cat = True
            else:
                prompt = custom_text
                use_cat = False
            # Display user message in chat message container
            with st.chat_message("user"):
                 st.markdown(prompt)
            with st.chat_message("assistant"):
                with st.spinner("Loss Run Agent is orchestrating available tools..."):
                    response, df_filtered = ask_agent(prompt, use_cat, filename=st.session_state.filename)
                response_text = re.sub(r'\$(.*)\$', r'\$\1\$',response[0]["text"])
                st.markdown(response_text)
                st.markdown("***This summary was generated using below filtered data from the document..***")
                st.dataframe(df_filtered)
                print(response)
                st.session_state.csv_messages.append({"role": "assistant", "content": response_text, "dataframe": df_filtered})
                # Add user message to chat history
                st.session_state.csv_messages.append({"role": "user", "content": prompt})

        # Display chat csv_messages from history on app rerun
        for message in st.session_state.csv_messages[:-2][::-1]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if message["role"] == "assistant":
                    if message["dataframe"]:
                        st.dataframe(message["dataframe"])
 
# if st.button("Run Agent", type="primary"):
#     if not query.strip():
#         st.warning("Please enter a question.")
#     else:
#         with st.spinner("Agent is thinking and calling tools..."):
#             response = ask_agent(query)
#         st.subheader("Answer")
#         st.markdown(response[0]["text"])
