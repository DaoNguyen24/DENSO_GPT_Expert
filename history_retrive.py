import weaviate
###########HAMM ĐÓNg GÓI
def retrive_history(query):
 client = weaviate.Client("http://localhost:8081")
 print("weaviatedb is ready: ",client.is_ready())
 response = (
        client.query
        .get("Denso_history",properties=["source"])
        .with_bm25(
          query=query,
          properties=["source","year","month","code","machine_name","line","description"]
        )
        .with_limit(1)
        .do()
    )
 #print(response)
 try:
  filepath = response["data"]["Get"]["Denso_history"][0]["source"]
  return filepath
  
 except:
  return "Tôi không tìm thấy lịch sử máy bạn đang cần.Xin hãy thử Câu hỏi khác cụ thể hơn"
 

if __name__ == "__main__":
 query = "Cho tôi lịch sử máy hút bụi"
 response = retrive_history(query=query)
 print(response)