source venv/bin/activate
source ~/.try-vector-db.env.sh

#DEBUG_LEVEL=WARN python run-regext.py "What may be a good travel plan to get away from Vancouver?"
DEBUG_LEVEL=WARN python run-regint.py "What flight can fly me from Vancouver to Seoul?"
DEBUG_LEVEL=WARN python run-regint.py "What may be a good travel plan to get away from Vancouver?"