import json
import boto3
import os

def lambda_handler(event, context):
    bucket_name = os.environ.get("BUCKET_NAME")

    if not bucket_name:
        raise Exception("Variável de ambiente BUCKET_NAME não definida")

    s3 = boto3.client("s3")

    input_key = "LZ/movies/global_movies.csv"

    try:
        # apenas valida se o arquivo existe
        s3.head_object(
            Bucket=bucket_name,
            Key=input_key
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "CSV disponível na LZ",
                "path": input_key
            })
        }

    except Exception as e:
        raise Exception(f"Erro ao acessar CSV: {str(e)}")