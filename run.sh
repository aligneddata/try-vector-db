source venv/bin/activate
source ~/.try-vector-db.env.sh

python -m unittest RagExtFree.py    
DEBUG_LEVEL=WARN python run-regext.py "What may be a good travel plan to get away from Vancouver?"