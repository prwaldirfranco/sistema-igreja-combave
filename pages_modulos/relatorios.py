import streamlit as st
import os
import json
import pandas as pd
from io import BytesIO
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase import pdfmetrics

pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))

# Constantes
CAMINHO_MEMBROS = "data/membros.json"
CAMINHO_FINANCEIRO = "data/financeiro.json"
CAMINHO_LOGO = "data/logo.png"
NOME_IGREJA = "Comunidade Batista Vida Efatá"

def carregar_json(caminho):
    if os.path.exists(caminho):
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def exibir():
    st.title("📈 Relatórios da Igreja")
    opcao = st.selectbox("Escolha o módulo do relatório:", ["👥 Membros", "💰 Financeiro"])

    if opcao == "👥 Membros":
        exibir_membros()
    elif opcao == "💰 Financeiro":
        exibir_financeiro()

def exibir_membros():
    membros = carregar_json(CAMINHO_MEMBROS)
    membros_validos = [m for m in membros if "nome" in m and "funcao" in m and "status" in m]

    st.header("👥 Relatório de Membros")
    if membros_validos:
        df_membros = pd.DataFrame(membros_validos)[["nome", "funcao", "status"]]
        df_membros.columns = ["Nome", "Função", "Status"]
        st.dataframe(df_membros, use_container_width=True)

        buffer_excel = BytesIO()
        with pd.ExcelWriter(buffer_excel, engine="openpyxl") as writer:
            df_membros.to_excel(writer, sheet_name="Membros", index=False)
        buffer_excel.seek(0)
        st.download_button("📥 Baixar Excel - Membros", data=buffer_excel, file_name="relatorio_membros.xlsx")

        st.download_button("📄 Baixar PDF - Membros", data=gerar_pdf_membros(membros_validos), file_name="relatorio_membros.pdf", mime="application/pdf")
    else:
        st.info("Nenhum membro cadastrado.")

def exibir_financeiro():
    financeiro = carregar_json(CAMINHO_FINANCEIRO)
    if not financeiro:
        st.info("Nenhum lançamento encontrado.")
        return

    tipos_disponiveis = sorted(set(f.get("categoria", "Outro") for f in financeiro))
    meses_disponiveis = sorted(set(f.get("mes_referencia", "") for f in financeiro if f.get("mes_referencia")))

    st.header("💰 Relatório Financeiro")

    col1, col2 = st.columns(2)
    tipo_filtro = col1.selectbox("Filtrar por categoria:", ["Todos"] + tipos_disponiveis)
    mes_filtro = col2.selectbox("Filtrar por mês de referência:", ["Todos"] + meses_disponiveis)

    # Aplicar filtros
    df_fin = pd.DataFrame(financeiro)
    if tipo_filtro != "Todos":
        df_fin = df_fin[df_fin["categoria"] == tipo_filtro]
    if mes_filtro != "Todos":
        df_fin = df_fin[df_fin["mes_referencia"] == mes_filtro]

    colunas = ["data", "tipo", "categoria", "valor", "descricao", "mes_referencia"]
    if "dizimista" in df_fin.columns:
        colunas.append("dizimista")
    df_fin = df_fin[colunas]
    df_fin.columns = [c.capitalize().replace("_", " ") for c in df_fin.columns]

    st.dataframe(df_fin, use_container_width=True)

    # Exportações
    buffer_excel_fin = BytesIO()
    with pd.ExcelWriter(buffer_excel_fin, engine="openpyxl") as writer:
        df_fin.to_excel(writer, sheet_name="Financeiro", index=False)
    buffer_excel_fin.seek(0)
    st.download_button("📥 Baixar Excel - Financeiro", data=buffer_excel_fin, file_name="relatorio_financeiro.xlsx")

    st.download_button("📄 Baixar PDF - Financeiro", data=gerar_pdf_financeiro(df_fin), file_name="relatorio_financeiro.pdf", mime="application/pdf")

# --- Geração de PDFs ---
def gerar_pdf_membros(membros):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    if os.path.exists(CAMINHO_LOGO):
        elements.append(RLImage(CAMINHO_LOGO, width=100, height=100))
    elements.append(Paragraph(f"<b>{NOME_IGREJA}</b>", styles['Heading1']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("📋 Relatório de Membros", styles['Heading2']))
    elements.append(Spacer(1, 6))

    dados = [["Nome", "Função", "Status"]] + [[m["nome"], m.get("funcao", ""), m.get("status", "")] for m in membros]
    tabela = Table(dados, repeatRows=1)
    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTNAME', (0, 0), (-1, -1), 'HeiseiMin-W3'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
    ]))
    elements.append(tabela)
    doc.build(elements)
    buffer.seek(0)
    return buffer

def gerar_pdf_financeiro(df_fin):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    if os.path.exists(CAMINHO_LOGO):
        elements.append(RLImage(CAMINHO_LOGO, width=100, height=100))
    elements.append(Paragraph(f"<b>{NOME_IGREJA}</b>", styles['Heading1']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("💰 Relatório Financeiro", styles['Heading2']))
    elements.append(Spacer(1, 6))

    dados = [df_fin.columns.tolist()] + df_fin.values.tolist()
    tabela = Table(dados, repeatRows=1)
    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTNAME', (0, 0), (-1, -1), 'HeiseiMin-W3'),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
    ]))
    elements.append(tabela)
    doc.build(elements)
    buffer.seek(0)
    return buffer