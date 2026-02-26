import streamlit as st
import pandas as pd
import json
import re
from langchain_aws import ChatBedrockConverse

modelId = 'us.anthropic.claude-3-5-sonnet-20241022-v2:0'
# modelId = 'us.anthropic.claude-sonnet-4-5-20250929-v1:0'

llm = ChatBedrockConverse(
    model_id=modelId,
    region_name="us-east-2",
    max_tokens=1500,
    aws_access_key_id=st.session_state["aws_credentials"]["aws_access_key"],
    aws_secret_access_key=st.session_state["aws_credentials"]["aws_secret_key"],
    aws_session_token=st.session_state["aws_credentials"]["aws_session_token"],
    # temperature=0,
    # additional_model_request_fields={
    #     "thinking": {"type": "enabled", "budget_tokens": 1024},
    # },
)

st.logo("Doclens_logo.png", size="large")

with open("policy.json", 'r') as f:
    policy_data = json.load(f)
with open("acord.md", 'r') as f:
    md = f.read()

st.set_page_config(layout="wide")

tab1, tab2 = st.tabs(["📄 **PDF & Data View**   ", "💬    **Chat**   "])

with tab1:
    col1, col2 = st.columns(spec=[2, 2], gap="xlarge", width=2000)
    with col1 :
        st.pdf("Acord-125-Commercial-Insurance.pdf", height=600)
    # pdf_viewer("Acord-125-Commercial-Insurance.pdf", zoom_level=1.25)
    with col2:
        with st.container(height=600):
            st.markdown(md)

with tab2:
    col1, col2 = st.columns(spec=[2, 2], gap="xlarge", width=2000)
    with col1:
        with st.container(height=600):
            st.markdown(md)
    with col2 :
        st.subheader("Chat with data..")
        if "acord_chat" not in st.session_state:
            st.session_state.acord_chat = []

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
                    st.session_state.acord_chat.append({"role": "assistant", "content": response.content})
                    # Add user message to chat history
                    st.session_state.acord_chat.append({"role": "user", "content": prompt})

            # Display chat acord_chat from history on app rerun
            for message in st.session_state.acord_chat[:-2][::-1]:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
