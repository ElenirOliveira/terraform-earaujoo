import json
import boto3
import os
import pandas as pd
from io import BytesIO

def lambda_handler(event, context):

   
    # 1. CONFIGURAÇÃO
  
    bucket_name = os.environ.get("BUCKET_NAME")

    if not bucket_name:
        raise Exception("Variável de ambiente BUCKET_NAME não definida")

    s3 = boto3.client("s3")

    input_key = "LZ/movies/global_movies.csv"
    output_key = "LZ/movies/global_movies.parquet"

    t
        # 2. LER CSV DO S3
       
        response = s3.get_object(
            Bucket=bucket_name,
            Key=input_key
        )

        df = pd.read_csv(response['Body'])

      
        # 3. PADRONIZAÇÃO (MELHORIA )
     
        df.columns = [c.lower() for c in df.columns]

        # 4. CONVERTER PARA PARQUET
      
        buffer = BytesIO()
        df.to_parquet(buffer, index=False)

        # 5. SALVAR NO S3
       
        s3.put_object(
            Bucket=bucket_name,
            Key=output_key,
            Body=buffer.getvalue()
        )

   
        # 6. RETORNO
      
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "CSV convertido para Parquet com sucesso",
                "input": input_key,
                "output": output_key,
                "linhas": len(df),
                "colunas": len(df.columns)
            })
        }

    except Exception as e:
        raise Exception(f"Erro no processamento: {str(e)}")