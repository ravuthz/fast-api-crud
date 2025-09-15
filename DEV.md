## Develop

```bash

python -m venv venv

# macOS/Linux
source venv/bin/activate
# window
venv\Scripts\activate.bat   

pip install fastapi uvicorn sqlalchemy pydantic[email] alembic
pip install python-jose[cryptography] bcrypt passlib[bcrypt] python-multipart
pip install "pydantic-settings>=2.0.0"

pip freeze > requirements.txt
```


## Deploy development server

```bash
# Install dependencies
pip install -r requirements.txt

# Create initial data (first time only)
python setup_initial_data.py

# Start the server
uvicorn main:app --reload

# REST Document
http://localhost:8000/docs

http://localhost:8000/redoc

```