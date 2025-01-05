import sys
from RagIntSmall import RagIntSmall

rag = RagIntSmall()
rag.load_file("z1.txt")

query = sys.argv[1]
print("Question: %s" % query)

answer = rag.generate_answer(query)
print("Answer: %s" % answer)