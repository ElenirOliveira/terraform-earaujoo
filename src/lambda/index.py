import json
import requests
import boto3
import os


def lambda_handler(event, context):
    # =========================================================
    # 1. CONFIGURAÇÃO DA API
    # =========================================================
    # Substituir pela API real do seu projeto
    url = "https://api.exemplo.com/dados"

    data_list = []

    # Cliente S3
    s3 = boto3.client("s3")

    # =========================================================
    # 2. BUCKET VINDO DO TERRAFORM (NÃO FIXO)
    # =========================================================
    bucket_name = os.environ.get("BUCKET_NAME")

    # Caminho da Landing Zone
    file_name = "lz/raw_data.json"

    # =========================================================
    # 3. REQUISIÇÃO DA API
    # =========================================================
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        # Ajustar conforme o formato da sua API
        data_list.append(data)

    else:
        return {
            "statusCode": response.status_code,
            "body": json.dumps({"error": "Erro ao buscar dados da API"})
        }

    # =========================================================
    # 4. SALVAR NO S3 (LANDING ZONE)
    # =========================================================
    s3.put_object(
        Bucket=bucket_name,
        Key=file_name,
        Body=json.dumps(data_list)
    )

    # =========================================================
    # 5. RETORNO
    # =========================================================
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Dados salvos no S3 com sucesso",
            "bucket": bucket_name,
            "path": file_name
        })
    }