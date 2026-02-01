import streamlit as st
import requests

st.set_page_config(page_title="Banking System", layout="wide")

st.sidebar.title("Simple Banking System")

st.sidebar.markdown("""
Navigation
- API documentation
""")

st.sidebar.link_button(
    "Open API Documentation",
    "http://127.0.0.1:8000/docs"
)

st.sidebar.divider()

API = "http://127.0.0.1:8000"

def api_get(path: str):
    req = requests.get(f"{API}{path}")
    return req

def api_post(path: str, json: dict):
    req = requests.post(f"{API}{path}", json=json)
    return req

st.title("Simple Banking System")
st.header("Clients")

response = api_get("/clients")
if response.status_code == 200:
    clients = response.json()
    st.dataframe(clients, use_container_width=True)
else:
    st.error(f"API Error: {response.status_code} - {response.text}")

st.subheader("Add client")

with st.form("create_client_form"):
    name = st.text_input("Name")
    surname = st.text_input("Surname")
    balance = st.number_input("Initial balance", min_value=0, step=1)
    submitted = st.form_submit_button("Add")

if submitted:
    payload = {"name": name, "surname": surname, "balance": int(balance)}
    resp = api_post("/clients", payload)

    if resp.status_code == 200:
        st.success("Client has been added")
        st.rerun()
    else:
        st.error(f"Error: {resp.status_code} - {resp.text}")

st.header("Operacje")

resp = api_get("/clients")
clients = resp.json() if resp.status_code == 200 else []

if not clients:
    st.info("In order to preform an operation you need to add a client")
else:
    options = {f'{c["client_id"]} - {c["name"]} {c["surname"]}': c["client_id"] for c in clients}
    choice_label = st.selectbox("Chose client", list(options.keys()))
    client_id = options[choice_label]

    amount = st.number_input("Amount", min_value=1, step=1)
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Deposit"):
            resp = api_post(f"/clients/{client_id}/deposit", {"amount": int(amount)})
            if resp.status_code == 200:
                st.success(f"Done. New balance: {resp.json()['balance']}")
                st.rerun()
            else:
                st.error(f"Error: {resp.status_code} - {resp.text}")

    with col2:
        if st.button("Withdraw"):
            resp = api_post(f"/clients/{client_id}/withdraw", {"amount": int(amount)})
            if resp.status_code == 200:
                st.success(f"Done. New balance: {resp.json()['balance']}")
                st.rerun()
            else:
                st.error(f"Error: {resp.status_code} - {resp.text}")

st.header("Transaction history")

if clients:
    reponse = api_get(f"/clients/{client_id}/statement")
    if response.status_code == 200:
        i = resp.json()
        st.dataframe(i, use_container_width=True)
    else:
        st.error(f"Error: {response.status_code} - {response.text}")
