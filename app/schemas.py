from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# MythologicalFigure schemas
class FigureBase(BaseModel):
    greek_name: Optional[str] = None
    latin_name: Optional[str] = None
    english_name: str
    figure_type: Optional[str] = None
    domain: Optional[str] = None
    origin_story: Optional[str] = None
    image_url: Optional[str] = None
    pronunciation_audio_url: Optional[str] = None


class FigureCreate(FigureBase):
    pass


class FigureUpdate(BaseModel):
    greek_name: Optional[str] = None
    latin_name: Optional[str] = None
    english_name: Optional[str] = None
    figure_type: Optional[str] = None
    domain: Optional[str] = None
    origin_story: Optional[str] = None
    image_url: Optional[str] = None
    pronunciation_audio_url: Optional[str] = None


class Figure(FigureBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Etymology schemas
class EtymologyBase(BaseModel):
    greek_root: str
    root_meaning: str
    phonetic_evolution: Optional[str] = None
    notes: Optional[str] = None


class EtymologyCreate(EtymologyBase):
    pass


class Etymology(EtymologyBase):
    id: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# EnglishCognate schemas
class CognateBase(BaseModel):
    word: str
    definition: Optional[str] = None
    part_of_speech: Optional[str] = None
    usage_frequency: Optional[str] = None
    example_sentence: Optional[str] = None
    pronunciation_audio_url: Optional[str] = None


class CognateCreate(CognateBase):
    pass


class Cognate(CognateBase):
    id: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# FunFact schemas
class FunFactBase(BaseModel):
    content: str
    source_citation: Optional[str] = None
    surprise_factor: Optional[int] = None
    category: Optional[str] = None


class FunFactCreate(FunFactBase):
    figure_id: int


class FunFact(FunFactBase):
    id: int
    figure_id: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Extended schemas with relationships
class FigureWithRelations(Figure):
    etymologies: List[Etymology] = []
    fun_facts: List[FunFact] = []


class EtymologyWithCognates(Etymology):
    cognates: List[Cognate] = []
