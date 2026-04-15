
import json
import boto3
import requests
import os

def lambda_handler(event, context):

    # ============================
    # CONFIG
    # ============================
    bucket_name = os.environ.get("BUCKET_NAME")

    s3 = boto3.client("s3")

    url = "https://datasus.saude.gov.br/wp-content/ftp/sihsus/202001_/Dados/RDSP2001.dbc"

    # ============================
    # DOWNLOAD
    # ============================
    response = requests.get(url, stream=True, timeout=60)

    if response.status_code != 200:
        raise Exception("Erro ao baixar arquivo")

    file_path = "/tmp/RDSP2001.dbc"

    with open(file_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

    # ============================
    # UPLOAD S3 (LZ)
    # ============================
    s3_key = "LZ/datasus/internacoes/year=2020/month=01/RDSP2001.dbc"

    with open(file_path, "rb") as f:
        s3.upload_fileobj(f, bucket_name, s3_key)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Arquivo enviado para LZ",
            "path": s3_key
        })
    }