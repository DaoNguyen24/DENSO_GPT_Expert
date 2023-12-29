import weaviate

client = weaviate.Client("http://localhost:8081")
print("weaviatedb is ready: ",client.is_ready())

#response = client.query.get("Denso_Document", ['source','page','content']).do()
User_query = "Làm thế nào để Sửa lỗi int3170 LNCT800"

def keyword_retrive(client=client,query=User_query):

    response = (
        client.query
        .get("Denso_Document",properties=['source','page','content',"machine_name","code","line","description"])
        .with_bm25(
          query=User_query,
          properties=["machine_name^2",'description',"content","code"]
        )
        .with_additional("score")
        .with_limit(5)
        .do()
    )
    list = []
    for result in response["data"]["Get"]['Denso_Document']:
        list.append({
            'source' :result["source"],
            'page' :result["page"],
            'type': '1_kw',
            'score': result["_additional"]["score"]
        })
    return list
    
    
def hybrid_retrive(client = client, query = User_query):
    response2 = (
        client.query
        .get("Denso_Document", properties=['source','page','content',"machine_name","code","line","description"])
        .with_hybrid(
            query=User_query,
            alpha= 0.25,
            properties=["machine_name^2",'description',"content","code"]
        )
        .with_additional(["score"])
        .with_limit(5)
        .do()
    )
    list = []
    for result in response2["data"]["Get"]['Denso_Document']:
        list.append({
            'source' :result["source"],
            'page' :result["page"],
            'type': '2_hb',
            'score': result["_additional"]["score"]
        })
    return list

def semantic_retrive(client = client, query = User_query):
    response3 = (
        client.query
        .get("Denso_Document", properties=['source','page','content',"machine_name","code","line","description"])
        .with_near_text({
            "concepts": User_query
        })
        .with_limit(5)
        .with_additional(["certainty"])
        .do()
    )
    list = []
    for result in response3["data"]["Get"]['Denso_Document']:
        list.append({
            'source' :result["source"],
            'page' :result["page"],
            'type': '3_sm',
            'score': result["_additional"]["certainty"]
        })
    return list

responses_list = keyword_retrive() + hybrid_retrive()+semantic_retrive()


def get_4_page(list_of_responses):
    import pandas as pd
    df = pd.DataFrame(list_of_responses)
    df['value_count']=df.groupby(["source","page"])['score'].transform('count')
    df["score"]=df["score"].astype(float)
    df['rank'] = df.sort_values('score', ascending=False).groupby("type").cumcount() + 1
    df = df.sort_values(by= ["value_count","rank","type"], ascending=[False,True,True]).drop_duplicates(subset=["source","page"], keep= "first")
    list = df.head(4).to_dict(orient='records')
    return list

#print(get_4_page(responses_list))
import pandas as pd
df = pd.DataFrame(responses_list)

print(df)
print(get_4_page(responses_list))

#print("keyword\n",keyword_retrive())
#print("Hybrid\n",hybrid_retrive())
#print("semantic\n",semantic_retrive())