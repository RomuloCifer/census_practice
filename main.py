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

def plt_hist(df):
    """Plota um histograma para uma coluna específica do DataFrame."""
    cols_pct = ['Hispanic', 'White', 'Black', 'Native', 'Asian']
    for col in cols_pct:
        plt.figure()
        plt.hist(df[col].dropna(), bins=15)
        plt.xlabel(col)
        plt.ylabel('Frequency')
        plt.title(f'Distribution of {col} population')
        plt.show()

def plt_hist_lado_a_lado(df, cols, bins=15):
    fig, axes = plt.subplots(1, len(cols), figsize=(20, 4), sharey=True)

    for ax, col in zip(axes, cols):
        ax.hist(df[col].dropna(), bins=bins)
        ax.set_title(f'{col} population')
        ax.set_xlabel('Percentage of state population (%)')

    axes[0].set_ylabel('Number of states')

    fig.suptitle(
        'Distribution of population percentages by race across U.S. states',
        fontsize=14
    )

    plt.tight_layout(rect=[0, 0, 1, 0.92])
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

def inspecionar_dataset(df):
    info = []
    for col in df.columns:
        info.append({
            'coluna': col,
            'tipo': df[col].dtype,
            'valores_faltantes': df[col].isna().sum(),
            'pct_nan': df[col].isna().mean(),
            'valores_unicos': df[col].nunique(dropna=True)
        })
    return pd.DataFrame(info)


def main():
    df_cru = carregar_estados_csv('states*.csv')
    df_limpo = limpar_dados(df_cru)
    df_preenchido = preencher_faltantes_genero(df_limpo)
    # plt_scatter(df_preenchido, "female", "Income")
    # relatorio = inspecionar_dataset(df_preenchido)
    cols_pct = ['Hispanic', 'White', 'Black', 'Native', 'Asian']
    plt_hist_lado_a_lado(df_preenchido, cols_pct)
    print(df_preenchido.columns)

if __name__ == "__main__":
    main()

    