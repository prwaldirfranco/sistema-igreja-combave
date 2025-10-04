import streamlit as st
import importlib

def mostrar_menu():
    st.sidebar.title("📋 Menu")
    menu = st.sidebar.radio("Navegação", [
        "🏠 Início",
        "👥 Membros",
        "📅 Eventos",
        "💒 Ministérios",
        "💰 Financeiro",
        "📈 Relatórios",
        "📚 Escola Bíblica",
        "📧 Avisos",
        "🧑‍🏫 Discipulado",
        "⚙️ Configurações"
    ])

    st.sidebar.markdown("---")
    if st.sidebar.button("Sair"):
        st.session_state.logado = False
        st.rerun()

    if menu == "🏠 Início":
        st.title("Painel Inicial")
        st.write("Bem-vindo ao Sistema da Igreja!")
    elif menu == "👥 Membros":
        pagina = importlib.import_module("pages_modulos.membros")
        pagina.exibir()
    elif menu == "📅 Eventos":
        pagina = importlib.import_module("pages_modulos.eventos")
        pagina.exibir()
    elif menu == "💒 Ministérios":
        pagina = importlib.import_module("pages_modulos.ministerios")
        pagina.exibir()
    elif menu == "💰 Financeiro":
        pagina = importlib.import_module("pages_modulos.financeiro")
        pagina.exibir()
    elif menu == "📈 Relatórios":
        pagina = importlib.import_module("pages_modulos.relatorios")
        pagina.exibir()
    elif menu == "📚 Escola Bíblica":
        pagina = importlib.import_module("pages_modulos.escola_biblica")
        pagina.exibir()
    elif menu == "📧 Avisos":
        pagina = importlib.import_module("pages_modulos.avisos")
        pagina.exibir()
    elif menu == "🧑‍🏫 Discipulado":
        pagina = importlib.import_module("pages_modulos.discipulado")
        pagina.exibir()
    elif menu == "⚙️ Configurações":
        pagina = importlib.import_module("pages_modulos.configuracoes")
        pagina.exibir()