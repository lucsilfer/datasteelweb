import streamlit as st
import pandas as pd
import fitz  # PyMuPDF para leitura de PDFs
import DS_Calculos as ds  # Certifique-se de que esse módulo está disponível
import os  # Para manipular arquivos temporários

st.set_page_config(page_title="Análise de Certificados Usiminas", layout="wide")

st.title("🔬 Análise de Certificados de Aço Carbono NRU - NTU - Usiminas")

# Upload do arquivo PDF
uploaded_file = st.file_uploader("📄 Envie o Certificado PDF", type=["pdf"])

# Campo de texto para a linha do certificado
linha = st.text_input("🔍 Linha do Certificado a Analisar")

# **Botão para Analisar**
if st.button("📊 Analisar Certificado") and uploaded_file and linha:
    if not linha.strip().isdigit():
        st.error("❌ Por favor, insira um número válido para a linha do certificado.")
    else:
        try:
            # Criar um arquivo temporário para armazenar o PDF
            temp_file_path = f"temp_{uploaded_file.name}"

            # Salvar o arquivo temporário
            with open(temp_file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Agora podemos abrir o PDF corretamente
            doc = fitz.open(temp_file_path)

            if len(doc) == 0:
                st.error("❌ O arquivo PDF está vazio ou corrompido.")
            else:
                # Processar Certificado
                df = ds.extrair_elementos_pdf_usiminas(temp_file_path, linha)
                if df is None or df.empty:
                    st.error(f"⚠️ A linha {linha} não contém dados válidos no certificado.")
                else:
                    C = df.loc["C", 0]
                    Mn = df.loc["Mn", 0]
                    Si = df.loc["Si", 0]
                    Cr = df.loc["Cr", 0]
                    Mo = df.loc["Mo", 0]
                    Nb = df.loc["Nb", 0]
                    Ti = df.loc["Ti", 0]
                    V = df.loc["V", 0]
                    Ni = df.loc["Ni", 0]
                    Cu = df.loc["Cu", 0]
                    P = df.loc["P", 0]
                    S = df.loc["S", 0]
                    Al = df.loc["Al", 0]

                    ceq = round(ds.calcularCeq(C, Mn, Si, Cr, Mo, V, Nb, Ti, Ni, Cu), 2)
                    si_eq = ds.calcular_SilEq(Si, P)
                    laudo_solda = ds.calcularSolda(ceq)
                    laudo_usinagem = ds.calcularUsinagem(ceq)
                    laudo_galvanizacao = ds.calcularGalvanizacao(si_eq)
                    laudo_calandra = ds.calcularCalandra(ceq)
                    laudo_Dobra = ds.calcularDobra(ceq)
                    LE = round(ds.calcular_LE(C, Si, Mn, P, S, Al, Cu, Cr).item(), 2)
                    LR = round(ds.calcular_LR(C, Si, Mn, P, S, Al, Cu, Cr).item(), 2)
                    dureza = round(LR / 3.45)

                    similaridade = ds.verificar_compatibilidade(C, Mn, Si, P, S, LE, LR, ceq)

                    resultado = {
                        "Ceq (Carbono Equivalente)": ceq,
                        "Dureza Estimada (HB)": dureza,
                        "Laudo Soldabilidade": laudo_solda,
                        "Laudo Usinagem": laudo_usinagem,
                        "Laudo Calandra": laudo_calandra,
                        "Laudo Dobra": laudo_Dobra,
                        "Laudo Galvanização": laudo_galvanizacao,
                        "Similaridade do Material": similaridade
                    }

                    # Exibir mensagem de sucesso
                    st.success("✅ Análise concluída!")

                    # **Estilização para fonte maior nos resultados**
                    for parametro, valor in resultado.items():
                        st.markdown(
                            f"""
                            <div style="font-size:24px; font-weight:bold; color:#2E8B57; padding:8px; border-bottom: 2px solid #ccc;">
                                {parametro}: {valor}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

            # Remover o arquivo temporário após o processamento
            os.remove(temp_file_path)

        except Exception as e:
            st.error(f"❌ Ocorreu um erro: {str(e)}")
