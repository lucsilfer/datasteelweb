def calcularCeq(C,Mn,Si,Cr,Mo,V,Nb,Ti,Ni,Cu):
    ceq = C+(Mn/6)+(Si/24)+((Cr+Mo+V+Nb+Ti)/5)+((Ni+Cu)/15)
    
    return ceq

def calcular_SilEq(Si,P):
    
    sil_Eq = Si + (2.5*P)
    return sil_Eq

def calcularSolda(ceq):
    if ceq < 0.40:
        return "Boa soldabilidade"
    elif ceq > 0.50:
        return "Baixa soldabilidade"
    else:
        return "Razoável soldabilidade"

def calcularUsinagem(ceq):
    if ceq>=0.45:
        return "Possibilidade de trinca"
    elif ceq < 0.35:
        return "Otimas condições"
    else:
        return"Condições normais"

def calcularGalvanizacao(sil_Eq):
    if sil_Eq >0.05:
        return "Desfavorável"
    else:
        return "Adequado"

def calcular_LE(C,Si,Mn,P,S,Al,Cu,Cr):

    import pandas as pd
    independente = pd.read_csv('independente.csv',header=None)
    dependente = pd.read_csv('dependente.csv',header=None)

    independente = independente.values
    dependente = dependente.iloc[:, 0].values

    from sklearn.model_selection import train_test_split

    from xgboost import XGBRegressor
    xgboost = XGBRegressor(objective='reg:squarederror',
    colsample_bytree=0.7,
    learning_rate=0.1,
    max_depth=5,
    n_estimators=50,
    subsample=0.7,
    random_state=42)
    xgboost.fit(independente, dependente)

  # Fazendo previsões para valores distintos
    informacoes = [C,Si,Mn,P,S,Al,Cu,Cr]
    LE = xgboost.predict([informacoes])

    return LE

def calcular_LR(C,Si,Mn,P,S,Al,Cu,Cr):

    import pandas as pd
    independente = pd.read_csv('independente.csv',header=None)
    dependente_LR = pd.read_csv('dependente_LR.csv',header=None)

    independente = independente.values
    dependente_LR = dependente_LR.values

    from sklearn.model_selection import train_test_split

    from xgboost import XGBRegressor

    xgboost2 = XGBRegressor(n_estimators=180, max_depth=3, 
                            learning_rate=0.05, objective="reg:squarederror", 
                            random_state=10)
    xgboost2.fit(independente, dependente_LR)

  # Fazendo previsões para valores distintos
    informacoes = [C,Si,Mn,P,S,Al,Cu,Cr]
    LR = xgboost2.predict([informacoes])

    return LR

def extrair_elementos_pdf_usiminas(caminho,linha):
  import PyPDF2
  import sys

  with open(caminho, 'rb') as pdf_file:

    # Criar um objeto PDF Reader
      pdf_reader = PyPDF2.PdfReader(pdf_file)

      # Iterar pelas páginas do arquivo PDF
      for page_num in range(len(pdf_reader.pages)):
          # Obter a página atual
          page = pdf_reader.pages[page_num]

          # Obter o conteúdo da página como uma string
          page_content = page.extract_text()
          
          # Verificar se a referência desejada está na página
          if 'Análise' in page_content:

            
            # Encontrou a referência - imprimir a linha seguinte

              #entrada = input('Qual Linha deseja Analisar ?  ') 
              print()
              numero = int(1)
              linha = int(linha)

              ent = numero + linha          
              lines = page_content.split('\n')
              for i in range(len(lines)):
                  if 'Análise' in lines[i]:
                      prev_line = lines[i+ent]
                      indice_line=lines[i]
                  
                      break

  #Transformando os textos extraidos em Array
  indice = indice_line.split()
  valores = prev_line.split()

  # Criar o dataframe com as duas arrays
  import pandas as pd
  df = pd.DataFrame(valores, indice)

  #Transformando a Array em Indice do df
  df = df.set_index(pd.Index(indice))

  #excluindo as linhas que não serão aproveitadas
  try:

    df = df.loc[["C", "Si", "Mn","Cr","Mo","V", "Nb", "Ti","Ni","Cu","P","S","Al"]]

  except KeyError:
      print("O Certificado não apresenta todos os elementos necessários para análise.")
      sys.exit()


  #Transformando os valores da df de String para Float
  df[df.columns[0]] = df[df.columns[0]].apply(lambda x: float(x.replace(',', '.')))

  elementos = {'C': df.loc["C", 0],
                     'Si': df.loc["Si", 0],
                     'Mn': df.loc["Mn", 0],
                     'Cr': df.loc["Cr", 0],
                     'Mo': df.loc["Mo", 0],
                     'V': df.loc["V", 0],
                     'Nb': df.loc["Nb", 0],
                     'Ti': df.loc["Ti", 0],
                     'Ni': df.loc["Ni", 0],
                     'Cu': df.loc["Cu", 0],
                     'P': df.loc["P", 0],
                     'S': df.loc["S", 0],
                     'Al': df.loc["Al", 0]}

  return df

def verificar_compatibilidade(C,Mn,Si,P, S,LE,LR,ceq):
    if C < 0.25 and Si < 0.40 and Mn < 1.20 and P < 0.040 and S < 0.050 and LE > 250 and LR >= 400 and LR <= 550 and ceq<=0.45:
        resultado = "ASTM-A36"
    elif C < 0.23 and Si < 0.40 and Mn < 1.52 and Mn > 0.60 and P < 0.040 and S < 0.050 and LE > 345 and LR >= 450 and ceq<=0.42:
        resultado = "ASTM-A572GR50"
    else:
        resultado = "COMERCIAL"

    return resultado


