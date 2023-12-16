from test import get_similar_chunks

query = "Lỗi INT3170 xử lý thế nào?"
chunks = get_similar_chunks(query=query.lower())
i = 1
for chunk in chunks:
 #if chunk[1]>30:
   print("      Score:",chunk[1])
   print("source:",chunk[0].metadata['source'],"page",chunk[0].metadata['page'])
   print(chunk[0].page_content)
   #print(chunk[0].page_content)
   #with open("result.txt",'a',encoding='utf-8') as f:
   # f.write(str(i))
   # 
   # f.write(". Score:")
   # f.write(str(chunk[1]))
   # f.write("\n")
   # f.writelines(str(chunk[0].metadata['source']))
   # f.writelines(str(chunk[0].metadata['page']))
   # #f.write("source:",chunk[0].metadata['source'],"page",chunk[0].metadata['page'])
   # f.write(str(chunk[0].page_content))
   # f.write("\n-------------------------------------------\n")
   i = i+1