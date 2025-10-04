import streamlit as st
import os
import json
import uuid
from datetime import datetime

CAMINHO_AVISOS = "data/avisos.json"
CAMINHO_MINISTERIOS = "data/ministerios.json"
CAMINHO_MEMBROS = "data/membros.json"

def carregar_avisos():
    if os.path.exists(CAMINHO_AVISOS):
        with open(CAMINHO_AVISOS, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def salvar_avisos(lista):
    with open(CAMINHO_AVISOS, "w", encoding="utf-8") as f:
        json.dump(lista, f, indent=4, ensure_ascii=False)

def carregar_membros():
    if os.path.exists(CAMINHO_MEMBROS):
        with open(CAMINHO_MEMBROS, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def carregar_ministerios():
    if os.path.exists(CAMINHO_MINISTERIOS):
        with open(CAMINHO_MINISTERIOS, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def exibir():
    st.title("📧 Comunicação / Avisos")

    aba = st.radio("Escolha uma opção:", ["➕ Novo Aviso", "📋 Avisos Enviados"])
    avisos = carregar_avisos()
    ministerios = carregar_ministerios()
    membros = carregar_membros()

    nomes_ministerios = [m["nome"] for m in ministerios]
    nomes_membros = [m["nome"] for m in membros]

    if aba == "➕ Novo Aviso":
        with st.form("form_aviso", clear_on_submit=True):
            titulo = st.text_input("Título do Aviso")
            mensagem = st.text_area("Mensagem")
            autor = st.text_input("Autor do Aviso")

            destinatario_tipo = st.radio("Destinatários", ["Todos os Membros", "Ministério Específico", "Selecionar Membros"])

            destinatarios = []
            if destinatario_tipo == "Ministério Específico":
                ministerio = st.selectbox("Escolha o Ministério", nomes_ministerios)
                destinatarios = [ministerio]
            elif destinatario_tipo == "Selecionar Membros":
                destinatarios = st.multiselect("Escolha os Membros", nomes_membros)
            else:
                destinatarios = ["Todos"]

            enviado = st.form_submit_button("📨 Enviar Aviso")

            if enviado:
                aviso = {
                    "id": str(uuid.uuid4()),
                    "titulo": titulo,
                    "mensagem": mensagem,
                    "autor": autor,
                    "destinatarios": destinatarios,
                    "tipo_destinatario": destinatario_tipo,
                    "data_envio": str(datetime.now())
                }
                avisos.append(aviso)
                salvar_avisos(avisos)
                st.success("✅ Aviso enviado com sucesso!")
                st.rerun()

    elif aba == "📋 Avisos Enviados":
        if not avisos:
            st.info("Nenhum aviso enviado ainda.")
            return

        for aviso in reversed(avisos):
            with st.expander(f"{aviso['titulo']} — por {aviso['autor']}"):
                st.markdown(f"**🕒 Enviado em:** {aviso['data_envio']}")
                st.markdown(f"**📨 Destinatários ({aviso['tipo_destinatario']}):**")
                for d in aviso['destinatarios']:
                    st.markdown(f"- {d}")
                st.markdown("---")
                st.markdown(f"**📝 Mensagem:**\\n{aviso['mensagem']}")

                col1, col2 = st.columns([1, 1])
                if col1.button("🗑️ Excluir", key=f"del_{aviso['id']}"):
                    avisos = [a for a in avisos if a["id"] != aviso["id"]]
                    salvar_avisos(avisos)
                    st.success("Aviso excluído.")
                    st.rerun()