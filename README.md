# API de Produtos
![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791.svg)
![Docker](https://img.shields.io/badge/Docker-compose-2496ED.svg)
![Pytest](https://img.shields.io/badge/Pytest-9.1-0A9EDC.svg)

---

## Subindo os bancos PostgreSQL

```bash
docker-compose up -d
```

## Executando os testes

```bash
pytest -v
```

## Executando testes com cobertura
```bash
pytest --cov=main -v
```

## Executando servidor local 
```bash
uvicorn main:app --reload
```
---

## Saída esperada

![print da saída dos testes](image.png)

---

## Como funciona o isolamento dos testes

A fixture `client` cria as tabelas antes de cada teste utilizando:

```python
Base.metadata.create_all()
```

e remove todas as tabelas ao final utilizando:

```python
Base.metadata.drop_all()
```

Dessa forma cada teste executa em um banco limpo, sem depender dos dados criados por outros testes.

---

## Tecnologias e Ferramentas

```text
- Python 3.12
- FastAPI (Framework web de alta performance)
- SQLAlchemy (ORM para mapeamento do banco)
- PostgreSQL 16 (Banco de dados relacional)
- Docker & Docker Compose (Conteinerização)
- Pytest (Framework de testes automatizados)
```
