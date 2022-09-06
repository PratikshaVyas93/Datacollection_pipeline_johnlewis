from operator import index
from textwrap import indent
import boto3
from sqlalchemy import create_engine
import pandas as pd
import sqlalchemy
import os

S3_BUCKET_NAME = "my-bucket-johnlewis"
HOST = "johnlewis-db.c1rptlndtetd.us-east-1.rds.amazonaws.com"
DBAPI = 'psycopg2'
USER = "postgres"
PASSWORD = "Pratiksha"
PORT = 5432
DATABASE = 'postgres'
DATABASE_TYPE = 'postgresql'
ACCESS_KEY= os.environ.get('ACCESS_KEY')
SECRET_KEY =os.environ.get('SECRET_KEY')

class AWSBoto:

    def upload_object_s3(self,file_name,object_name)-> str:
         
        """Function takes an existing images from local directory and upload it on aws s3 bucket 
          
          Parameters
          ----------
          file_name : str
            Name of file to upload on s3 bucket
          object_name : str
            Name of each image to upload on s3 Bucket
            
          Returns
          -------
          file_url_to_upload : str
            return url as string

        """
  
        s3_client = boto3.client('s3',aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
        try:
            print("S3_BUCKET_NAME", S3_BUCKET_NAME)
            print("object_name", object_name)
            s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=object_name)
        except:
            print("upload file on s3")
            s3_client.upload_file(file_name, S3_BUCKET_NAME, object_name)
        
        file_url_to_upload = f's3://{S3_BUCKET_NAME}/{object_name}'
        return file_url_to_upload  

    def save_data_RDS(self,Data_list):
      engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
      print(f"Connecting to Database : {DATABASE_TYPE}")
      engine.connect()
      print("Connection established")
      print("Checking the table product_informations is exists or not !!!")
      if sqlalchemy.inspect(engine).has_table("product_informations"):
        print("Table product_informations is exists")
        sql = sqlalchemy.text("SELECT pi.product_id FROM product_informations as pi")
        result = pd.read_sql_query(sql, engine)
        unique_product_id_list = result['product_id'].tolist()
      print("Checking if records are unique or not")
      for item in Data_list:
        rds_entry = pd.DataFrame([item])
        if item["product_id"] not in unique_product_id_list:
          print("Unique records found")
          print("Inserting unique record/s in product_informations table !!")
          rds_entry.to_sql('product_informations', engine, if_exists = 'append', index=False)
          print("Record/s inserted successfully")
      
