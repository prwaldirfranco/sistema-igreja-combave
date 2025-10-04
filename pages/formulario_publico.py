import streamlit as st
import json
import os
import uuid
from datetime import datetime

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

def salvar_resposta(resposta):
    dados = []
    if os.path.exists(CAMINHO_RESPOSTAS):
        with open(CAMINHO_RESPOSTAS, "r", encoding="utf-8") as f:
            try:
                dados = json.load(f)
            except json.JSONDecodeError:
                dados = []
    dados.append(resposta)
    with open(CAMINHO_RESPOSTAS, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def exibir():
    st.title("📝 Formulário Público")

    params = st.experimental_get_query_params()
    form_id = params.get("id", [None])[0]

    if not form_id:
        st.error("ID do formulário não foi fornecido na URL.")
        return

    formularios = carregar_formularios()
    formulario = next((f for f in formularios if f.get("id") == form_id), None)

    if not formulario:
        st.error("Formulário não encontrado.")
        return

    st.header(formulario.get("titulo", "Formulário"))
    st.markdown(formulario.get("descricao", ""))

    respostas = {}
    with st.form("responder_formulario"):
        for campo in formulario.get("campos", []):
            if isinstance(campo, str):
                # Compatibilidade com campos antigos (formato string)
                respostas[campo] = st.text_input(campo)
            elif isinstance(campo, dict):
                tipo = campo.get("tipo", "texto")
                pergunta = campo.get("pergunta", "Pergunta sem texto")

                if tipo == "texto":
                    respostas[pergunta] = st.text_input(pergunta)
                elif tipo == "texto_longo":
                    respostas[pergunta] = st.text_area(pergunta)
                elif tipo == "numero":
                    respostas[pergunta] = st.number_input(pergunta, step=1)
                elif tipo == "opcoes":
                    opcs = campo.get("opcoes", [])
                    respostas[pergunta] = st.selectbox(pergunta, opcs)
                else:
                    respostas[pergunta] = st.text_input(pergunta)
            else:
                st.warning("Campo com formato inválido.")

        enviado = st.form_submit_button("Enviar")

        if enviado:
            resposta_salvar = {
                "id_resposta": str(uuid.uuid4()),
                "id_formulario": form_id,
                "respostas": respostas,
                "enviado_em": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            }
            salvar_resposta(resposta_salvar)
            st.success("✅ Obrigado! Sua resposta foi registrada.")

if __name__ == "__main__":
    exibir()
