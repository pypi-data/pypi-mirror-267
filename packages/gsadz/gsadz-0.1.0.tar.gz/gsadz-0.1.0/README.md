# GSADZ - Ferramenta de Análise de Sentimento para a língua portuguesa

O **gsadz** apresenta-se como um módulo de análise de sentimento para a língua portuguesa, baseado num léxico de sentimentos denominado [```SentiLex-PT 02```](https://b2find.eudat.eu/dataset/b6bd16c2-a8ab-598f-be41-1e7aeecd60d3), e um conjunto de negadores e boosters adaptados a partir da recolha através da ferramenta [```LeIA```](https://github.com/rafjaa/LeIA).

### Exemplo de Utilização

#### Como módulo:
O módulo SentimentAnalysis apresenta dois parâmetros relativos à calibração das polaridades, conferindo a possibilidade de atribuição de diferentes pesos entre elas.

```py
from gsadz import SentimentAnalysis

text = "Nesta bela manhã, encontro-me feliz."
```

- Sem calibração de polaridades
```py
sa = SentimentAnalysis()

print(sa.polarity_result(text))
# {'Polarity': 1.0, 'Words': 5, 'Puncts': 2, 'Boosters': 0, 'Deniers': 0, 'Positives': 2, 'Negatives': 0, 'Neutrals': 0}
```

- Com calibração de polaridades
```py
# A polaridade positiva apresenta um peso de 1.75 e a negativa de 0.75
sa = SentimentAnalysis(1.75, 0.75)

print(sa.polarity_result(text))
# {'Polarity': 1.75, 'Words': 5, 'Puncts': 2, 'Boosters': 0, 'Deniers': 0, 'Positives': 2, 'Negatives': 0, 'Neutrals': 0}
```

#### Como script:
```
gsadz [Opção].. [Ficheiro]...

Sem Ficheiro, o input é recebido através do stdin.

Opções

    -n NUM     Calibração de polaridade negativa

    -p NUM     Calibração de polaridade positiva

    -v         Output em modo non-verbose
```


### Features

- Negadores
```py
print(sa.polarity_result("Não gosto nada de ti."))
# {'Polarity': -1.0, 'Words': 5, 'Puncts': 1, 'Boosters': 0, 'Deniers': 1, 'Positives': 1, 'Negatives': 0, 'Neutrals': 0}
```
- Boosters
```py
print(sa.polarity_result("És incrivelmente inteligente."))
# {'Polarity': 1.25, 'Words': 3, 'Puncts': 1, 'Boosters': 1, 'Deniers': 0, 'Positives': 1, 'Negatives': 0, 'Neutrals': 0}
```

- Expressões idiomáticas 
```py
print(sa.polarity_result("O João dá de frosques."))
# {'Polarity': -1.0, 'Words': 5, 'Puncts': 1, 'Boosters': 0, 'Deniers': 0, 'Positives': 0, 'Negatives': 1, 'Neutrals': 0}
```

### Output

* ```Polarity```: Valor final da polaridade do input
    + ```Polarity > 0``` : Sentimento positivo
    + ```Polarity == 0```: Sentimento neutro
    + ```Polarity < 0``` : Sentimento Negativo

* ```Words```: Total de palavras
* ```Puncts```: Total de tokens relativos a qualquer pontuação
* ```Boosters```: Total de intensificadores
* ```Deniers```: Total de palavras de negadores
* ```Positives```: Total de palavras com polaridade positiva
* ```Negatives```: Total de palavras com polaridade negativa
* ```Neutrals```: Total de palavras com polaridade neutra


### Instalação
```
$ pip install gsadz
$ python -m spacy download pt_core_news_lg
```



