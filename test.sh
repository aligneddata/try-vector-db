source venv/bin/activate
. ~/.try-vector-db.env.sh

export DEBUG_LEVEL=DEBUG

python -m unittest RagIntFast.py
exit 0
python -m unittest VectorDbPgvector.py
python -m unittest EmbeddingsSimple.py
