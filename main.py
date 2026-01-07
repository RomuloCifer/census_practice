import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import glob
import logging

logging.basicConfig(level=logging.INFO)
def carregar_estados_csv(padrao) -> pd.DataFrame:
    """Carrega todos os arquivos CSV de estados em um único DataFrame."""
    arquivos = glob.glob(padrao)
    if not arquivos:
        raise FileNotFoundError("Nenhum arquivo CSV encontrado com o padrão fornecido.")
    df_list = [pd.read_csv(arquivo) for arquivo in arquivos] # Lista de DataFrames
    df_concatenado = pd.concat(df_list, ignore_index=True)
    return df_concatenado

def limpar_dados_dinheiro(s):
    """Limpa a coluna de valor, removendo símbolo de moeda e convertendo para float."""
    extraido = s.astype(str).str.extract(r'([\d,.]+)', expand=False) # \d para números e ,. literal
    extraido = extraido.str.replace(',', '') #Remove virgulas para não virar NaN
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

def plt_scatter(df, x_col, y_col):
    """Plota um gráfico de dispersão entre duas colunas"""
    plt.figure()
    plt.scatter(df[x_col], df[y_col])
    plt.xlabel('Female population (millions)')
    plt.ylabel(y_col)
    plt.title(f'Scatter plot of {y_col} vs {x_col}')
    plt.show()

def preencher_faltantes_genero(df):
    """Preenche os valores faltantes das colunas de gênero com base na população total.
    REGRAS: 
    - Se somente female estiver faltando, preenche com TotalPop - male
    - Se somente male estiver faltando, preenche com TotalPop - female
    - Se ambos estiverem faltando, não preenche, eles são deixados como NaN
    """
    # 1 caso: female nan, male válido
    mask_female_nan = df['female'].isna() & df['male'].notna()
    df.loc[mask_female_nan, 'female'] = (
    df.loc[mask_female_nan, 'TotalPop'] -
    df.loc[mask_female_nan, 'male']
    )
    logging.info(f"Total de valores faltantes em nas colunas male e female após o preenchimento: {df[['male', 'female']].isna().sum().sum()}")


    # 2 caso: male nan, female válido
    mask_male_nan = df['male'].isna() & df['female'].notna()
    df.loc[mask_male_nan, 'male'] = (
        df.loc[mask_male_nan, 'TotalPop'] -
        df.loc[mask_male_nan, 'female']
    )

    return df

def main():
    df_cru = carregar_estados_csv('states*.csv')
    df_limpo = limpar_dados(df_cru)
    df_preenchido = preencher_faltantes_genero(df_limpo)
    plt_scatter(df_preenchido, "female", "Income")



if __name__ == "__main__":
    main()

    