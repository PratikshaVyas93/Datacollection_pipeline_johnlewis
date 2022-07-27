import boto3

S3_BUCKET_NAME = 'johnlewisdpbucket'

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
