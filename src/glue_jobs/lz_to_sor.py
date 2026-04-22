import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext

from pyspark.sql.functions import col

args = getResolvedOptions(sys.argv, ['ENV', 'BUCKET'])
env = args['ENV']
bucket = args['BUCKET']

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

source = f"s3://{bucket}/LZ/movies/"
destination = f"s3://{bucket}/SOR/movies/"

# LER CSV (CORRETO PARA LZ)
df = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv(source)

# padronizar colunas
df = df.toDF(*[c.lower() for c in df.columns])

# remover linhas sem título
df = df.dropna(subset=["title"])

# cast correto
df = df.withColumn("release_year", col("release_year").cast("int"))
df = df.withColumn("runtime_min", col("runtime_min").cast("int"))

# salvar em parquet (SOR)
df.write \
    .mode("overwrite") \
    .parquet(destination)

print(f"{env} | LZ to SOR movies completed")