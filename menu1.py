import streamlit as st
import importlib

def mostrar_menu():
    st.sidebar.title("📋 Menu")
    
    menu = st.sidebar.radio(
        "Navegação",
        ["🏠 Início", "👥 Membros", "📅 Eventos", "💒 Ministérios", "💰 Financeiro", "📈 Relatórios", "📚 Escola Bíblica", "📧 Comunicação / Avisos", "⚙️ Configurações do Sistema"]
    )

    st.sidebar.markdown("---")
    if st.sidebar.button("Sair"):
        st.session_state.logado = False
        st.rerun()

    if menu == "🏠 Início":
        st.title("Painel Inicial")
        st.write("Bem-vindo ao Sistema da Igreja!")

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

    elif menu == "📚 Escola Bíblica":
        pagina = importlib.import_module("pages.escola_biblica")
        pagina.exibir()

    elif menu == "📧 Comunicação / Avisos":
        pagina = importlib.import_module("pages.avisos")
        pagina.exibir()

    elif menu == "⚙️ Configurações do Sistema":
        pagina = importlib.import_module("pages.configuracoes")
        pagina.exibir()
