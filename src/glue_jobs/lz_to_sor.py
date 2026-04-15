import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext

from pyspark.sql.functions import col

# PARAMETROS
args = getResolvedOptions(sys.argv, ['ENV', 'BUCKET'])
env = args['ENV']
bucket = args['BUCKET']

# SPARK
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# CAMINHOS
source = f"s3://{bucket}/LZ/test/"
destination = f"s3://{bucket}/SOR/test/"

# LEITURA
df = spark.read.parquet(source)

# PADRONIZAÇÃO
df = df.toDF(*[c.lower() for c in df.columns])

# TIPOS
df = df.withColumn("userid", col("userid").cast("int"))
df = df.withColumn("id", col("id").cast("int"))

# REMOVER NULOS
df = df.dropna(subset=["userid", "id"])

# ESCRITA
df.write \
    .mode("overwrite") \
    .parquet(destination)

print(f"{env} | LZ to SOR completed")