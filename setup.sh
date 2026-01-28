#! /bin/bash
function create_env(){
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
}

echo "{}" > data.json

echo "go to http://127.0.0.1:8000/index.html to view the site"
uvicorn book_manager:app --reload
