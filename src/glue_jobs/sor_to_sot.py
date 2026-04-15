
import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext

from pyspark.sql.functions import col, length

# PARAMETROS
args = getResolvedOptions(sys.argv, ['ENV', 'BUCKET'])
env = args['ENV']
bucket = args['BUCKET']

# SPARK
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# CAMINHOS
source = f"s3://{bucket}/SOR/test/"
destination = f"s3://{bucket}/SOT/test/"

# LEITURA
df = spark.read.parquet(source)

# REGRAS DE NEGOCIO
df = df.withColumn("title_length", length(col("title")))
df = df.withColumn("body_length", length(col("body")))

# FILTRO
df = df.filter(col("title").isNotNull())

# ESCRITA
df.write \
    .mode("overwrite") \
    .parquet(destination)

print(f"{env} | SOR to SOT completed")