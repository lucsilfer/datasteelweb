import streamlit as st
import pandas as pd
import fitz  # PyMuPDF para leitura de PDFs
import DS_Calculos as ds  # Certifique-se de que esse módulo está disponível

st.set_page_config(page_title="Análise de Certificados Usiminas", layout="wide")

st.title("🔬 Análise de Certificados de Aço Carbono NRU - NTU - Usiminas")

# Upload do arquivo PDF
uploaded_file = st.file_uploader("📄 Envie o Certificado PDF", type=["pdf"])

linha = st.text_input("🔍 Linha do Certificado a Analisar", "")

if uploaded_file and linha:
    if not linha.strip().isdigit():
        st.error("Por favor, insira um número válido para a linha do certificado.")
    else:
        try:
            # Abrir o PDF
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            if len(doc) == 0:
                st.error("O arquivo PDF está vazio ou corrompido.")
            else:
                # Processar Certificado
                df = ds.extrair_elementos_pdf_usiminas(uploaded_file, linha)
                if df is None or df.empty:
                    st.error(f"A linha {linha} não contém dados válidos no certificado.")
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

                    df_resultado = pd.DataFrame(resultado.items(), columns=["Parâmetro", "Valor"])

                    st.dataframe(df_resultado)

        except Exception as e:
            st.error(f"Ocorreu um erro: {str(e)}")
