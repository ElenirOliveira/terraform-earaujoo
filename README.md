# 🌿 Terraform AWS Data Pipeline — Earaujo

## 📌 Visão Geral

Este projeto implementa um pipeline de dados completo na AWS utilizando Terraform como infraestrutura como código.

A arquitetura foi construída com foco em organização, escalabilidade e boas práticas de engenharia de dados, separando responsabilidades entre coleta, processamento e orquestração.

---

## 🧠 Arquitetura do Projeto

O fluxo do pipeline segue a seguinte ordem:

```text
GitHub Actions → Terraform → AWS

Step Function
   ↓
Lambda (coleta dados)
   ↓
S3 (Landing Zone)
   ↓
Glue Jobs
   ↓
LZ → SOR → SOT → SPEC
```

---

## 🧩 Componentes

### 🔹 AWS Lambda

Responsável por coletar dados de uma API externa e armazenar no S3.

* Runtime: Python 3.12
* Entrada: API externa
* Saída: S3 (camada LZ)

---

### 🔹 Amazon S3

Data Lake do projeto.

Estrutura de camadas:

* `lz/` → dados brutos
* `sor/` → dados organizados
* `sot/` → dados tratados
* `spec/` → dados prontos para consumo

---

### 🔹 AWS Glue

Responsável pelo processamento dos dados.

Jobs criados:

* LZ → SOR
* SOR → SOT
* SOT → SPEC

---

### 🔹 AWS Step Functions

Orquestra toda a execução do pipeline:

1. Executa Lambda
2. Executa Glue LZ → SOR
3. Executa Glue SOR → SOT
4. Executa Glue SOT → SPEC

---

### 🔹 Terraform

Responsável por provisionar toda a infraestrutura:

* Lambda
* S3
* Glue Jobs
* Step Function
* IAM Roles

---

### 🔹 GitHub Actions

Responsável pelo deploy automatizado da infraestrutura.

---

## 🔐 Controle de Acesso (IAM)

O projeto segue o princípio de menor privilégio, com roles separadas:

| Serviço        | Role                |
| -------------- | ------------------- |
| GitHub Actions | github_actions_role |
| Lambda         | lambda_role         |
| Glue           | glue_role           |
| Step Function  | step_function_role  |

Cada serviço possui permissões específicas para sua função.

---

## 📂 Estrutura do Projeto

```text
terraform-earaujoo/
│
├── infra/
│   ├── main.tf
│   ├── variables.tf
│   ├── iam.tf
│   ├── backend.tf
│   ├── outputs.tf
│   └── envs/
│       └── dev.tfvars
│
├── src/
│   ├── lambda/
│   │   └── index.py
│   └── glue_jobs/
│       ├── lz_to_sor.py
│       ├── sor_to_sot.py
│       └── sot_to_spec.py
│
└── .github/
    └── workflows/
        ├── 00-terraform.yml
        ├── 01-dev.yml
        └── 02-prd.yml
```

---

## ⚙️ Como Executar Localmente

### 1. Inicializar Terraform

```bash
cd infra
terraform init
```

---

### 2. Planejar execução

```bash
terraform plan -var-file="envs/dev.tfvars"
```

---

### 3. Aplicar infraestrutura

```bash
terraform apply -var-file="envs/dev.tfvars"
```

---

## 🚀 Execução do Pipeline

Após o deploy:

1. Acesse AWS Step Functions
2. Execute a State Machine
3. O pipeline será executado automaticamente

---

## 📌 Observações

* A Lambda utiliza variáveis de ambiente definidas via Terraform
* Os scripts do Glue são versionados no repositório e enviados ao S3
* O estado do Terraform é armazenado em S3 com lock via DynamoDB

---

## 🌿 Boas Práticas Aplicadas

* Infraestrutura como código (IaC)
* Separação de responsabilidades
* Princípio do menor privilégio (IAM)
* Versionamento com Git
* Pipeline automatizado (CI/CD)

---

## 📌 Próximos Passos

* Implementar lógica real nos Glue Jobs
* Adicionar monitoramento e alertas
* Criar camada de consumo (ex: Athena ou BI)
* Melhorar controle de permissões (escopo específico ao invés de `*`)

---

## ✍️ Autor

Projeto desenvolvido por Elenir Oliveira
Foco em Engenharia de Dados, Cloud e Arquitetura de Dados

---
