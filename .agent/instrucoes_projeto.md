# Instruções do Projeto: Pipeline de Dados Orientado a Eventos (EDA)

## Visão Geral

Projeto de tiro curto para portfólio e treinamento focado em Engenharia de Dados. O objetivo é simular um cenário real de consolidação de dados oriundos de microsserviços distintos em um banco de dados NoSQL, evoluindo de uma arquitetura simples baseada em filas para uma orquestração robusta de estados.

## Stack Tecnológica

- **Infraestrutura como Código (IaC):** Terraform
- **Emulador de Nuvem Local:** Floci (via Docker)
- **Linguagem:** Python 3.x
- **Bibliotecas Principais:** `boto3` (AWS), `pymongo` (DocumentDB/MongoDB), `Faker` (Geração de Dados), `pydantic` (Data Contracts)
- **AWS Services:** DynamoDB, SQS, Lambda, Step Functions, IAM
- **Destino Híbrido (Data Lakehouse/App DB):** Amazon DocumentDB (Emulado localmente via Floci) -> MongoDB Atlas (Tier Gratuito em Produção).

---

## Roadmap de Desenvolvimento

### Épico 1: Fundações e Carga de Dados Sintéticos

**Objetivo:** Preparar o terreno, subir o ambiente de desenvolvimento local e popular os bancos com dados de teste respeitando contratos de dados.

1.  **Ambiente Local com Floci:**
    - Suba o emulador Floci via `docker-compose` ativando os serviços: `dynamodb`, `sqs`, `lambda` e `docdb`.
2.  **Terraform - Tabelas DynamoDB (Local):**
    - Crie um módulo Terraform para provisionar duas tabelas: `tb_usuarios_perfil` e `tb_usuarios_atividade`.
    - Configure os _endpoints_ no Terraform para apontar para o Floci (`http://localhost:4566`).
    - Configure _Billing Mode_ como `PAY_PER_REQUEST`.
3.  **Script de Carga (Python):**
    - Utilize a biblioteca `Faker` e `pydantic` gerando um dataset de perfis e atividades.
    - Insira os dados em pequenos lotes no DynamoDB (apontando o `boto3` para o Floci) utilizando `batch_write_item`.

### Épico 2: Orquestração Sênior (Step Functions no Floci)

**Objetivo:** Consolidar os dados utilizando a orquestração robusta do AWS Step Functions, ainda 100% isolado na máquina local (Floci).

1.  **Terraform - Step Functions e Lambda:**
    - Adicione ao Terraform a criação da State Machine (Step Functions) no Floci.
    - Crie uma AWS Lambda Function em Python e faça o deploy localmente (para a etapa de consolidação final).
2.  **Desenho do Fluxo (ASL - Amazon States Language):**
    - **Passo 1 (Parallel State):** Utilize integrações nativas da AWS para ler o DynamoDB de forma paralela (`tb_user_profile` e `tb_user_activity`).
    - **Passo 2 (Wait State - Opcional):** Simular delay de longo processamento.
    - **Passo 3 (Task State - Lambda):** Lambda recebe o JSON consolidado.
3.  **Código do Lambda e Ingestão:**
    - O Lambda recebe o _payload_ consolidado pelo Step Functions.
    - Conecta no DocumentDB local (Floci) via `pymongo` e salva o documento consolidado.

### Épico 3: Deploy Real e Banco Híbrido (AWS + MongoDB Atlas)

**Objetivo:** Subir a infraestrutura para a AWS real e alterar a _connection string_ para o MongoDB Atlas (Custo Zero).

1.  **Migração para a Nuvem e Atlas:**
    - Remova os _endpoints_ locais do Terraform e aplique o código na sua conta AWS verdadeira.
    - Altere a URI de conexão no código Lambda para apontar para o cluster gratuito do MongoDB Atlas, evitando os custos de infraestrutura do DocumentDB na nuvem.

---

## Mentoria / Lembretes de Arquitetura

- **Contratos de Dados:** A validação na borda com `pydantic` evita lixo no banco.
- **Idempotência:** Garanta que operações possam ser repetidas sem duplicar registros.
- **Git Commits:** Mensagens de commit sempre em uma única linha e estritamente em inglês (ex: `feat: ...`, `fix: ...`).
