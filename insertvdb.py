import os
import json
from pymongo import MongoClient
from langchain_openai import OpenAIEmbeddings
import openai
import pymongo

# Set up OpenAI API key
os.environ["OPENAI_API_KEY"] = ""
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI embeddings
embeddings = OpenAIEmbeddings()

# Connect to MongoDB Atlas
MONGO_URL="mongodb+srv://sriramg:Coc54694@cluster0.uwofdgc.mongodb.net/"
MONGO_DBNAME = "Vector_Data"
COLLECTION ="datacollections"

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DBNAME]
vec_collection = db[COLLECTION]

def load_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return None

def embed_data(tenants_data):
    for item in tenants_data:
        if ("accountName" in item['dimensions'].keys() and
            "accountNumber" in item['entity'].keys() and
            "accountId" in item['entity'].keys() and
            "campaign" in item['entity'].keys() and
            "noaaRegion" in item['entity'].keys() and
            "campaignId" in item['entity'].keys() and
            "customerId" in item['entity'].keys() and
            "cost" in item['metrics'].keys() and 
            "impressions" in item['metrics'].keys() and
            "date" in item['entity'].keys()):
            item['metrics']['cost'] = str(item['metrics']['cost'])
            item['metrics']['impressions'] = str(item['metrics']['impressions'])
            item['entity']['date']= str(item['entity']['date'])
            accountName=item['dimensions']['accountName']
            accountNumber=item['entity']['accountNumber']
            accountId=item['entity']['accountId']
            campaign=item['entity']['campaign']
            customerId=item['entity']['customerId']
            noaaRegion=item['entity']['noaaRegion']
            campaignId=item['entity']['campaignId']
            cost= item['metrics']['cost']
            impressions=item['metrics']['impressions']
            date=item['entity']['date']
            metrics_name=embeddings.embed_query(accountName)
            metrics_number=embeddings.embed_query(accountNumber)
            metrics_id=embeddings.embed_query(accountId)
            metrics_campaign=embeddings.embed_query(campaign)
            metrics_region=embeddings.embed_query(noaaRegion)
            metrics_campaignid=embeddings.embed_query(campaignId)
            metrics_customerId=embeddings.embed_query(customerId)
            metrics_cost=embeddings.embed_query(cost)
            metrics_impressions=embeddings.embed_query(impressions)
            metrics_date=embeddings.embed_query(date)
            vec_collection.insert_many([{"accountName": accountName,"accountNumber":accountNumber,"accountId":accountId,"campaign":campaign,"noaaRegion":noaaRegion,"campaignId":campaignId,"cost":cost,"impressions":impressions,"date":date,"metrics_name":metrics_name,"metrics_number":metrics_number,"metrics_id":metrics_id,"metrics_campaign":metrics_campaign,"metrics_region":metrics_region,"metrics_campaignid":metrics_campaignid,"metrics_customerId":metrics_customerId,"metrics_cost":metrics_cost,"metrics_impressions":metrics_impressions,"metrics_date":metrics_date}])
            print('success')

        else:
            print('fail')

            
if __name__ == "__main__":
    tenants_data = load_data("C:/Sriram.J/Sysdatasource/haller Enterprises.DataMsAdsCampaignPerformanceTransformed.json")
    if tenants_data:
        embed_data(tenants_data)