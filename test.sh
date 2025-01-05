source venv/bin/activate
. ~/.try-vector-db.env.sh

export DEBUG_LEVEL=WARN
python -m unittest VectorDbPgvector.py
python -m unittest EmbeddingsSimple.py
python -m unittest RagIntSmall.py
