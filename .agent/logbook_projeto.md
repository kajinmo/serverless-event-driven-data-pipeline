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

**Data de Início:** **_/_**/**_
**Data de Conclusão:** _**/**_/_**

### Tarefas Realizadas

- [ ] Terraform: Criação da State Machine (Step Functions) provisionada no Floci.
- [ ] Terraform: Lambda empacotado e provisionado no ambiente local.
- [ ] Step Functions lendo nativamente o DynamoDB e repassando o payload consolidado.
- [ ] Lambda recebendo o JSON do Step Functions e persistindo dados no DocumentDB emulado (Floci).

### Decisões Técnicas e Trade-offs

- ...

### Bugs / Desafios Encontrados

- ...

---

## 📝 Épico 3: Deploy Real e Banco Híbrido

**Data de Início:** **_/_**/**_
**Data de Conclusão:** _**/**_/_**

### Tarefas Realizadas

- [ ] Substituição da _connection string_ para o MongoDB Atlas.
- [ ] Terraform: Alteração dos endpoints para deploy na AWS verdadeira.

### Decisões Técnicas e Trade-offs

- ...
