
import streamlit as st
import importlib
from utils.configuracoes import carregar_config

def mostrar_menu():
    config = carregar_config()

    with st.sidebar:
        if config.get("logo") and config["logo"] != "":
            st.image(config["logo"], use_container_width=True)
        st.markdown(f"### {config.get('nome_igreja', 'Nome da Igreja')}")

    menu = st.sidebar.radio("Menu", [
        "🏠 Início",
        "👥 Membros",
        "📅 Eventos",
        "💒 Ministérios",
        "💰 Financeiro",
        "📈 Relatórios",
        "📝 Formulários",
        "⚙️ Configurações"
    ])

    st.sidebar.markdown("---")
    if st.sidebar.button("Sair"):
        st.session_state.logado = False
        st.rerun()

    if menu == "🏠 Início":
        pagina = importlib.import_module("pages.inicio")
    elif menu == "👥 Membros":
        pagina = importlib.import_module("pages.membros")
    elif menu == "📅 Eventos":
        pagina = importlib.import_module("pages.eventos")
    elif menu == "💒 Ministérios":
        pagina = importlib.import_module("pages.ministerios")
    elif menu == "💰 Financeiro":
        pagina = importlib.import_module("pages.financeiro")
    elif menu == "📈 Relatórios":
        pagina = importlib.import_module("pages.relatorios")
    elif menu == "📝 Formulários":
        pagina = importlib.import_module("pages_modulos.formularios")
    elif menu == "⚙️ Configurações":
        pagina = importlib.import_module("pages.configuracoes")
    else:
        st.warning("Página não encontrada.")
        return

    pagina.exibir()
