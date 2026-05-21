import os
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Database Connection Configuration
# Replace 'username' and 'password' with your local PostgreSQL credentials
# Change 5400 to 5432
# Replace the postgres URL with a local SQLite file database connection string
DATABASE_URL = "sqlite:///bank_reviews.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. Define Schema Tables
class Bank(Base):
    __tablename__ = 'banks'
    bank_id = Column(Integer, primary_key=True, autoincrement=True)
    bank_name = Column(String(100), unique=True, nullable=False)
    app_name = Column(String(100), nullable=True)

class Review(Base):
    __tablename__ = 'reviews'
    review_id = Column(Integer, primary_key=True, autoincrement=True)
    bank_id = Column(Integer, ForeignKey('banks.bank_id'), nullable=False)
    review_text = Column(String, nullable=True)
    rating = Column(Integer, nullable=False)
    review_date = Column(Date, nullable=False)
    sentiment_label = Column(String(20), nullable=True)
    sentiment_score = Column(Float, nullable=True)
    identified_theme = Column(String(100), nullable=True)
    source = Column(String(50), default='Google Play Store')

def init_db():
    """Creates tables if they don't exist."""
    Base.metadata.create_all(bind=engine)
    print("PostgreSQL Tables created successfully.")

def populate_data(csv_path):
    """Reads processed data from Task 2 and inserts it into PostgreSQL."""
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found. Please run Task 2 first.")
        return

    df = pd.read_csv(csv_path)
    # Ensure dates match correct datetime formatting
    df['review_date'] = pd.to_datetime(df.get('review_date', pd.Timestamp.now())).dt.date
    
    session = SessionLocal()
    try:
        # Extract unique banks and seed the banks table safely
        unique_banks = df['bank_name'].dropna().unique()
        bank_mapping = {}
        
        for b_name in unique_banks:
            bank_obj = session.query(Bank).filter_by(bank_name=b_name).first()
            if not bank_obj:
                bank_obj = Bank(bank_name=b_name, app_name=f"{b_name} Mobile")
                session.add(bank_obj)
                session.commit()
            bank_mapping[b_name] = bank_obj.bank_id

        # Batch insert reviews
        print(f"Inserting {len(df)} records into PostgreSQL...")
        for _, row in df.iterrows():
            review_obj = Review(
                bank_id=bank_mapping[row['bank_name']],
                review_text=row.get('review_text', ''),
                rating=int(row.get('rating', 5)),
                review_date=row['review_date'],
                sentiment_label=row.get('sentiment_label', 'neutral'),
                sentiment_score=float(row.get('sentiment_score', 0.0)),
                identified_theme=row.get('identified_theme', 'General Feedback')
            )
            session.add(review_obj)
        
        session.commit()
        print("Database population complete!")
        
    except Exception as e:
        session.rollback()
        print(f"Database error occurred: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    # Ensure dependencies are satisfied
    # Run: pip install psycopg2-binary sqlalchemy
    init_db()
    populate_data("data/sentiment_thematic_results.csv")