# Census Practice

Projeto de prática em análise de dados com **Pandas** e **Matplotlib**, usando arquivos CSV de estados dos EUA.

O script principal faz:
- carregamento de múltiplos arquivos `states*.csv`;
- limpeza de colunas numéricas (moeda e porcentagens);
- separação da coluna `GenderPop` em `male` e `female`;
- preenchimento parcial de valores ausentes de gênero com base em `TotalPop`;
- visualização da distribuição percentual por raça em histogramas lado a lado.

## Estrutura do projeto

```text
census_practice/
├── main.py
├── requirements.txt
├── states0.csv
├── states1.csv
├── ...
└── states9.csv
```

## Requisitos

- Python 3.9+ (recomendado)
- Dependências em `requirements.txt`:
  - `pandas`
  - `numpy`
  - `matplotlib`
  - `jupyter`

## Instalação

No diretório do projeto:

```bash
python -m venv .venv
```

### Windows (PowerShell)

```bash
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Linux/macOS

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## Como executar

Com o ambiente ativado:

```bash
python main.py
```

Ao executar, o script:
1. junta os arquivos `states*.csv` em um único DataFrame;
2. limpa os dados;
3. gera histogramas comparativos para as colunas:
   - `Hispanic`
   - `White`
   - `Black`
   - `Native`
   - `Asian`

## Regras de limpeza implementadas

### 1) Coluna de renda (`Income`)

Remove símbolos e separadores para converter em número (`float`).

### 2) Colunas percentuais

Detecta automaticamente colunas com `%` e converte para valores numéricos.

### 3) Coluna `GenderPop`

Converte strings no formato `123M_456F` em duas colunas:
- `male`
- `female`

### 4) Preenchimento de faltantes (`male` / `female`)

- Se apenas `female` estiver ausente: `female = TotalPop - male`
- Se apenas `male` estiver ausente: `male = TotalPop - female`
- Se ambos estiverem ausentes: mantém `NaN`

Essa estratégia evita inferências forçadas quando não há informação suficiente.

## Funções principais (`main.py`)

- `carregar_estados_csv(padrao)`
- `limpar_dados_dinheiro(s)`
- `limpar_dados_porcentagem(df)`
- `separar_genero_pop(df, coluna)`
- `limpar_dados(df)`
- `preencher_faltantes_genero(df)`
- `inspecionar_dataset(df)`
- `plt_hist_lado_a_lado(df, cols, bins=15)`

## Melhorias

- salvar gráficos automaticamente em arquivo (`.png`);
- adicionar testes para funções de limpeza;
- exportar o DataFrame final para CSV tratado;
- adicionar argumentos de linha de comando para escolher visualizações.