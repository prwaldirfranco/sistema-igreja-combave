import streamlit as st
import json
import os
import uuid
from datetime import datetime

# Caminhos
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
    # Carrega respostas existentes
    dados = []
    if os.path.exists(CAMINHO_RESPOSTAS):
        with open(CAMINHO_RESPOSTAS, "r", encoding="utf-8") as f:
            try:
                dados = json.load(f)
            except json.JSONDecodeError:
                dados = []
    # Adiciona nova resposta
    dados.append(resposta)
    with open(CAMINHO_RESPOSTAS, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def exibir():
    st.title("📝 Formulário Público")

    # Captura o parâmetro `id` da URL
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
        # Gera campos dinamicamente
        for campo in formulario.get("campos", []):
            tipo = campo.get("tipo")
            pergunta = campo.get("pergunta")
            if tipo == "texto":
                respostas[pergunta] = st.text_input(pergunta)
            elif tipo == "texto_longo":
                respostas[pergunta] = st.text_area(pergunta)
            elif tipo == "numero":
                respostas[pergunta] = st.number_input(pergunta)
            elif tipo == "opcoes":
                opcs = campo.get("opcoes", [])
                respostas[pergunta] = st.selectbox(pergunta, opcs)
            else:
                # tipo desconhecido, tratar como texto simples
                respostas[pergunta] = st.text_input(pergunta)

        enviado = st.form_submit_button("Enviar")

        if enviado:
            resposta_salvar = {
                "id_resposta": str(uuid.uuid4()),
                "id_formulario": form_id,
                "respostas": respostas,
                "enviado_em": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            }
            salvar_resposta(resposta_salvar)
            st.success("Obrigado! Sua resposta foi registrada.")

if __name__ == "__main__":
    exibir()
