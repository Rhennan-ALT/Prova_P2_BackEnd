import os 
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# database

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/dev_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base = declarative_base()

# modelo

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    estoque = Column(Integer, default=0)
    ativo = Column(Boolean, default=True)

# esquemas 

class CriarP(BaseModel):
    nome: str = Field(..., min_length=1)
    preco: float = Field(..., gt=0)
    estoque: int = Field(default=0, ge=0)
    ativo: bool = True

class RespostaP(BaseModel):
    id: int
    nome: str
    preco: float
    estoque: int
    ativo: bool

    class Config:
        from_attributes = True

# api

Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield
    finally:
        db.close()

# pesquisa geral

@app.get("/produtos", response_model=list[RespostaP], status_code=status.HTTP_200_OK)
def listar_p(db: Session = Depends(get_db)):
    return db.query(Produto).all()

# pesquisa por id 

@app.get("/produtos/{produto_id}",response_model=RespostaP, status_code=status.HTTP_200_OK)
def buscar_produto(produto_id: int, db: Session = Depends(get_db)):
    
    produto = (
        db.query(Produto).filter(Produto.id == produto_id).first()
    )

    if not produto:
        raise HTTPException(
            status_code=404,
            detail="Não foi possivel encontrar"
        )

    return produto

# criar um produto

@app.post("/produtos",response_model=RespostaP,status_code=status.HTTP_201_CREATED)
def criar_produto(produto: CriarP, db: Session = Depends(get_db)):

    novo = Produto(**produto.model_dump())

    db.add(novo)
    db.commit()
    db.refresh(novo)

    return novo

# deletar um produto

@app.delete("/produtos/{produto_id}",status_code=status.HTTP_204_NO_CONTENT)
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    
    produto = (
        db.query(Produto).filter(Produto.id == produto_id).first()
    )

    if not produto:
        raise HTTPException(
            status_code=404,
            detail="Não foi possivel encontrar"
        )

    db.delete(produto)
    db.commit()

