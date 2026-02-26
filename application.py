import streamlit as st
#from streamlit_pdf_viewer import pdf_viewer
import pandas as pd
import json 


modelId = 'us.anthropic.claude-3-5-sonnet-20241022-v2:0'
# modelId = 'us.anthropic.claude-sonnet-4-5-20250929-v1:0'
# modelId = 'qwen.qwen3-vl-235b-a22b'
# modelId = 'us.anthropic.claude-haiku-4-5-20251001-v1:0'
# print(response_text)
from langchain_aws import ChatBedrockConverse

llm = ChatBedrockConverse(
    model_id=modelId,
    region_name="us-east-2",
    max_tokens=4000,
    aws_access_key_id=st.session_state["aws_credentials"]["aws_access_key"],
    aws_secret_access_key=st.session_state["aws_credentials"]["aws_secret_key"],
    aws_session_token=st.session_state["aws_credentials"]["aws_session_token"],
    # temperature=0,
    # additional_model_request_fields={
    #     "thinking": {"type": "enabled", "budget_tokens": 1024},
    # },
)


st.logo("Doclens_logo.png", size="large")
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

# # * Make Streamlit logo bigger */
# # [data-testid="stSidebar"] img[src*="DocsLens_WhiteText.svg"] {
# #     width: 250px !important;
# #     height: auto !important;
# # }

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


st.markdown(
    """
    <style>
    .card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
    }
    .section-title {
        font-size: 20px;
        font-weight: 600;
        margin-bottom: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with open("quote.json", 'r') as f:
    quote_data = json.load(f)
with open("application.md", 'r') as f:
    md = f.read()
    
st.set_page_config(layout="wide")
st.markdown("""
<style>
[data-testid="stTabs"] button {
    font-size: 18px;
    padding: 8px 16px;
}
</style>
""", unsafe_allow_html=True)
# tab1, tab2, tab3  = st.tabs(["📄    **Document View**  ", "🛢     **Data**     ", "💬    **Chat**   "])
tab1, tab3 = st.tabs(["📄 **PDF & Data View**   ", "💬    **Chat**   "])
# tab1, tab2, tab3 = st.tabs(["📄 **Document View**  ", "🛢   **Data** ", "💬    **Chat**   "])

with tab1:
    col1, col2 = st.columns(spec=[2, 2], gap="xlarge", width=2000)
    with col1 :
    # st.subheader("*Document view*")
        st.pdf("Limousine_Quotation_Application_Fleet_fillable.pdf", height=600)
    # pdf_viewer("Limousine_Quotation_Application_Fleet_fillable.pdf", zoom_level=1.25)
    with col2:
        with st.container(height=600):
            st.markdown(md)
# with tab2:
#     st.markdown(md)
with tab3:
    col1, col2 = st.columns(spec=[2, 2], gap="xlarge", width=2000)
    with col1:
        with st.container(height=600):
            st.markdown(md)
    with col2 :
        st.subheader("Chat with data..")
        if "csv_messages" not in st.session_state:
            st.session_state.csv_messages = []

        if custom_text := st.chat_input("Enter your query here..."):
            print(custom_text)
        with st.container(height=500):
            if custom_text:

                prompt = custom_text
                # Display user message in chat message container
                with st.chat_message("user"):
                        st.markdown(prompt)
                with st.chat_message("assistant"):
                    with st.spinner("Searching the data ..."):
                        response = llm.invoke(prompt + md)
                    # response_text = re.sub(r'\$(.*)\$', r'\$\1\$',response[0]["text"])
                    st.markdown(response.content)
                    print(response.content)
                    st.session_state.csv_messages.append({"role": "assistant", "content": response.content})
                    # Add user message to chat history
                    st.session_state.csv_messages.append({"role": "user", "content": prompt})

            # Display chat csv_messages from history on app rerun
            for message in st.session_state.csv_messages[:-2][::-1]:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
# with tab3:
#     # st.subheader("*Quotation Application Data*")
#     for k, v in quote_data.items():
#         section_hdr = f"""
#         <div class="section-title">{k}</div>
#         """
#         st.markdown(section_hdr, unsafe_allow_html=True)
#         st.json(v)
    # st.write(df)
    # st.json(data)
