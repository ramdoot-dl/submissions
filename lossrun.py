# app.py
import streamlit as st
from main import ask_agent, configure_agent

import streamlit as st
import pandas as pd
import re


st.set_page_config(layout="wide")
tab1, tab2 = st.tabs(["📄**Document & Data View** ", "💬 **Loss Run Agent**"])


CSV_FILE = "Loss Run.csv"
IMAGE = "loss-run-cw.pdf"

st.logo("Doclens_logo.png", size="large")
# st.sidebar.image("DocsLens_WhiteText.svg", width=200)  # 3rem ≈ 48px

add_selectbox = st.sidebar.selectbox(
    'Select Loss Run document',
    (CSV_FILE, IMAGE)
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
        if "lr_messages" not in st.session_state:
            st.session_state.lr_messages = []
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
                    configure_agent(st.session_state["aws_credentials"])
                    response, df_filtered = ask_agent(prompt, use_cat, filename=st.session_state.filename)
                response_text = re.sub(r'\$(.*)\$', r'\$\1\$',response[0]["text"])
                st.markdown(response_text)
                st.markdown("***This summary was generated using below filtered data from the document..***")
                st.dataframe(df_filtered)
                print(response)
                st.session_state.lr_messages.append({"role": "assistant", "content": response_text, "dataframe": df_filtered})
                # Add user message to chat history
                st.session_state.lr_messages.append({"role": "user", "content": prompt})

        # Display chat lr_messages from history on app rerun
        for message in st.session_state.lr_messages[:-2][::-1]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if message["role"] == "assistant":
                    if message["dataframe"]:
                        st.dataframe(message["dataframe"])

