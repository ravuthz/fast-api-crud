## Develop

```bash

python -m venv venv

# macOS/Linux
source venv/bin/activate
# window
venv\Scripts\activate.bat   

pip install fastapi uvicorn sqlalchemy pydantic[email] alembic
pip install python-jose[cryptography] python-multipart
pip install "pydantic-settings>=2.0.0"
# pip install --upgrade bcrypt passlib bcrypt passlib[bcrypt] 
pip install bcrypt==3.2.0 passlib
# pip uninstall bcrypt passlib

pip freeze > requirements.txt

pip install pytest httpx

pytest -v

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


curl -X POST http://127.0.0.1:8000/users -H "Content-Type: application/json" -d '{"email": "test100@gm.com", "username": "test100", "password": "test123123"}'


```