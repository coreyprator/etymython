from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
import os

from app import models, schemas, crud
from app.database import engine, get_db, Base
from app.image_test.routes import router as image_test_router

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Etymython API",
    description="Greek mythology etymology learning system",
    version="0.1.0"
)

# Serve static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Include image test router
app.include_router(image_test_router)

@app.get("/app")
def serve_frontend():
    return FileResponse("frontend/index.html")

@app.get("/gallery")
def serve_gallery():
    return FileResponse("frontend/gallery.html")


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


@app.get("/api/v1/figures/{figure_id}/chain")
def get_figure_etymology_chain(figure_id: int, db: Session = Depends(get_db)):
    """Get complete etymology chain: figure → etymologies → cognates"""
    query = text("""
        SELECT 
            f.id as figure_id,
            f.english_name,
            f.greek_name,
            f.figure_type,
            f.domain,
            e.id as etymology_id,
            e.greek_root,
            e.root_meaning,
            c.id as cognate_id,
            c.word as cognate,
            c.definition,
            c.part_of_speech,
            c.example_sentence,
            ec.derivation_path
        FROM mythological_figures f
        LEFT JOIN figure_etymologies fe ON f.id = fe.figure_id
        LEFT JOIN etymologies e ON fe.etymology_id = e.id
        LEFT JOIN etymology_cognates ec ON e.id = ec.etymology_id
        LEFT JOIN english_cognates c ON ec.cognate_id = c.id
        WHERE f.id = :figure_id
        ORDER BY e.id, c.word
    """)
    
    result = db.execute(query, {"figure_id": figure_id}).fetchall()
    
    if not result:
        raise HTTPException(status_code=404, detail="Figure not found")
    
    # Structure the response
    figure_data = {
        "id": result[0].figure_id,
        "english_name": result[0].english_name,
        "greek_name": result[0].greek_name,
        "figure_type": result[0].figure_type,
        "domain": result[0].domain,
        "etymologies": []
    }
    
    etymology_map = {}
    for row in result:
        if row.etymology_id and row.etymology_id not in etymology_map:
            etymology_map[row.etymology_id] = {
                "id": row.etymology_id,
                "greek_root": row.greek_root,
                "root_meaning": row.root_meaning,
                "cognates": []
            }
        
        if row.cognate_id and row.etymology_id:
            etymology_map[row.etymology_id]["cognates"].append({
                "id": row.cognate_id,
                "word": row.cognate,
                "definition": row.definition,
                "part_of_speech": row.part_of_speech,
                "example_sentence": row.example_sentence,
                "derivation_path": row.derivation_path
            })
    
    figure_data["etymologies"] = list(etymology_map.values())
    return figure_data


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


@app.get("/api/v1/relationships")
def get_all_relationships(db: Session = Depends(get_db)):
    """Get all figure relationships for graph edges"""
    query = text("""
        SELECT 
            fr.figure1_id as source_id,
            fr.figure2_id as target_id,
            fr.relationship_type,
            fr.notes,
            f1.english_name as source_name,
            f2.english_name as target_name
        FROM figure_relationships fr
        JOIN mythological_figures f1 ON fr.figure1_id = f1.id
        JOIN mythological_figures f2 ON fr.figure2_id = f2.id
    """)
    result = db.execute(query).fetchall()
    return [
        {
            "source_id": row.source_id,
            "target_id": row.target_id,
            "relationship_type": row.relationship_type,
            "notes": row.notes,
            "source_name": row.source_name,
            "target_name": row.target_name
        }
        for row in result
    ]
