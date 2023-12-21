from hybrid_retrive import retrive_Hybrid
from semantic_retrive import retrive_Semantic
from keyword_retrive import retrive_Keyword


query = "error int3170"

print("Semantic Result: ")
dict1 = retrive_Semantic(query=query)
print(dict1)

print("Keyword Result:")
dict2 = retrive_Keyword(query=query)
print(dict2)

print("Hybrid Result:")
dict3 = retrive_Hybrid(query=query)
print(dict3)