source venv/bin/activate
. ~/.try-vector-db.env.sh

python -m unittest VectorDbPgvector.py
python -m unittest EmbeddingsSimple.py
