# DataGrim (Backend)

##  Sobre o DataGrim

O DataGrim é uma aplicação desenvolvida com foco em ingestão, organização e análise de dados, permitindo realizar validações, controle de qualidade e gerenciamento de informações através de uma API REST.

O projeto foi desenvolvido como uma proposta inicial para Trabalho de Conclusão de Curso (TCC), com o objetivo de criar uma plataforma simples e modular para manipulação e validação de dados. Apesar da ideia principal não ter sido concluída como TCC final, o projeto continuou sendo desenvolvido como estudo prático e aplicação de conceitos de desenvolvimento backend.

---

## Tecnologias utilizadas

O backend foi construído utilizando:

- Python
- FastAPI
- SQLite
- Uvicorn

---

## ️ Instruções de instalação

### 1. Clone o repositório

```bash
git clone https://github.com/SEU_USUARIO/datagrim-backend.git
```

---

### 2. Acesse a pasta do projeto

```bash
cd datagrim-backend
```

---

### 3. Crie um ambiente virtual

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux/Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

---

### 5. Execute o servidor

```bash
uvicorn app.main:app --reload
```

---

##  Instruções de uso

1. Execute o servidor localmente
2. Acesse a documentação automática da API
3. Realize uploads ou consultas utilizando os endpoints disponíveis
4. Utilize os módulos de ingestão, histórico e qualidade de dados

---

## Endpoints e documentação

Após iniciar o servidor, a documentação da API poderá ser acessada em:

### Swagger UI

```bash
http://127.0.0.1:8000/docs
```

### ReDoc

```bash
http://127.0.0.1:8000/redoc
```

---

##  Principais funcionalidades

-  Upload de arquivos
-  Ingestão de dados
-  Validação de qualidade de dados
-  Histórico de análises
-  Persistência local com SQLite
-  API REST modular

---

##  Segurança

Arquivos sensíveis e dados locais são ignorados através do `.gitignore`, incluindo:

- `.env`
- bancos locais
- uploads
- exports
- ambientes virtuais

---

## 📄 Licença

Este projeto é destinado para fins acadêmicos, estudos e desenvolvimento pessoal.
