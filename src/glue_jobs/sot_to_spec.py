import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext

from pyspark.sql.functions import col, count, avg

# PARAMETROS
args = getResolvedOptions(sys.argv, ['ENV', 'BUCKET'])
env = args['ENV']
bucket = args['BUCKET']

# SPARK
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# CAMINHOS
source = f"s3://{bucket}/SOT/test/"
destination = f"s3://{bucket}/SPEC/test/"

# LEITURA
df = spark.read.parquet(source)

# AGREGAÇÕES
df_spec = df.groupBy("userid").agg(
    count("*").alias("qtd_posts"),
    avg("title_length").alias("media_titulo"),
    avg("body_length").alias("media_conteudo")
)

# ESCRITA
df_spec.write \
    .mode("overwrite") \
    .parquet(destination)

print(f"{env} | SOT to SPEC completed")