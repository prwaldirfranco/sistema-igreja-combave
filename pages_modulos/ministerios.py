import streamlit as st
import os
import json
import uuid
from datetime import datetime
from PIL import Image

CAMINHO_MINISTERIOS = "data/ministerios.json"
CAMINHO_LOGOS = "data/logos_ministerios"
CAMINHO_MEMBROS = "data/membros.json"

os.makedirs(CAMINHO_LOGOS, exist_ok=True)

def carregar_ministerios():
    if os.path.exists(CAMINHO_MINISTERIOS):
        with open(CAMINHO_MINISTERIOS, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def salvar_ministerios(lista):
    with open(CAMINHO_MINISTERIOS, "w", encoding="utf-8") as f:
        json.dump(lista, f, indent=4, ensure_ascii=False)

def carregar_membros():
    if os.path.exists(CAMINHO_MEMBROS):
        with open(CAMINHO_MEMBROS, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def exibir():
    st.title("💒 Ministérios da Igreja")

    aba = st.radio("Selecione:", ["➕ Novo Ministério", "📋 Lista de Ministérios"])
    ministerios = carregar_ministerios()
    membros = carregar_membros()
    nomes_membros = [m["nome"] for m in membros]

    if aba == "➕ Novo Ministério":
        with st.form("form_ministerio", clear_on_submit=True):
            nome = st.text_input("Nome do Ministério")
            logo = st.file_uploader("Logo do Ministério", type=["jpg", "jpeg", "png"])
            descricao = st.text_area("Descrição")

            responsavel_nome = st.selectbox("Responsável pelo Ministério", nomes_membros)
            membro_resp = next((m for m in membros if m["nome"] == responsavel_nome), None)
            contato_responsavel = membro_resp["telefone"] if membro_resp else ""

            st.markdown(f"📞 **Contato do Líder:** `{contato_responsavel}`")

            membros_participantes = st.multiselect("Membros Participantes", nomes_membros)
            enviado = st.form_submit_button("💾 Salvar Ministério")

            if enviado:
                id_min = str(uuid.uuid4())
                caminho_logo = ""
                if logo:
                    ext = logo.name.split(".")[-1]
                    nome_arquivo = f"{id_min}.{ext}"
                    caminho_logo = os.path.join(CAMINHO_LOGOS, nome_arquivo)
                    with open(caminho_logo, "wb") as f:
                        f.write(logo.read())

                novo = {
                    "id": id_min,
                    "nome": nome,
                    "descricao": descricao,
                    "responsavel": responsavel_nome,
                    "contato_responsavel": contato_responsavel,
                    "membros": membros_participantes,
                    "logo": caminho_logo,
                    "criado_em": str(datetime.now())
                }
                ministerios.append(novo)
                salvar_ministerios(ministerios)
                st.session_state["ministerio_sucesso"] = True
                st.rerun()

        if st.session_state.get("ministerio_sucesso"):
            st.success("✅ Ministério cadastrado com sucesso!")
            del st.session_state["ministerio_sucesso"]

    elif aba == "📋 Lista de Ministérios":
        if not ministerios:
            st.info("Nenhum ministério cadastrado.")
            return

        for m in ministerios:
            with st.expander(f"{m['nome']} — Líder: {m['responsavel']}"):
                col1, col2 = st.columns([1, 2])
                if m["logo"] and os.path.exists(m["logo"]):
                    col1.image(m["logo"], width=150)
                else:
                    col1.markdown("🖼️ Sem logo")

                with col2:
                    st.markdown(f"📄 **Descrição:** {m['descricao']}")
                    st.markdown(f"📞 **Contato do Líder:** {m['contato_responsavel']}")
                    st.markdown("👥 **Membros:**")
                    for nome in m["membros"]:
                        st.markdown(f"- {nome}")
                    st.markdown(f"🗓️ _Criado em: {m.get('criado_em', 'N/D')}_")

                col_a, col_b, col_c = st.columns([1, 1, 2])
                if col_a.button("🗑️ Excluir", key=f"del_{m['id']}"):
                    if m["logo"] and os.path.exists(m["logo"]):
                        os.remove(m["logo"])
                    ministerios = [x for x in ministerios if x["id"] != m["id"]]
                    salvar_ministerios(ministerios)
                    st.success("Ministério excluído.")
                    st.rerun()

                if col_b.button("📝 Editar", key=f"edit_{m['id']}"):
                    st.session_state["editando"] = m["id"]
                    st.rerun()

        # Formulário de edição
        if "editando" in st.session_state:
            edit_id = st.session_state["editando"]
            ministerio = next((x for x in ministerios if x["id"] == edit_id), None)
            if ministerio:
                st.subheader(f"✏️ Editar Ministério: {ministerio['nome']}")
                with st.form("form_editar"):
                    nome = st.text_input("Nome do Ministério", value=ministerio["nome"])
                    logo = st.file_uploader("Atualizar Logo", type=["jpg", "jpeg", "png"])
                    descricao = st.text_area("Descrição", value=ministerio["descricao"])

                    responsavel_nome = st.selectbox("Responsável", nomes_membros, index=nomes_membros.index(ministerio["responsavel"]))
                    membro_resp = next((m for m in membros if m["nome"] == responsavel_nome), None)
                    contato_responsavel = membro_resp["telefone"] if membro_resp else ""
                    st.markdown(f"📞 **Contato do Líder:** `{contato_responsavel}`")

                    membros_participantes = st.multiselect("Membros Participantes", nomes_membros, default=ministerio["membros"])
                    salvar = st.form_submit_button("💾 Salvar Alterações")

                    if salvar:
                        if logo:
                            if ministerio["logo"] and os.path.exists(ministerio["logo"]):
                                os.remove(ministerio["logo"])
                            ext = logo.name.split(".")[-1]
                            nome_arquivo = f"{edit_id}.{ext}"
                            caminho_logo = os.path.join(CAMINHO_LOGOS, nome_arquivo)
                            with open(caminho_logo, "wb") as f:
                                f.write(logo.read())
                            ministerio["logo"] = caminho_logo

                        ministerio["nome"] = nome
                        ministerio["descricao"] = descricao
                        ministerio["responsavel"] = responsavel_nome
                        ministerio["contato_responsavel"] = contato_responsavel
                        ministerio["membros"] = membros_participantes

                        salvar_ministerios(ministerios)
                        del st.session_state["editando"]
                        st.success("Ministério atualizado com sucesso!")
                        st.rerun()