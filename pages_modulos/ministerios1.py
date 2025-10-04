import streamlit as st
import os
import json
import uuid
from datetime import datetime

CAMINHO_MINISTERIOS = "data/ministerios.json"
CAMINHO_MEMBROS = "data/membros.json"

# Utilitários
def carregar_json(caminho):
    if os.path.exists(caminho):
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def salvar_json(dados, caminho):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

# Interface principal
def exibir():
    st.title("💒 Ministérios da Igreja")

    aba = st.radio("Escolha uma opção:", ["➕ Cadastrar Ministério", "📋 Lista de Ministérios"])

    membros = carregar_json(CAMINHO_MEMBROS)
    ministerios = carregar_json(CAMINHO_MINISTERIOS)

    if aba == "➕ Cadastrar Ministério":
        with st.form("form_ministerio", clear_on_submit=True):
            nome = st.text_input("Nome do Ministério")
            responsavel = st.text_input("Responsável")
            descricao = st.text_area("Descrição do Ministério")
            st.markdown("**👥 Membros Participantes:**")
            nomes_membros = [m['nome'] for m in membros]
            membros_escolhidos = st.multiselect("Selecione os membros", nomes_membros)

            enviado = st.form_submit_button("💾 Salvar Ministério")

            if enviado:
                novo = {
                    "id": str(uuid.uuid4()),
                    "nome": nome,
                    "responsavel": responsavel,
                    "descricao": descricao,
                    "membros": membros_escolhidos,
                    "cadastrado_em": str(datetime.now())
                }
                ministerios.append(novo)
                salvar_json(ministerios, CAMINHO_MINISTERIOS)
                st.success("✅ Ministério cadastrado com sucesso!")

    elif aba == "📋 Lista de Ministérios":
        if not ministerios:
            st.info("Nenhum ministério cadastrado.")
            return

        for ministerio in ministerios:
            with st.expander(f"{ministerio['nome']} - Resp: {ministerio['responsavel']}"):
                st.markdown(f"**Descrição:** {ministerio['descricao']}")
                st.markdown(f"**Membros:** {', '.join(ministerio['membros']) if ministerio['membros'] else 'Nenhum'}")
                st.markdown(f"**Cadastrado em:** {ministerio['cadastrado_em']}")

                if st.button("🗑️ Excluir Ministério", key=f"excluir_{ministerio['id']}"):
                    ministerios = [m for m in ministerios if m['id'] != ministerio['id']]
                    salvar_json(ministerios, CAMINHO_MINISTERIOS)
                    st.success("Ministério excluído com sucesso.")
                    st.rerun()
