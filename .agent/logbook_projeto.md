# Diário de Bordo (Logbook) - Projeto EDA

Use este documento para registrar suas decisões arquiteturais, bugs encontrados, e lições aprendidas. Um bom portfólio documenta não apenas o código final, mas a jornada e os _trade-offs_.

---

## 📝 Épico 1: Fundações e Carga de Dados

**Data de Início:** 06/09/2026
**Data de Conclusão:** 06/09/2026

### Tarefas Realizadas

- [x] Ambiente local emulado inicializado via Docker (Floci), incluindo o serviço `docdb`.
- [x] Construção do código Terraform para as tabelas do DynamoDB apontando para o localhost.
- [x] Script Python com `Faker` e `Pydantic` criado, validando e inserindo dados no emulador local.

### Decisões Técnicas e Trade-offs

- **Clean Architecture & Modularização:** Decidimos quebrar o `seed.py` monolítico em módulos como `src/models/contracts.py` (Data Contracts isolados para reuso no Lambda futuro) e `src/infra/dynamodb.py` para isolar a configuração Boto3.
- **Data Contracts e Idioma:** Todo o código fonte e as tabelas Terraform foram traduzidas para o Inglês, alinhado às boas práticas da engenharia de software global.
- _Ex: Decisão de Arquitetura Híbrida: Utilizar DocumentDB emulado no desenvolvimento local para espelhar o ambiente corporativo, mas migrar para MongoDB Atlas Serverless na produção para garantir eficiência e custo zero, mitigando o overhead de rede (VPCs/Subnets) que o DocumentDB exige na AWS real._

### Bugs / Desafios Encontrados

- ...

### Lições Aprendidas

- ...

---

## 📝 Épico 2: Orquestração Sênior (Step Functions no Floci)

**Data de Início:** 06/09/2026
**Data de Conclusão:** 06/09/2026

### Tarefas Realizadas

- [x] Terraform: Criação da State Machine (Step Functions) provisionada no Floci.
- [x] Terraform: Lambda empacotado e provisionado no ambiente local.
- [x] Step Functions lendo nativamente o DynamoDB e repassando o payload consolidado.
- [x] Lambda recebendo o JSON do Step Functions e persistindo dados no MongoDB (Floci).

### Decisões Técnicas e Trade-offs

- **Substituição do Serviço MongoDB:** Descobrimos que o serviço emulado `docdb` no Floci não expõe o MongoDB na porta 27017, então optamos por adicionar um contêiner oficial do MongoDB (`mongo:latest`) no `docker-compose.yml` para garantir que a Lambda tivesse um banco disponível para conexão.

### Bugs / Desafios Encontrados

- **Networking no Docker Bridge:** Enfrentamos um grande desafio com timeouts `ServerSelectionTimeoutError` do `pymongo` conectando a partir da Lambda. A Lambda roda em seu próprio contêiner gerado sob demanda pelo Floci. Resolvemos apontando a URI de conexão para `mongodb://eda-mongodb:27017/` já que a Lambda está na mesma rede Docker (`serverless-event-driven-data-pipeline_default`).

---

## 📝 Épico 3: Deploy Real e Banco Híbrido

**Data de Início:** 07/09/2026
**Data de Conclusão:** 07/09/2026

### Tarefas Realizadas

- [x] Backup do ambiente local `floci/`.
- [x] Ajustar os arquivos Terraform (remover `endpoints` locais) e configurar o _AWS profile_.
- [x] Configurar as credenciais do banco de dados na AWS (usando SSM Parameter Store).
- [x] Atualizar a Lambda para resgatar e utilizar essas senhas dinamicamente (`MONGO_USER` e `MONGO_PASSWORD`).
- [x] Fazer o deploy oficial da infraestrutura na AWS.

### Decisões Técnicas e Trade-offs

- Uso de `mongodb+srv` gerado dinamicamente para não deixar _connection strings_ expostas nem dependentes do arquivo `terraform.tfstate`.

---

## 📝 Épico 4: Integração E2E (End-to-End) e Validação de Dados

**Data de Início:** 07/09/2026
**Data de Conclusão:** _**/**_/_**

### Tarefas Planejadas

- [x] Injetar payload de teste diretamente na Step Functions (via AWS CLI).
- [x] Validar a visualização dos dados consolidados no MongoDB Atlas.
- [x] Garantir que o pipeline assíncrono ocorre com sucesso sem falhas de timeout.

### Decisões Técnicas e Trade-offs

- Para viabilizar o teste E2E real, injetamos mock data (`test-aws-atlas-001`) diretamente nas tabelas DynamoDB da AWS, permitindo que a _State Machine_ consumisse os dados nativamente através do `getItem`.
- **Bug/Desafio Resolvido:** Durante a primeira execução da Step Functions, identificamos que a _Role IAM_ associada à máquina de estados não possuía permissões (`dynamodb:GetItem` e `lambda:InvokeFunction`). Corrigimos a infraestrutura no Terraform adicionando uma `inline_policy` e realizamos um novo _apply_.
