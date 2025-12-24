from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas, crud
from app.database import engine, get_db, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Etymython API",
    description="Greek mythology etymology learning system",
    version="0.1.0"
)


@app.get("/")
def root():
    return {"message": "Welcome to Etymython", "status": "running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


# Figures endpoints
@app.get("/api/v1/figures", response_model=List[schemas.Figure])
def list_figures(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_figures(db, skip=skip, limit=limit)


@app.get("/api/v1/figures/{figure_id}", response_model=schemas.FigureWithRelations)
def get_figure(figure_id: int, db: Session = Depends(get_db)):
    figure = crud.get_figure(db, figure_id)
    if not figure:
        raise HTTPException(status_code=404, detail="Figure not found")
    return figure


@app.post("/api/v1/figures", response_model=schemas.Figure)
def create_figure(figure: schemas.FigureCreate, db: Session = Depends(get_db)):
    existing = crud.get_figure_by_name(db, figure.english_name)
    if existing:
        raise HTTPException(status_code=400, detail="Figure already exists")
    return crud.create_figure(db, figure)


@app.put("/api/v1/figures/{figure_id}", response_model=schemas.Figure)
def update_figure(figure_id: int, figure: schemas.FigureUpdate, db: Session = Depends(get_db)):
    updated = crud.update_figure(db, figure_id, figure)
    if not updated:
        raise HTTPException(status_code=404, detail="Figure not found")
    return updated


@app.delete("/api/v1/figures/{figure_id}")
def delete_figure(figure_id: int, db: Session = Depends(get_db)):
    if not crud.delete_figure(db, figure_id):
        raise HTTPException(status_code=404, detail="Figure not found")
    return {"message": "Figure deleted"}


# Etymologies endpoints
@app.get("/api/v1/etymologies", response_model=List[schemas.Etymology])
def list_etymologies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_etymologies(db, skip=skip, limit=limit)


@app.post("/api/v1/etymologies", response_model=schemas.Etymology)
def create_etymology(etymology: schemas.EtymologyCreate, db: Session = Depends(get_db)):
    return crud.create_etymology(db, etymology)


# Cognates endpoints
@app.get("/api/v1/cognates", response_model=List[schemas.Cognate])
def list_cognates(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_cognates(db, skip=skip, limit=limit)


@app.post("/api/v1/cognates", response_model=schemas.Cognate)
def create_cognate(cognate: schemas.CognateCreate, db: Session = Depends(get_db)):
    existing = crud.get_cognate_by_word(db, cognate.word)
    if existing:
        raise HTTPException(status_code=400, detail="Cognate already exists")
    return crud.create_cognate(db, cognate)


# Fun facts endpoints
@app.get("/api/v1/figures/{figure_id}/facts", response_model=List[schemas.FunFact])
def get_figure_facts(figure_id: int, db: Session = Depends(get_db)):
    figure = crud.get_figure(db, figure_id)
    if not figure:
        raise HTTPException(status_code=404, detail="Figure not found")
    return crud.get_fun_facts_for_figure(db, figure_id)


@app.post("/api/v1/facts", response_model=schemas.FunFact)
def create_fun_fact(fun_fact: schemas.FunFactCreate, db: Session = Depends(get_db)):
    figure = crud.get_figure(db, fun_fact.figure_id)
    if not figure:
        raise HTTPException(status_code=404, detail="Figure not found")
    return crud.create_fun_fact(db, fun_fact)


# Relationship endpoints
@app.post("/api/v1/figures/{figure_id}/etymologies/{etymology_id}")
def link_figure_to_etymology(figure_id: int, etymology_id: int, db: Session = Depends(get_db)):
    crud.link_figure_etymology(db, figure_id, etymology_id)
    return {"message": "Linked successfully"}


@app.post("/api/v1/etymologies/{etymology_id}/cognates/{cognate_id}")
def link_etymology_to_cognate(etymology_id: int, cognate_id: int, db: Session = Depends(get_db)):
    crud.link_etymology_cognate(db, etymology_id, cognate_id)
    return {"message": "Linked successfully"}
