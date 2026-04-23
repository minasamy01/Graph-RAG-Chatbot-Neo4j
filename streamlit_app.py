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

    # show assistant answer
    with st.chat_message("assistant"):
        st.markdown(answer)

        # 🔥 Debug info
        with st.expander("🧾 Generated Cypher"):
            st.code(cypher, language="cypher")

        with st.expander("📊 Raw Results"):
            st.write(results)

    st.session_state.messages.append({"role": "assistant", "content": answer})