"""
Database seeding script for mythological figures.
Populates the database with all 44 figures from figure_prompts.py
"""
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app import models
from app.image_gen.figure_prompts import FIGURE_PROMPTS, get_figure_relationships

def seed_figures(db: Session):
    """Seed all mythological figures from FIGURE_PROMPTS."""
    
    # Check if already seeded
    existing_count = db.query(models.MythologicalFigure).count()
    if existing_count > 0:
        print(f"Database already contains {existing_count} figures. Skipping seed.")
        return existing_count
    
    print(f"Seeding {len(FIGURE_PROMPTS)} mythological figures...")
    
    figures_created = 0
    for greek_name, data in FIGURE_PROMPTS.items():
        # Convert greek name to english name (simplified)
        english_name = greek_name
        
        # Create figure
        figure = models.MythologicalFigure(
            greek_name=greek_name,
            english_name=english_name,
            figure_type=data["figure_type"],
            description=f"{english_name}, {data['figure_type'].lower()} from Greek mythology",
            role="",  # Could be populated from prompts
            domain="",  # Could be populated from prompts
            symbols="",  # Could be extracted from prompts
            image_url=None  # Will be populated when images are generated
        )
        
        db.add(figure)
        figures_created += 1
    
    # Add relationships
    relationships = get_figure_relationships()
    db.commit()
    
    # Now add parent/child relationships
    print("Adding family relationships...")
    for greek_name, data in FIGURE_PROMPTS.items():
        figure = db.query(models.MythologicalFigure).filter(
            models.MythologicalFigure.greek_name == greek_name
        ).first()
        
        if figure and greek_name in relationships:
            rel_data = relationships[greek_name]
            
            # Set parents
            if "parents" in rel_data:
                for parent_name in rel_data["parents"]:
                    parent = db.query(models.MythologicalFigure).filter(
                        models.MythologicalFigure.greek_name == parent_name
                    ).first()
                    if parent:
                        if not figure.father_id and rel_data["parents"].index(parent_name) == 0:
                            figure.father_id = parent.id
                        elif not figure.mother_id:
                            figure.mother_id = parent.id
    
    db.commit()
    print(f"✓ Seeded {figures_created} figures with relationships")
    return figures_created

def main():
    """Run the seeding script."""
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Create session and seed
    db = SessionLocal()
    try:
        count = seed_figures(db)
        print(f"\n{'='*50}")
        print(f"Database seeding complete!")
        print(f"Total figures: {count}")
        print(f"{'='*50}\n")
    finally:
        db.close()

if __name__ == "__main__":
    main()
