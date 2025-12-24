from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

# Junction table for Figure-to-Figure relationships (family tree, etc.)
figure_relationships = Table(
    'figure_relationships',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('figure1_id', Integer, ForeignKey('mythological_figures.id')),
    Column('figure2_id', Integer, ForeignKey('mythological_figures.id')),
    Column('relationship_type', String(50)),  # parent_of, spouse_of, sibling_of
    Column('notes', Text)
)

# Junction table for Figure-Etymology
figure_etymologies = Table(
    'figure_etymologies',
    Base.metadata,
    Column('figure_id', Integer, ForeignKey('mythological_figures.id'), primary_key=True),
    Column('etymology_id', Integer, ForeignKey('etymologies.id'), primary_key=True)
)

# Junction table for Etymology-Cognate
etymology_cognates = Table(
    'etymology_cognates',
    Base.metadata,
    Column('etymology_id', Integer, ForeignKey('etymologies.id'), primary_key=True),
    Column('cognate_id', Integer, ForeignKey('english_cognates.id'), primary_key=True),
    Column('derivation_path', String(500))  # Greek → Latin → English
)


class MythologicalFigure(Base):
    __tablename__ = 'mythological_figures'
    
    id = Column(Integer, primary_key=True, index=True)
    greek_name = Column(String(100))  # Ἀφροδίτη
    latin_name = Column(String(100))  # Venus
    english_name = Column(String(100), index=True)  # Aphrodite
    figure_type = Column(String(50))  # Olympian, Titan, Primordial, Hero, Creature
    domain = Column(String(200))  # love, beauty, passion
    origin_story = Column(Text)
    image_url = Column(String(500))
    pronunciation_audio_url = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    etymologies = relationship("Etymology", secondary=figure_etymologies, back_populates="figures")
    fun_facts = relationship("FunFact", back_populates="figure")


class Etymology(Base):
    __tablename__ = 'etymologies'
    
    id = Column(Integer, primary_key=True, index=True)
    greek_root = Column(String(100))  # ἔρως
    root_meaning = Column(String(200))  # desire, love
    phonetic_evolution = Column(Text)  # how pronunciation changed
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    figures = relationship("MythologicalFigure", secondary=figure_etymologies, back_populates="etymologies")
    cognates = relationship("EnglishCognate", secondary=etymology_cognates, back_populates="etymologies")


class EnglishCognate(Base):
    __tablename__ = 'english_cognates'
    
    id = Column(Integer, primary_key=True, index=True)
    word = Column(String(100), index=True)  # aphrodisiac
    definition = Column(Text)
    part_of_speech = Column(String(50))  # noun, verb, adjective
    usage_frequency = Column(String(20))  # common, uncommon, rare, technical
    example_sentence = Column(Text)
    pronunciation_audio_url = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    etymologies = relationship("Etymology", secondary=etymology_cognates, back_populates="cognates")


class FunFact(Base):
    __tablename__ = 'fun_facts'
    
    id = Column(Integer, primary_key=True, index=True)
    figure_id = Column(Integer, ForeignKey('mythological_figures.id'))
    content = Column(Text)  # The anecdote or fact
    source_citation = Column(String(500))
    surprise_factor = Column(Integer)  # 1-5 rating
    category = Column(String(50))  # linguistic, historical, cultural, trivia
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    figure = relationship("MythologicalFigure", back_populates="fun_facts")
