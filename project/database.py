from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# Define the database schema
Base = declarative_base()

class PLCData(Base):
    __tablename__ = 'plc_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow)  # Auto-generated timestamp
    variable = Column(String, nullable=False)  # Tag name (e.g., "temperature", "pressure")
    value = Column(Float, nullable=False)  # Numerical value


# Database setup
engine = create_engine('sqlite:///plc_data.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


# Function to insert data
def save_value(variable, value):
    """Insert a new PLC data record into the database."""
    new_entry = PLCData(variable=variable, value=value)
    session.add(new_entry)
    session.commit()
    print(f"Saved: {variable} = {value}")


# Function to retrieve all data
def retrieve_all_data():
    """Retrieve all stored data from the database."""
    return session.query(PLCData).all()

