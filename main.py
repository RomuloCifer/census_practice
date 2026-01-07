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
