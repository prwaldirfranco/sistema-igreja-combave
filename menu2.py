import streamlit as st
import importlib
import json
import os

CAMINHO_CONFIG = "data/config.json"
CAMINHO_LOGO = "data/logo_igreja.png"

def carregar_config():
    if os.path.exists(CAMINHO_CONFIG):
        with open(CAMINHO_CONFIG, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def mostrar_menu():
    config = carregar_config()
    nome_igreja = config.get("nome_igreja", "Sistema da Igreja")

    st.sidebar.image(CAMINHO_LOGO, width=150) if os.path.exists(CAMINHO_LOGO) else None
    st.sidebar.title(nome_igreja)

    menu = st.sidebar.radio("Navegação", [
        "🏠 Início",
        "👥 Membros",
        "📅 Eventos",
        "💒 Ministérios",
        "💰 Financeiro",
        "📈 Relatórios",
        "📧 Avisos",
        "📚 Escola Bíblica / Discipulado",
        "⚙️ Configurações do Sistema"
    ])

    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Sair"):
        st.session_state.logado = False
        st.rerun()

    if menu == "🏠 Início":
        st.title(f"Bem-vindo à {nome_igreja}!")
        st.write("Escolha uma opção no menu ao lado para começar.")
    elif menu == "👥 Membros":
        pagina = importlib.import_module("pages.membros")
        pagina.exibir()
    elif menu == "📅 Eventos":
        pagina = importlib.import_module("pages.eventos")
        pagina.exibir()
    elif menu == "💒 Ministérios":
        pagina = importlib.import_module("pages.ministerios")
        pagina.exibir()
    elif menu == "💰 Financeiro":
        pagina = importlib.import_module("pages.financeiro")
        pagina.exibir()
    elif menu == "📈 Relatórios":
        pagina = importlib.import_module("pages.relatorios")
        pagina.exibir()
    elif menu == "📧 Avisos":
        pagina = importlib.import_module("pages.avisos")
        pagina.exibir()
    elif menu == "📚 Escola Bíblica / Discipulado":
        pagina = importlib.import_module("pages.discipulado")
        pagina.exibir()
    elif menu == "⚙️ Configurações do Sistema":
        pagina = importlib.import_module("pages.configuracoes")
        pagina.exibir()