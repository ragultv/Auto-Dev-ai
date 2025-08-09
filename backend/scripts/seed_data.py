#!/usr/bin/env python3
"""
Script to seed the database with initial data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, create_tables
from app.models.project import Project
from app.models.dataset import Dataset

def seed_data():
    """Seed the database with initial data"""
    db = SessionLocal()
    
    try:
        # Create tables
        create_tables()
        
        # Seed projects
        projects = [
            Project(
                prompt="Create a machine learning model for sentiment analysis",
                status="completed"
            ),
            Project(
                prompt="Build a REST API for a todo application",
                status="in_progress"
            )
        ]
        
        for project in projects:
            db.add(project)
        
        # Seed datasets
        datasets = [
            Dataset(
                name="sentiment_analysis_data",
                description="Dataset for sentiment analysis",
                file_path="/data/sentiment.csv"
            ),
            Dataset(
                name="todo_data",
                description="Dataset for todo application",
                file_path="/data/todos.json"
            )
        ]
        
        for dataset in datasets:
            db.add(dataset)
        
        db.commit()
        print("Data seeded successfully!")
        
    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data() 