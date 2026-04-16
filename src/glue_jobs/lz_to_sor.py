import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext

from pyspark.sql.functions import col
from pyspark.sql.types import IntegerType, DoubleType


# 1. PARAMETROS

args = getResolvedOptions(sys.argv, ['ENV', 'BUCKET'])
env = args['ENV']
bucket = args['BUCKET']


# 2. SPARK

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session


# 3. CAMINHOS (ATUALIZADO)

source = f"s3://{bucket}/LZ/movies/"
destination = f"s3://{bucket}/SOR/movies/"

# 4. LEITURA

df = spark.read.parquet(source)


# 5. PADRONIZAÇÃO

df = df.toDF(*[c.lower() for c in df.columns])


# 6. TRATAMENTO DE TIPOS

if "movie_id" in df.columns:
    df = df.withColumn("movie_id", col("movie_id").cast(IntegerType()))

if "release_year" in df.columns:
    df = df.withColumn("release_year", col("release_year").cast(IntegerType()))

if "runtime_min" in df.columns:
    df = df.withColumn("runtime_min", col("runtime_min").cast(IntegerType()))

if "vote_average" in df.columns:
    df = df.withColumn("vote_average", col("vote_average").cast(DoubleType()))


# 7. LIMPEZA

df = df.dropna(subset=["movie_id", "title"])


# 8. ESCRITA

df.write \
    .mode("overwrite") \
    .parquet(destination)


# 9. LOG

print(f"{env} | LZ to SOR movies completed")