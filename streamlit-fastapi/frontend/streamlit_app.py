import os

import requests
import streamlit as st


API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Emergency Call Center", page_icon=":rotating_light:", layout="wide")
st.title("Emergency Call Center")
st.caption("Simple call intake and priority queue")


def api_request(method: str, path: str, **kwargs):
    response = requests.request(method, f"{API_URL}{path}", timeout=10, **kwargs)
    response.raise_for_status()
    return response.json()


try:
    summary = api_request("GET", "/api/dashboard")
    metrics = st.columns(4)
    metrics[0].metric("Total calls", summary["total"])
    metrics[1].metric("Waiting", summary["waiting"])
    metrics[2].metric("In progress", summary["in_progress"])
    metrics[3].metric("Resolved", summary["resolved"])

    with st.expander("Register emergency call", expanded=True):
        with st.form("call_form", clear_on_submit=True):
            first, second = st.columns(2)
            caller_name = first.text_input("Caller name")
            phone = second.text_input("Phone")
            location = first.text_input("Location")
            emergency_type = second.selectbox(
                "Emergency type",
                ["Medical", "Fire", "Police", "Rescue", "Road accident", "Other"],
            )
            description = st.text_area("Description")
            priority = st.slider("Priority", min_value=1, max_value=5, value=3)
            submitted = st.form_submit_button("Register call", type="primary")

        if submitted:
            payload = {
                "caller_name": caller_name,
                "phone": phone,
                "location": location,
                "emergency_type": emergency_type,
                "description": description,
                "priority": priority,
            }
            try:
                api_request("POST", "/api/calls", json=payload)
                st.success("Emergency call registered.")
                st.rerun()
            except requests.HTTPError as error:
                st.error(f"Could not register call: {error}")

    st.subheader("Priority queue")
    calls = api_request("GET", "/api/calls")
    if not calls:
        st.info("No emergency calls have been registered.")
    else:
        for call in calls:
            with st.container(border=True):
                columns = st.columns([1, 2, 2, 2, 2, 2])
                columns[0].write(f"**#{call['call_id']}**\nPriority: {call['priority']}")
                columns[1].write(f"**{call['caller_name']}**\n{call['phone']}")
                columns[2].write(f"**{call['emergency_type']}**\n{call['description']}")
                columns[3].write(f"**Location**\n{call['location']}")
                new_status = columns[4].selectbox(
                    "Status",
                    ["WAITING", "IN_PROGRESS", "RESOLVED", "CANCELLED"],
                    index=["WAITING", "IN_PROGRESS", "RESOLVED", "CANCELLED"].index(call["status"]),
                    key=f"status-{call['call_id']}",
                )
                if columns[5].button("Update", key=f"update-{call['call_id']}"):
                    api_request(
                        "PATCH",
                        f"/api/calls/{call['call_id']}/status",
                        params={"status": new_status},
                    )
                    st.success("Status updated.")
                    st.rerun()
except requests.RequestException:
    st.error(
        "The FastAPI backend is not running. Start it on "
        f"{API_URL} and refresh this page."
    )

st.caption(f"Backend: {API_URL}")
