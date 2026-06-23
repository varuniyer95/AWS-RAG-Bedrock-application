import streamlit as st
import requests
import json
from dotenv import load_dotenv
import os

#load environment variables
load_dotenv()

# =====================================================
# ENDPOINTS
# =====================================================

QUERY_URL = os.getenv("QUERY_URL")
UPLOAD_URL = os.getenv("UPLOAD_URL")
SYNC_URL = os.getenv("SYNC_URL")

# Optional validation
required_vars = {
    "QUERY_URL": QUERY_URL,
    "UPLOAD_URL": UPLOAD_URL,
    "SYNC_URL": SYNC_URL,
}

missing = [k for k, v in required_vars.items() if not v]

if missing:
    st.error(
        f"Missing environment variables: {', '.join(missing)}"
    )
    st.stop()

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Bedrock KB Chat",
    layout="wide"
)

st.title("Bedrock Knowledge Base Chat")

# =====================================================
# SESSION STATE
# =====================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = None

if "last_sync_job" not in st.session_state:
    st.session_state.last_sync_job = None

# =====================================================
# HELPERS
# =====================================================

def trigger_sync():

    sync_response = requests.post(
        SYNC_URL,
        json={},
        timeout=60
    )

    sync_response.raise_for_status()

    sync_data = sync_response.json()

    if "body" in sync_data:
        sync_data = json.loads(sync_data["body"])

    job_id = sync_data.get("ingestionJobId")
    status = sync_data.get("status")

    st.session_state.last_sync_job = job_id

    return {
        "job_id": job_id,
        "status": status
    }


def upload_file_to_s3(file):
    """
    Upload file using presigned URL.
    """

    payload = {
        "fileName": file.name,
        "contentType": file.type
    }

    upload_response = requests.post(
        UPLOAD_URL,
        json=payload,
        timeout=30
    )

    upload_response.raise_for_status()

    upload_data = upload_response.json()

    upload_url = upload_data["uploadUrl"]

    put_response = requests.put(
        upload_url,
        data=file.getvalue(),
        headers={
            "Content-Type": file.type
        }
    )

    put_response.raise_for_status()

    return upload_data


def parse_response(resp):

    data = resp.json()

    # API Gateway wrapper support
    if "body" in data:
        data = json.loads(data["body"])

    return data


def render_citations(citations):

    if not citations:
        return

    with st.expander("Sources / Citations", expanded=False):

        seen_sources = set()

        for c in citations:

            text = c.get("text", "")
            s3_uri = c.get("s3_uri")
            metadata = c.get("metadata", {})

            if s3_uri and s3_uri not in seen_sources:
                seen_sources.add(s3_uri)
                st.markdown(f"**Source:** `{s3_uri}`")

            if metadata:
                st.json(metadata)

            if text:
                st.caption(
                    text[:400] + "..."
                    if len(text) > 400
                    else text
                )

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.header("Knowledge Base")

    # -----------------------------
    # FILE UPLOAD
    # -----------------------------

    file = st.file_uploader(
        "Upload document",
        type=["pdf", "txt", "docx", "md"]
    )

    if file:

        if st.button(
            "Upload & Sync",
            use_container_width=True
        ):

            try:

                upload_file_to_s3(file)

                st.success("File uploaded successfully")

                job_id = trigger_sync()

                st.success(
                    f"Sync started\n\nJob ID: {job_id}"
                )

            except Exception as e:

                st.error(
                    f"Upload/Sync failed: {str(e)}"
                )

    st.divider()

    # -----------------------------
    # MANUAL SYNC BUTTON
    # -----------------------------

    st.subheader("Knowledge Base Sync")

    st.caption(
        "Use this when documents are added, modified, "
        "or deleted directly in S3."
    )

    if st.button(
            "Force Sync Knowledge Base",
            use_container_width=True
    ):

        try:

            with st.spinner("Starting knowledge base sync..."):

                result = trigger_sync()

            st.success(
                f"""
    Knowledge base sync started successfully.

    Job ID: {result['job_id']}
    Status: {result['status']}
    """
            )

        except Exception as e:

            st.error(
                f"Failed to start sync: {str(e)}"
            )

# =====================================================
# CHAT HISTORY
# =====================================================

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.markdown(msg["content"])

        if (
            msg["role"] == "assistant"
            and "citations" in msg
        ):
            render_citations(msg["citations"])

# =====================================================
# CHAT INPUT
# =====================================================

query = st.chat_input(
    "Ask something from your knowledge base..."
)

if query:

    # --------------------------------
    # USER MESSAGE
    # --------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )

    with st.chat_message("user"):
        st.markdown(query)

    # --------------------------------
    # ASSISTANT MESSAGE
    # --------------------------------

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                payload = {
                    "query": query,
                    "sessionId": st.session_state.session_id
                }

                response = requests.post(
                    QUERY_URL,
                    json=payload,
                    timeout=120
                )

                response.raise_for_status()

                data = parse_response(response)

                answer = data.get("answer", "")
                citations = data.get("citations", [])
                session_id = data.get("sessionId")

                st.session_state.session_id = session_id

                st.markdown(answer)

                render_citations(citations)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "citations": citations
                    }
                )

            except Exception as e:

                error = f"Error: {str(e)}"

                st.error(error)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error,
                        "citations": []
                    }
                )