import streamlit as st
from graph_rag import chat

st.set_page_config(page_title="Graph Chat", page_icon="🧠")

st.title("🧠 Neo4j Graph Chatbot")

# =========================
# SESSION STATE
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# CLEAR BUTTON
# =========================
if st.button("🗑 Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# =========================
# SHOW HISTORY
# =========================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =========================
# INPUT
# =========================
if prompt := st.chat_input("Ask your graph..."):

    # show user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # run model
    with st.spinner("Thinking..."):
        answer, cypher, results = chat(prompt, debug=True)

    # تقسيم الشاشة لعرض الـ Debug جنباً إلى جنب مع الإجابة
    col1, col2 = st.columns([1, 1])
    
    with col1:
        with st.expander("🛠 Developer Tools", expanded=True):
            st.subheader("📌 Generated Cypher")
            st.code(cypher, language="cypher")
            st.subheader("📊 Database Results")
            st.json(results)

    with col2:
        with st.chat_message("assistant"):
            st.success(answer)