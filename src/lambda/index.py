
# 1. IMPORTS

import json
import boto3
import os
import tempfile

import pandas as pd
from pysus.online_data.SIH import download


# 2. HANDLER PRINCIPAL

def lambda_handler(event, context):

   
    # 3. CONFIGURAÇÃO
  
    bucket_name = os.environ.get("BUCKET_NAME")

    # Cliente S3
    s3 = boto3.client("s3")

    
    # 4. DOWNLOAD DO DATASUS (PARQUET DIRETO )
   
    # Isso já baixa e salva parquet automaticamente no ambiente
    files = download(
        states="SP",
        years=2020,
        months=1,
        groups="RD"
    )

    # Caminho do arquivo gerado pelo pysus
    local_parquet_path = "/tmp/RDSP2001.parquet"

    # Copiar do diretório padrão para /tmp (Lambda só escreve aqui)
    original_path = files[0].path

    df = pd.read_parquet(original_path)


    # 5. SALVAR TEMPORÁRIO (LAMBDA)
  
    df.to_parquet(local_parquet_path, index=False)

   
    # 6. DEFINIR CAMINHO NO S3 (LZ)

    file_name = "LZ/datasus/internacoes/year=2020/month=01/RDSP2001.parquet"


    # 7. UPLOAD PARA S3
 
    with open(local_parquet_path, "rb") as f:
        s3.upload_fileobj(f, bucket_name, file_name)

    
    # 8. RETORNO
   
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Parquet salvo na LZ com sucesso 🚀",
            "bucket": bucket_name,
            "path": file_name
        })
    }