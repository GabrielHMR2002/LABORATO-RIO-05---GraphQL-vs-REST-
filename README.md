# LAB05 – GraphQL vs REST  
## Um Experimento Controlado para Análise de Desempenho e Tamanho de Respostas

Este repositório contém o trabalho desenvolvido para o Laboratório 05 (LAB05) da disciplina Laboratório de Experimentação de Software, ministrada pelo professor João Paulo Carneiro Aramuni, no curso de Engenharia de Software – 6º período.

O objetivo deste experimento é comparar quantitativamente APIs GraphQL e REST com base em duas perguntas de pesquisa:

- RQ1: Respostas às consultas GraphQL são mais rápidas que respostas às consultas REST?  
- RQ2: Respostas às consultas GraphQL têm tamanho menor que respostas às consultas REST?

---

## Conteúdo do Repositório

- /scripts – Scripts utilizados para aplicação dos tratamentos e coleta dos dados  
- /datasets – Dados coletados durante o experimento  
- /dashboard – Código e artefatos do dashboard  
- /report – Relatório final  
- README.md – Documento principal  

---

# 1. Desenho do Experimento

O experimento foi desenvolvido com base em princípios de experimentação controlada, buscando garantir reprodutibilidade e controle das variáveis envolvidas.

## Hipóteses

### RQ1 – Tempo de resposta
- H0₁: Não há diferença significativa no tempo de resposta entre GraphQL e REST.  
- H1₁: GraphQL apresenta tempo de resposta significativamente menor que REST.

### RQ2 – Tamanho da resposta
- H0₂: Não há diferença significativa no tamanho das respostas entre GraphQL e REST.  
- H1₂: GraphQL apresenta respostas significativamente menores que REST.

## Variáveis

### Variáveis Dependentes
- Tempo de resposta (ms)  
- Tamanho da resposta (bytes)

### Variáveis Independentes
- Tipo da API (REST ou GraphQL)

### Variáveis de Controle
- Ambiente de execução  
- Rede  
- Tipo de consulta  
- Número de trials  
- Máquina utilizada  

## Tratamentos

- T1: Execução da consulta utilizando REST  
- T2: Execução da consulta utilizando GraphQL  

## Objetos Experimentais

- API preparada com endpoints equivalentes em REST e GraphQL  
- Conjunto padronizado de consultas  

## Tipo de Projeto Experimental

- Experimento controlado intra-sujeitos  
- Execução repetida sob condições fixas  

## Quantidade de Medições

- Número pré-definido de trials por API (detalhado no relatório final)

## Ameaças à Validade

- Possível variação na rede  
- Cache de respostas  
- Aquecimento da máquina  
- Diferenças internas entre as tecnologias  
- Outliers decorrentes de instabilidades momentâneas  

---

# 2. Preparação do Experimento

A preparação envolveu:

- Desenvolvimento de scripts automáticos para consultas REST e GraphQL  
- Definição do ambiente experimental  
- Escolha das ferramentas de coleta e análise  
- Estruturação dos datasets e logs  
- Testes preliminares para validar comportamento e consistência das respostas  

---

# 3. Execução do Experimento

Durante a execução:

- Cada consulta foi enviada repetidamente tanto via REST quanto via GraphQL  
- Para cada resposta foram registrados:  
  - Tempo de resposta  
  - Tamanho do corpo retornado  
- Todos os dados foram armazenados em arquivos próprios para análise  

---

# 4. Análise dos Resultados

A análise envolveu:

- Inspeção inicial dos dados coletados  
- Remoção de valores extremos quando justificado  
- Cálculo de estatísticas descritivas  
- Comparação entre REST e GraphQL com base nas variáveis dependentes  
- Interpretação dos resultados no contexto de RQ1 e RQ2  

Os resultados completos encontram-se no relatório final.

---

# 5. Relatório Final

O relatório apresenta:

1. Introdução e fundamentação  
2. Hipóteses  
3. Metodologia e ambiente utilizado  
4. Execução detalhada do experimento  
5. Resultados obtidos  
6. Respostas às perguntas de pesquisa  
7. Discussão geral  

O relatório está disponível na pasta `/report`.

---

# 6. Dashboard de Visualização

Foi criado um dashboard para facilitar a interpretação dos resultados, apresentando:

- Gráficos comparativos de tempo de resposta  
- Gráficos comparativos de tamanho das respostas  
- Tabelas estatísticas  
- Consolidação visual dos dados coletados

Acesso ao dashboard:

https://claude.ai/public/artifacts/e7348c78-7534-4b63-9943-b854a2817b72

---

