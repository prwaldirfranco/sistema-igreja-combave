import streamlit as st
import os
import json
import uuid
from datetime import datetime
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

CAMINHO_FINANCEIRO = "data/financeiro.json"
CAMINHO_MEMBROS = "data/membros.json"

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

def gerar_pdf_analise(dados):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("💰 Análise Financeira da Igreja", styles["Heading1"]))
    elements.append(Spacer(1, 12))

    total_entradas = sum(d["valor"] for d in dados if d["tipo"] == "Entrada")
    total_saidas = sum(d["valor"] for d in dados if d["tipo"] == "Saída")
    saldo = total_entradas - total_saidas

    elements.append(Paragraph(f"Total de Entradas: R$ {total_entradas:,.2f}", styles["Normal"]))
    elements.append(Paragraph(f"Total de Saídas: R$ {total_saidas:,.2f}", styles["Normal"]))
    elements.append(Paragraph(f"Saldo Atual: R$ {saldo:,.2f}", styles["Normal"]))
    elements.append(Spacer(1, 12))

    dados_tabela = [["Data", "Tipo", "Categoria", "Valor", "Descrição"]]
    for d in sorted(dados, key=lambda x: x["data"], reverse=True):
        dados_tabela.append([
            d.get("data", "-"),
            d.get("tipo", "-"),
            d.get("categoria", "-"),
            f"R$ {d.get('valor', 0):,.2f}",
            d.get("descricao", "-")
        ])

    tabela = Table(dados_tabela, repeatRows=1)
    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('FONTSIZE', (0,0), (-1,-1), 8),
    ]))
    elements.append(tabela)
    doc.build(elements)
    buffer.seek(0)
    return buffer

def exibir():
    st.title("💰 Financeiro da Igreja")

    aba = st.radio("Escolha uma opção:", ["➕ Registrar Movimento", "📋 Histórico"])

    dados = carregar_json(CAMINHO_FINANCEIRO)
    membros = carregar_json(CAMINHO_MEMBROS)
    nomes_membros = [m["nome"] for m in membros]

    if aba == "➕ Registrar Movimento":
        with st.form("form_financeiro", clear_on_submit=True):
            tipo = st.selectbox("Tipo", ["Entrada", "Saída"])
            categoria = st.selectbox("Categoria", ["Dízimo", "Oferta", "Doação", "Despesa", "Outro"])
            mes_referencia = st.selectbox("📅 Mês de Referência", [
                "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
            ])
            valor = st.number_input("Valor (R$)", min_value=0.0, format="%.2f")
            data = st.date_input("Data")
            descricao = st.text_input("Descrição")
            observacoes = st.text_area("Observações")

            dizimista = ""
            if categoria == "Dízimo" and nomes_membros:
                dizimista = st.selectbox("Selecione o membro dizimista", nomes_membros)

            enviado = st.form_submit_button("💾 Salvar Registro")

            if enviado:
                novo = {
                    "id": str(uuid.uuid4()),
                    "tipo": tipo,
                    "categoria": categoria,
                    "valor": valor,
                    "data": str(data),
                    "mes_referencia": mes_referencia,
                    "descricao": descricao,
                    "observacoes": observacoes,
                    "dizimista": dizimista,
                    "registrado_em": str(datetime.now())
                }
                dados.append(novo)
                salvar_json(dados, CAMINHO_FINANCEIRO)
                st.success("✅ Registro salvo com sucesso!")

    elif aba == "📋 Histórico":
        if not dados:
            st.info("Nenhuma movimentação registrada ainda.")
            return

        # Cálculos adicionais
        entradas = [d for d in dados if d["tipo"] == "Entrada"]
        saidas = [d for d in dados if d["tipo"] == "Saída"]

        total_entradas = sum(d["valor"] for d in entradas)
        total_saidas = sum(d["valor"] for d in saidas)
        saldo = total_entradas - total_saidas

        total_dizimos = sum(d["valor"] for d in entradas if d["categoria"] == "Dízimo")
        total_ofertas = sum(d["valor"] for d in entradas if d["categoria"] == "Oferta")
        total_doacoes = sum(d["valor"] for d in entradas if d["categoria"] == "Doação")

        ano_atual = datetime.now().year
        mes_atual = datetime.now().month
        entradas_ano = [d for d in entradas if datetime.fromisoformat(d["data"]).year == ano_atual]
        entradas_mes = [d for d in entradas_ano if datetime.fromisoformat(d["data"]).month == mes_atual]
        total_ano = sum(d["valor"] for d in entradas_ano)
        total_mes = sum(d["valor"] for d in entradas_mes)
        media_mensal = total_ano / mes_atual if mes_atual else 0
        projecao_ano = media_mensal * 12

        # Exibição de Métricas
        st.markdown("## 📊 Visão Geral")
        col1, col2, col3 = st.columns(3)
        col1.metric("💸 Entradas", f"R$ {total_entradas:,.2f}")
        col2.metric("💵 Saídas", f"R$ {total_saidas:,.2f}")
        col3.metric("📊 Saldo Atual", f"R$ {saldo:,.2f}")

        col4, col5, col6 = st.columns(3)
        col4.metric("📅 Entradas no Mês", f"R$ {total_mes:,.2f}")
        col5.metric("📆 Entradas no Ano", f"R$ {total_ano:,.2f}")
        col6.metric("🔮 Projeção Anual", f"R$ {projecao_ano:,.2f}")

        col7, col8, col9 = st.columns(3)
        col7.metric("🙏 Dízimos", f"R$ {total_dizimos:,.2f}")
        col8.metric("❤️ Ofertas", f"R$ {total_ofertas:,.2f}")
        col9.metric("🎁 Doações", f"R$ {total_doacoes:,.2f}")

        # Exportar PDF
        st.markdown("### 📄 Exportar Análise")
        st.download_button(
            "📥 Baixar PDF da Análise Financeira",
            data=gerar_pdf_analise(dados),
            file_name="analise_financeira.pdf",
            mime="application/pdf"
        )

        # Lista de Movimentações
        st.markdown("### 📋 Lista de Movimentações")
        for mov in sorted(dados, key=lambda x: x["data"], reverse=True):
            cor = "🟢" if mov["tipo"] == "Entrada" else "🔴"
            with st.expander(f"{cor} {mov['data']} - {mov['categoria']} ({mov['tipo']}) - R$ {mov['valor']:.2f}"):
                st.markdown(f"**Mês de Referência:** {mov.get('mes_referencia', '-')}")
                st.markdown(f"**Descrição:** {mov['descricao']}")
                if mov.get("dizimista"):
                    st.markdown(f"**Dizimista:** {mov['dizimista']}")
                st.markdown(f"**Observações:** {mov['observacoes']}")
                st.markdown(f"**Registrado em:** {mov['registrado_em']}")

                col1, col2 = st.columns(2)
                if col1.button("🗑️ Excluir", key=f"excluir_{mov['id']}"):
                    dados = [m for m in dados if m["id"] != mov["id"]]
                    salvar_json(dados, CAMINHO_FINANCEIRO)
                    st.success("Movimentação excluída com sucesso.")
                    st.rerun()

                if col2.button("✏️ Editar", key=f"editar_{mov['id']}"):
                    with st.form(f"form_editar_{mov['id']}"):
                        novo_valor = st.number_input("Novo valor", value=mov["valor"], format="%.2f")
                        nova_desc = st.text_input("Nova descrição", value=mov["descricao"])
                        nova_obs = st.text_area("Novas observações", value=mov["observacoes"])
                        confirmado = st.form_submit_button("💾 Salvar Alterações")
                        if confirmado:
                            mov["valor"] = novo_valor
                            mov["descricao"] = nova_desc
                            mov["observacoes"] = nova_obs
                            salvar_json(dados, CAMINHO_FINANCEIRO)
                            st.success("Movimentação atualizada com sucesso!")
                            st.rerun()
