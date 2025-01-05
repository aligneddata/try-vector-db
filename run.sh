source venv/bin/activate
source ~/.try-vector-db.env.sh

python run-regext.py "What flight can fly me from Vancouver to Seoul?"
python run-regext.py "Who is the passenger and what is the passenger's travel plan?"

python run-regint.py "What flight can fly me from Vancouver to Seoul?"
python run-regint.py "Who is the passenger and what is the passenger's travel plan?"