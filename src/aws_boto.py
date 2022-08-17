from operator import index
from textwrap import indent
import boto3
from sqlalchemy import create_engine
import pandas as pd

S3_BUCKET_NAME = 'my-bucket-johnlewis'
HOST = 'johnlewis-db.c1rptlndtetd.us-east-1.rds.amazonaws.com'
DBAPI = 'psycopg2'
USER = 'postgres'
PASSWORD = 'Pratiksha'
PORT = 5432
DATABASE = 'postgres'
DATABASE_TYPE = 'postgresql'

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
        s3_client = boto3.client('s3')
        try:
            s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=object_name)
        except:
            s3_client.upload_file(file_name, S3_BUCKET_NAME, object_name)
        
        file_url_to_upload = f's3://{S3_BUCKET_NAME}/{object_name}'
        return file_url_to_upload  

    def save_data_RDS(self,Data_list):
      engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
      print(f"Connecting to Database : {DATABASE_TYPE}")
      engine.connect()
      print("Connection established")
      Data_list.to_sql('product_informations', engine, index=True)
      print("Data Table is created !!")
      sql_query = f"SELECT * FROM product_informations"
      print("Fetching the data")
      fetched_data = engine.execute(sql_query).fetchall()
      print("Data fetching done !!")
      print(fetched_data)