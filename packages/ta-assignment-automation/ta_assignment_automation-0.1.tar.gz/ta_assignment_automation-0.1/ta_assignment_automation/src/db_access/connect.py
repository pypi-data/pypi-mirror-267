import sys, os

from sqlalchemy import create_engine, text



# Get the current working directory
current_path = os.path.dirname(os.path.abspath(__file__))

# Add the parent directory to sys.path
parent_path = os.path.join(current_path, '..')
sys.path.append(parent_path)

from data.db_config import db_url

# DB CONNECTION CODE BELOW

engine = create_engine(db_url, echo=True)

with engine.connect() as conn:
    result = conn.execute(text('select "HELLO"'))
    print(result.all())