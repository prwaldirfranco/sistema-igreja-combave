import streamlit as st
import json
import os
from datetime import datetime
from PIL import Image
import uuid

CAMINHO_DADOS = "data/membros.json"
CAMINHO_FOTOS = "data/fotos_membros"

os.makedirs(CAMINHO_FOTOS, exist_ok=True)

def carregar_membros():
    if os.path.exists(CAMINHO_DADOS):
        try:
            with open(CAMINHO_DADOS, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def salvar_membros(membros):
    with open(CAMINHO_DADOS, "w", encoding="utf-8") as f:
        json.dump(membros, f, indent=4, ensure_ascii=False)

def exibir():
    st.title("👥 Cadastro de Membros")

    aba = st.radio("Escolha uma opção:", ["➕ Cadastrar Membro", "📋 Lista de Membros"])

    if aba == "➕ Cadastrar Membro":
        with st.form("form_membro", clear_on_submit=True):
            st.subheader("📄 Dados Pessoais")

            foto = st.file_uploader("Foto do Membro", type=["jpg", "jpeg", "png"])
            nome = st.text_input("Nome Completo")
            cpf = st.text_input("CPF")
            rg = st.text_input("RG")
            nascimento = st.date_input("Data de Nascimento")
            funcao = st.selectbox("Função na Igreja", ["Membro", "Pastor", "Diácono", "Evangelista", "Visitante", "Outro"])
            status = st.selectbox("Status", ["Ativo", "Inativo", "Afastado"])

            st.markdown("---")
            st.subheader("📞 Contato")
            telefone = st.text_input("Telefone / WhatsApp")
            email = st.text_input("Email")

            st.markdown("---")
            st.subheader("🏠 Endereço")
            cep = st.text_input("CEP")
            rua = st.text_input("Rua")
            numero = st.text_input("Número")
            bairro = st.text_input("Bairro")
            cidade = st.text_input("Cidade")
            estado = st.text_input("Estado")

            st.markdown("---")
            st.subheader("📝 Observações")
            observacoes = st.text_area("Anotações adicionais")

            enviado = st.form_submit_button("💾 Salvar Membro")

            if enviado:
                membros = carregar_membros()
                id_membro = str(uuid.uuid4())

                caminho_foto_salva = ""
                if foto:
                    extensao = foto.name.split('.')[-1]
                    nome_arquivo = f"{id_membro}.{extensao}"
                    caminho_foto_salva = os.path.join(CAMINHO_FOTOS, nome_arquivo)
                    with open(caminho_foto_salva, "wb") as f:
                        f.write(foto.read())

                novo_membro = {
                    "id": id_membro,
                    "nome": nome,
                    "cpf": cpf,
                    "rg": rg,
                    "nascimento": str(nascimento),
                    "funcao": funcao,
                    "status": status,
                    "telefone": telefone,
                    "email": email,
                    "cep": cep,
                    "rua": rua,
                    "numero": numero,
                    "bairro": bairro,
                    "cidade": cidade,
                    "estado": estado,
                    "observacoes": observacoes,
                    "foto": caminho_foto_salva,
                    "cadastrado_em": str(datetime.now())
                }

                membros.append(novo_membro)
                salvar_membros(membros)
                st.success("✅ Membro cadastrado com sucesso!")

    elif aba == "📋 Lista de Membros":
        membros = carregar_membros()

        if not membros:
            st.info("Nenhum membro cadastrado ainda.")
            return

        for membro in membros:
            with st.expander(f"{membro['nome']} ({membro['funcao']})"):
                cols = st.columns([1, 2])
                if membro.get("foto") and os.path.exists(membro["foto"]):
                    cols[0].image(membro["foto"], width=150)
                else:
                    cols[0].markdown("🖼️ Sem foto")

                with cols[1]:
                    st.markdown(f"**CPF:** {membro.get('cpf', '')}")
                    st.markdown(f"**Nascimento:** {membro.get('nascimento', '')}")
                    st.markdown(f"**Telefone:** {membro.get('telefone', '')}")
                    st.markdown(f"**Email:** {membro.get('email', '')}")
                    st.markdown(f"**Função:** {membro.get('funcao', '')}")
                    st.markdown(f"**Status:** {membro.get('status', '')}")
                    st.markdown(f"**Endereço:** {membro.get('rua', '')}, {membro.get('numero', '')} - {membro.get('bairro', '')}, {membro.get('cidade', '')} - {membro.get('estado', '')} | CEP: {membro.get('cep', '')}")
                    st.markdown(f"**Observações:** {membro.get('observacoes', '')}")
                    st.markdown(f"**Cadastrado em:** {membro.get('cadastrado_em', '')}")

                col1, col2 = st.columns([1, 1])
                if col1.button("🗑️ Excluir", key=f"excluir_{membro['id']}"):
                    membros = [m for m in membros if m["id"] != membro["id"]]
                    salvar_membros(membros)
                    if membro.get("foto") and os.path.exists(membro["foto"]):
                        os.remove(membro["foto"])
                    st.success("Membro excluído com sucesso.")
                    st.rerun()

