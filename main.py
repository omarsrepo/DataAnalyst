import pandas as pd
import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
import json
import time

# Initialize session state variables
st.session_state.setdefault("button_clicked", False)
st.session_state.setdefault("input_text", "")
st.session_state.setdefault("latest_row", None)

# Sidebar for file upload
st.sidebar.title("Upload Dataset")
uploaded_file = st.sidebar.file_uploader("Choose a file", type=['xlsx', 'xls', 'csv'])

if uploaded_file is not None:
    if uploaded_file.type != 'text/csv':
        data = pd.read_excel(uploaded_file)
    else:
        data = pd.read_csv(uploaded_file)
    st.write(data)


def add_row(table_id, input_text):
    url = "https://app.jamaibase.com/api/v1/gen_tables/action/rows/add"
    payload = {
        "data": {"data": input_text},
        "stream": True,
        "table_id": table_id,
    }
    headers = {"accept": "application/json", "content-type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)


def get_row(table_id):
    url = f"https://app.jamaibase.com/api/v1/gen_tables/action/{table_id}/rows?limit=100"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    return response


def get_latest_row(table_id):
    response = get_row(table_id)
    json_object = json.loads(response.text)
    last_row = json_object["items"][0]
    return last_row


button_clicked = st.button("Run analysis")
if button_clicked:
    add_row('DataAnalyst', st.session_state["input_text"])
    st.session_state["latest_row"] = get_latest_row('DataAnalyst')
    # Remaining code to process data goes here


def stream_data(input_text):
    for word in input_text.split(" "):
        yield "**" + word + "** "
        time.sleep(0.1)


def stream_text_sections(button_clicked, stream_text, placeholder_key):
    text_area_placeholder = st.empty()
    if not button_clicked:
        st.session_state[placeholder_key] = text_area_placeholder.text_area(
            placeholder_key,
            value="",
            height=100,
        )
    else:
        if st.session_state[placeholder_key] != "":
            st.session_state[placeholder_key] = text_area_placeholder.text_area(
                placeholder_key,
                value=st.session_state[
                    placeholder_key
                ],
                height=100,
            )
            return
        response = stream_data(stream_text)
        full_response = ""
        for res in response:
            full_response += res
            text_area_placeholder.markdown(full_response, unsafe_allow_html=True)
        st.session_state[placeholder_key] = text_area_placeholder.text_area(
            placeholder_key,
            value=full_response.replace("**", ""),
            height=100,
        )


# Add the functions at appropriate sections to display the outputs:
stream_text_sections(st.session_state["button_clicked"], result, key)


keys = ["Result_A1", "Result_A2", "Result_A3"]
results = [rA1, rA2, rA3]
for key, result in zip(keys, results):
    stream_text_sections(st.session_state["button_clicked"], result, key)


options = keys + ["None"]
selected_option = st.radio(
    "Choose the appropriate description:", options, index=0
)
if selected_option == "None":
    user_text = st.text_area(
        "User input", placeholder="Please provide your input."
    )
    st.session_state["result_A"] = user_text
elif selected_option in ["Result_A1", "Result_A2", "Result_A3"]:
    st.session_state["result_A"] = selected_option
    st.write(st.session_state.result_A)


if st.session_state["button_clicked"]:
    st.download_button(
        label="Download File",
        data=gen_doc(
            text_1=text_1,
            text_2=text_2,
            html_table_1=html_table_1,
        ),
        file_name="report.docx",
        mime="text/plain",
    )
