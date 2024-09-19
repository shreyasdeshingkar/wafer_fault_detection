from pymongo.mongo_client import MongoClient
import pandas as pd
import json

#uniform resourse identifier
uri = "mongodb+srv://shreyasdeshingkar:Shreyas123@cluster0.zj3ek.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri)

#create a database name and collection name
DATABASE_NAME="wafer_db"
COLLECTION_NAME="waferfault"


#read data as a dataframe 
df = pd.read_csv('D:\Wafer_fault_detection\notebooks\wafer_23012020_041211.csv')
df = df.drop('Unnamed: 0',axis=1)

#convert the data into json
json_records = json.load(df.T.to_json)


# now dump the data into database
client(DATABASE_NAME)[COLLECTION_NAME] = json_records



# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)