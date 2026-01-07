import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import glob

def carregar_estados_csv(padrao) -> pd.DataFrame:
    """Carrega todos os arquivos CSV de estados em um único DataFrame."""
    arquivos = glob.glob(padrao)
    if not arquivos:
        raise FileNotFoundError("Nenhum arquivo CSV encontrado com o padrão fornecido.")
    df_list = [pd.read_csv(arquivo) for arquivo in arquivos] # Lista de DataFrames
    df_concatenado = pd.concat(df_list, ignore_index=True)
    return df_concatenado

def limpar_dados_dinheiro(df):
    """Limpa a coluna de valor, removendo símbolo de moeda e convertendo para float."""
    extraido = df.astype(str).str.extract(r'([\d,.]+)', expand=False) # \d para números e ,. literal
    return pd.to_numeric(extraido, errors='coerce')

def limpar_dados_porcentagem(df):
    """Detecta colunas que contém "%" e as retorna somente com os valores numéricos."""
    cols_pct = [
        col for col in df.columns if df[col].astype(str).str.contains('%').any()
    ]
    if not cols_pct:
        return df
    df[cols_pct] = df[cols_pct].apply(
        lambda x : pd.to_numeric(x.astype(str).str.extract(r'([\d,.]+)', expand=False), errors='coerce')
    )
    return df

def separar_genero_pop(df, coluna):
    """Separa a coluna de população por gênero em duas colunas diferentes"""
    extraido = df[coluna].astype(str).str.extract(r'(\d+)M_(\d+)F')
    df[['male', 'female']] = extraido.apply(pd.to_numeric, errors='coerce')
    return df.drop(columns=[coluna])
def limpar_dados(df):
    """Limpa todo o dataframe """
    df = df.copy()
    if 'Income' in df.columns:
        df['Income'] = limpar_dados_dinheiro(df['Income'])
    
    df= limpar_dados_porcentagem(df)

    if 'GenderPop' in df.columns:
        df = separar_genero_pop(df, 'GenderPop')
    return df


def main():
    df_cru = carregar_estados_csv('states*.csv')
    df_limpo = limpar_dados(df_cru)
    print("Dados limpos:")
    print(df_limpo.head())
    print(df_limpo.info())
    print(df_limpo.dtypes)

if __name__ == "__main__":
    main()