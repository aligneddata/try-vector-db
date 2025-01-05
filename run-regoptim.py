import sys
from RagOptim import RagOptim

rag = RagOptim()
rag.load_file("z1.txt")

query = sys.argv[1]
print("Question: %s" % query)

answer = rag.generate_answer(query)
print("Answer: %s" % answer)