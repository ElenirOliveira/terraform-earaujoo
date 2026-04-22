import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext

from pyspark.sql.functions import col, count, avg, round


args = getResolvedOptions(sys.argv, ['ENV', 'BUCKET'])
env = args['ENV']
bucket = args['BUCKET']


sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session


source = f"s3://{bucket}/SOT/movies/"
destination = f"s3://{bucket}/SPEC/movies/"


df = spark.read.parquet(source)


# padronização de segurança
df = df.toDF(*[c.lower() for c in df.columns])


# remover dados inválidos antes de agregar
df = df.dropna(subset=["genero", "duracao_minutos", "tamanho_titulo"])


# agregação
df_spec = df.groupBy("genero").agg(
    count("*").alias("quantidade_filmes"),
    round(avg("duracao_minutos"), 2).alias("duracao_media"),
    round(avg("tamanho_titulo"), 2).alias("tamanho_medio_titulo")
)


# ordenar (melhoria de consumo)
df_spec = df_spec.orderBy(col("quantidade_filmes").desc())


# escrita
df_spec.write \
    .mode("overwrite") \
    .parquet(destination)