import streamlit as st
from login import login
from menu import mostrar_menu

st.set_page_config(page_title="Sistema Igreja", layout="wide")

# Sessão de autenticação
if 'logado' not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:
    login()
else:
    mostrar_menu()
