```markdown
## Tratamento de valores ausentes

Alguns estados apresentaram valores ausentes nas colunas de população `male` e `female`.

- Quando apenas um dos valores de gênero estava ausente, ele foi inferido usando:
  `TotalPop - genero_oposto`
- Quando ambos os valores `male` e `female` estavam ausentes, não foi possível inferir
  a linha, e os valores foram mantidos como NaN.

Essa abordagem evita introduzir viés artificial no conjunto de dados.
```