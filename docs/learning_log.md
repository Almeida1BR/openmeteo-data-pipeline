# Registro de aprendizagem e progresso

Este arquivo registra marcos já implementados e o próximo foco, para manter o projeto guiado sem perder decisões entre as etapas.

## 2026-10-04 — consulta ao snapshot recente e primeira tela

- Adicionada ao repositório uma consulta que seleciona a coleta meteorológica mais recente e ordena seus horários.
- Criada a primeira tela Streamlit com tabela, cartões de temperatura, umidade e probabilidade de precipitação e um gráfico de temperatura.
- Ajustado o container do dashboard para importar o pacote Python em `src` e conectar-se ao Postgres usando `psycopg`.
- A integração da tela com a função de consulta ainda precisa ser validada em execução. Não considerar esta etapa finalizada até que o dashboard carregue dados reais do banco.

## Conceitos praticados

- Consulta SQLAlchemy ordenada e subconsulta escalar para identificar o snapshot mais recente.
- Conversão de registros Python em `pandas.DataFrame` para apresentar dados tabulares.
- Métricas e gráfico de linhas com Streamlit e Plotly Express.
- Caminhos de importação Python e configuração de dependências entre serviços Docker.

## Próxima validação

Com os serviços Compose em execução e registros presentes no Postgres, iniciar ou reconstruir o serviço `dashboard` e conferir a tabela, os três cartões e o gráfico. Resolver eventuais incompatibilidades entre os campos retornados pela consulta e os usados pela interface antes de registrar a etapa como concluída.
