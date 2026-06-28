import boto3
import os

bucket = "stock-market-data-charan"

s3 = boto3.client("s3")

for file in os.listdir():

    if file.endswith(".csv"):

        s3.upload_file(
            file,
            bucket,
            f"raw/{file}"
        )

        print(f"{file} uploaded")
        