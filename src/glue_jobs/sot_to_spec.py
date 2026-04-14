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

source = f"s3://{bucket}/SOT/.......parquet"
destination = f"s3://{bucket}/SPEC/.................parquet"

df = spark.read.parquet(source)

df = df.select(
    col("name"),
    col("........"),
    col("...........")
)

df.write.mode("overwrite").parquet(destination)

print(f"{env} | SOT → SPEC finalizado")