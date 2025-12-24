from sqlalchemy.orm import Session
from app import models, schemas
from typing import List, Optional


# MythologicalFigure CRUD
def get_figure(db: Session, figure_id: int) -> Optional[models.MythologicalFigure]:
    return db.query(models.MythologicalFigure).filter(models.MythologicalFigure.id == figure_id).first()


def get_figure_by_name(db: Session, english_name: str) -> Optional[models.MythologicalFigure]:
    return db.query(models.MythologicalFigure).filter(models.MythologicalFigure.english_name == english_name).first()


def get_figures(db: Session, skip: int = 0, limit: int = 100) -> List[models.MythologicalFigure]:
    return db.query(models.MythologicalFigure).offset(skip).limit(limit).all()


def get_figures_by_type(db: Session, figure_type: str) -> List[models.MythologicalFigure]:
    return db.query(models.MythologicalFigure).filter(models.MythologicalFigure.figure_type == figure_type).all()


def create_figure(db: Session, figure: schemas.FigureCreate) -> models.MythologicalFigure:
    db_figure = models.MythologicalFigure(**figure.model_dump())
    db.add(db_figure)
    db.commit()
    db.refresh(db_figure)
    return db_figure


def update_figure(db: Session, figure_id: int, figure: schemas.FigureUpdate) -> Optional[models.MythologicalFigure]:
    db_figure = get_figure(db, figure_id)
    if db_figure:
        update_data = figure.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_figure, key, value)
        db.commit()
        db.refresh(db_figure)
    return db_figure


def delete_figure(db: Session, figure_id: int) -> bool:
    db_figure = get_figure(db, figure_id)
    if db_figure:
        db.delete(db_figure)
        db.commit()
        return True
    return False


# Etymology CRUD
def get_etymology(db: Session, etymology_id: int) -> Optional[models.Etymology]:
    return db.query(models.Etymology).filter(models.Etymology.id == etymology_id).first()


def get_etymologies(db: Session, skip: int = 0, limit: int = 100) -> List[models.Etymology]:
    return db.query(models.Etymology).offset(skip).limit(limit).all()


def create_etymology(db: Session, etymology: schemas.EtymologyCreate) -> models.Etymology:
    db_etymology = models.Etymology(**etymology.model_dump())
    db.add(db_etymology)
    db.commit()
    db.refresh(db_etymology)
    return db_etymology


# EnglishCognate CRUD
def get_cognate(db: Session, cognate_id: int) -> Optional[models.EnglishCognate]:
    return db.query(models.EnglishCognate).filter(models.EnglishCognate.id == cognate_id).first()


def get_cognate_by_word(db: Session, word: str) -> Optional[models.EnglishCognate]:
    return db.query(models.EnglishCognate).filter(models.EnglishCognate.word == word).first()


def get_cognates(db: Session, skip: int = 0, limit: int = 100) -> List[models.EnglishCognate]:
    return db.query(models.EnglishCognate).offset(skip).limit(limit).all()


def create_cognate(db: Session, cognate: schemas.CognateCreate) -> models.EnglishCognate:
    db_cognate = models.EnglishCognate(**cognate.model_dump())
    db.add(db_cognate)
    db.commit()
    db.refresh(db_cognate)
    return db_cognate


# FunFact CRUD
def get_fun_facts_for_figure(db: Session, figure_id: int) -> List[models.FunFact]:
    return db.query(models.FunFact).filter(models.FunFact.figure_id == figure_id).all()


def create_fun_fact(db: Session, fun_fact: schemas.FunFactCreate) -> models.FunFact:
    db_fun_fact = models.FunFact(**fun_fact.model_dump())
    db.add(db_fun_fact)
    db.commit()
    db.refresh(db_fun_fact)
    return db_fun_fact


# Relationship helpers
def link_figure_etymology(db: Session, figure_id: int, etymology_id: int):
    """Link a figure to an etymology."""
    figure = get_figure(db, figure_id)
    etymology = get_etymology(db, etymology_id)
    if figure and etymology:
        figure.etymologies.append(etymology)
        db.commit()


def link_etymology_cognate(db: Session, etymology_id: int, cognate_id: int, derivation_path: str = None):
    """Link an etymology to a cognate."""
    etymology = get_etymology(db, etymology_id)
    cognate = get_cognate(db, cognate_id)
    if etymology and cognate:
        etymology.cognates.append(cognate)
        db.commit()
