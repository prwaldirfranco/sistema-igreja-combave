import streamlit as st
import importlib
import json
from datetime import datetime

def carregar_config():
    try:
        with open("data/config.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"nome_igreja": "Nome da Igreja", "logo": "data/logo_igreja.png"}

def carregar_membros():
    try:
        with open("data/membros.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def mostrar_menu():
    config = carregar_config()
    nome_igreja = config.get("nome_igreja", "Nome da Igreja")
    logo_path = config.get("logo", "data/logo_igreja.png")

    # Header com logo e nome
    with st.sidebar:
        if logo_path:
            st.image(logo_path, use_container_width=True)
        st.markdown(f"## {nome_igreja}")
        st.markdown("---")

    # Menu lateral
    menu = st.sidebar.radio("Menu", [
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

    # INÍCIO DO SISTEMA
    if menu == "🏠 Início":
        st.title("📊 Painel Inicial")

        membros = carregar_membros()
        hoje = datetime.now().strftime("%m-%d")
        aniversariantes = [m for m in membros if "nascimento" in m and hoje == "-".join(m["nascimento"].split("-")[1:3])]

        st.subheader("🎂 Aniversariantes de hoje")
        if aniversariantes:
            for m in aniversariantes:
                st.markdown(f"- {m['nome']} ({m['nascimento']})")
        else:
            st.info("Nenhum aniversariante hoje.")

        st.subheader("⛪ Cultos do Dia")
        st.markdown("- 19:30 - Culto de Ensino")
        st.markdown("- 20:00 - Culto Jovem")  # exemplo fixo

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