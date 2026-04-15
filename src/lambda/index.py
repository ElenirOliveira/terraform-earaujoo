import json
import boto3
import os
import requests
import pandas as pd
from io import BytesIO

def lambda_handler(event, context):

    # =========================================================
    # 1. CONFIGURAÇÃO
    # =========================================================
    bucket_name = os.environ.get("BUCKET_NAME")
    s3 = boto3.client("s3")

    url = "https://jsonplaceholder.typicode.com/posts"

    # =========================================================
    # 2. CONSUMO DA API
    # =========================================================
    try:
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            raise Exception(f"Erro HTTP: {response.status_code}")

        data = response.json()

    except Exception as e:
        raise Exception(f"Erro ao consumir API: {str(e)}")

    # =========================================================
    # 3. CONVERTER PARA PARQUET
    # =========================================================
    df = pd.DataFrame(data)

    buffer = BytesIO()
    df.to_parquet(buffer, index=False)

    # =========================================================
    # 4. SALVAR NO S3 (LZ)
    # =========================================================
    file_name = "LZ/test/posts.parquet"

    s3.put_object(
        Bucket=bucket_name,
        Key=file_name,
        Body=buffer.getvalue()
    )

    # =========================================================
    # 5. RETORNO
    # =========================================================
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Dados salvos com sucesso",
            "path": file_name
        })
    }