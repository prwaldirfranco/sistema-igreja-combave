import streamlit as st
import json
import uuid
from datetime import datetime
import os

from pages_modulos.ver_respostas_formularios import carregar_respostas

CAMINHO_FORMULARIOS = "data/formularios.json"
CAMINHO_RESPOSTAS = "data/respostas_formularios.json"

def carregar_formularios():
    if os.path.exists(CAMINHO_FORMULARIOS):
        with open(CAMINHO_FORMULARIOS, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def salvar_formularios(formularios):
    with open(CAMINHO_FORMULARIOS, "w", encoding="utf-8") as f:
        json.dump(formularios, f, indent=4, ensure_ascii=False)

def exibir():
    st.title("📝 Formulários")

    aba = st.radio("Escolha uma opção:", ["➕ Criar Formulário", "📋 Meus Formulários", "📋 Ver Respostas dos Formulários"])

    if aba == "➕ Criar Formulário":
        with st.form("form_criar_formulario"):
            titulo = st.text_input("Título do Formulário")
            descricao = st.text_area("Descrição")
            campos = st.multiselect("Campos do Formulário", ["Nome", "Telefone", "Email", "Observações"], default=["Nome", "Telefone"])
            enviado = st.form_submit_button("💾 Salvar Formulário")

            if enviado:
                if not titulo or not campos:
                    st.warning("Preencha o título e selecione ao menos um campo.")
                else:
                    formularios = carregar_formularios()
                    novo_formulario = {
                        "id": str(uuid.uuid4()),
                        "titulo": titulo,
                        "descricao": descricao,
                        "campos": [c.lower() for c in campos],
                        "criado_em": str(datetime.now()),
                        "ativo": True
                    }
                    formularios.append(novo_formulario)
                    salvar_formularios(formularios)
                    st.success("✅ Formulário criado com sucesso!")

    elif aba == "📋 Ver Respostas dos Formulários":
        st.subheader("📬 Respostas Recebidas")
        formularios = carregar_formularios()
        respostas = carregar_respostas()

        if not formularios:
            st.warning("Nenhum formulário encontrado.")
            return

        if not respostas:
            st.info("Nenhuma resposta registrada ainda.")
            return

        opcoes_formularios = {f["titulo"]: f["id"] for f in formularios}
        titulo_escolhido = st.selectbox("Escolha o formulário:", list(opcoes_formularios.keys()))

        id_escolhido = opcoes_formularios[titulo_escolhido]
        respostas_filtradas = [r for r in respostas if r["id_formulario"] == id_escolhido]

        if not respostas_filtradas:
            st.info("Nenhuma resposta para este formulário ainda.")
            return

        for r in respostas_filtradas:
            with st.expander(f"📅 Enviado em {r['enviado_em']}"):
                for pergunta, resposta in r["respostas"].items():
                    st.markdown(f"**{pergunta.capitalize()}**: {resposta}")

    elif aba == "📋 Meus Formulários":
        formularios = carregar_formularios()

        if not formularios:
            st.info("Nenhum formulário criado ainda.")
            return

        for f in formularios:
            with st.expander(f"{f['titulo']}"):
                st.markdown(f"**Descrição:** {f.get('descricao', '-')}")
                st.markdown(f"**Criado em:** {f.get('criado_em', '-')}")
                campos_formatados = ', '.join([c.title() for c in f.get("campos", [])])
                st.markdown(f"**Campos:** {campos_formatados}")

                col1, col2, col3 = st.columns(3)

                with col1:
                    ver = st.button("📨 Ver Respostas", key=f"respostas_{f['id']}")
                    if ver:
                        st.session_state["ver_respostas_form_id"] = f["id"]
                        st.experimental_rerun()

                with col2:
                    # Corrigido: link público fixo baseado no ID
                    link_publico = f"http://localhost:8501/formulario_publico.py?id={f['id']}"
                    st.code(link_publico, language="text")

                with col3:
                    if st.button("🗑️ Excluir", key=f"del_{f['id']}"):
                        formularios = [x for x in formularios if x["id"] != f["id"]]
                        salvar_formularios(formularios)
                        st.success("Formulário excluído com sucesso.")
                        st.rerun()

        # Se clicou em "Ver Respostas", redireciona automaticamente
        if "ver_respostas_form_id" in st.session_state:
            st.markdown("---")
            st.subheader("📬 Respostas Recebidas")
            id_escolhido = st.session_state["ver_respostas_form_id"]
            respostas = carregar_respostas()
            respostas_filtradas = [r for r in respostas if r["id_formulario"] == id_escolhido]

            if not respostas_filtradas:
                st.info("Nenhuma resposta para este formulário ainda.")
                return

            for r in respostas_filtradas:
                with st.expander(f"📅 Enviado em {r['enviado_em']}"):
                    for pergunta, resposta in r["respostas"].items():
                        st.markdown(f"**{pergunta.capitalize()}**: {resposta}")

if __name__ == "__main__":
    exibir()
