import streamlit as st
from utils.auth import verificar_credenciais

def login():
    st.title("Login - Sistema Igreja")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        usuario_autenticado = verificar_credenciais(usuario, senha)
        if usuario_autenticado:
            st.session_state.logado = True
            st.session_state.usuario = usuario_autenticado  # Armazena o dicionário completo do usuário
            st.success("Login realizado com sucesso!")
            st.rerun()  # CORRIGIDO: antes era experimental_rerun()
        else:
            st.error("Usuário ou senha inválidos.")
