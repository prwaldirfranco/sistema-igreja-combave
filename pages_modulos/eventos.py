import streamlit as st
import os
import json
import uuid
from datetime import datetime

CAMINHO_EVENTOS = "data/eventos.json"

def carregar_eventos():
    if os.path.exists(CAMINHO_EVENTOS):
        with open(CAMINHO_EVENTOS, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def salvar_eventos(eventos):
    with open(CAMINHO_EVENTOS, "w", encoding="utf-8") as f:
        json.dump(eventos, f, indent=4, ensure_ascii=False)

def exibir():
    st.title("📅 Gerenciamento de Eventos")

    eventos = carregar_eventos()

    aba = st.radio("Escolha uma opção:", ["➕ Novo Evento", "📋 Lista de Eventos"])

    if aba == "➕ Novo Evento":
        with st.form("form_evento"):
            titulo = st.text_input("Título do Evento")
            data = st.date_input("Data")
            horario = st.time_input("Horário")
            local = st.text_input("Local")
            responsavel = st.text_input("Responsável")
            descricao = st.text_area("Descrição do Evento")

            enviado = st.form_submit_button("💾 Salvar Evento")

            if enviado:
                novo_evento = {
                    "id": str(uuid.uuid4()),
                    "titulo": titulo,
                    "data": str(data),
                    "horario": str(horario),
                    "local": local,
                    "responsavel": responsavel,
                    "descricao": descricao,
                    "criado_em": str(datetime.now())
                }
                eventos.append(novo_evento)
                salvar_eventos(eventos)
                st.session_state["evento_sucesso"] = True
                st.rerun()

        if st.session_state.get("evento_sucesso"):
            st.success("✅ Evento cadastrado com sucesso!")
            del st.session_state["evento_sucesso"]

    elif aba == "📋 Lista de Eventos":
        if not eventos:
            st.info("Nenhum evento cadastrado ainda.")
            return

        eventos_ordenados = sorted(eventos, key=lambda e: e["data"])
        for evento in eventos_ordenados:
            with st.expander(f"📌 {evento['titulo']} — {evento['data']} às {evento['horario']}"):
                st.markdown(f"**Local:** {evento['local']}")
                st.markdown(f"**Responsável:** {evento['responsavel']}")
                st.markdown(f"**Descrição:** {evento['descricao']}")
                st.markdown(f"_Criado em: {evento.get('criado_em', 'Data não disponível')}_")

                col1, col2 = st.columns([1, 1])
                if col1.button("🗑️ Excluir", key=f"del_{evento['id']}"):
                    eventos = [e for e in eventos if e["id"] != evento["id"]]
                    salvar_eventos(eventos)
                    st.success("Evento excluído com sucesso.")
                    st.rerun()