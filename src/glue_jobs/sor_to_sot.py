import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from pyspark.sql.functions import col, size

args = getResolvedOptions(sys.argv, ['ENV', 'BUCKET'])

env = args['ENV']
bucket = args['BUCKET']

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

source = f"s3://{bucket}/SOR/.................."
destination = f"s3://{bucket}/SOT/...............parquet"

df = spark.read.parquet(source)

df = df.withColumn("qtd_types", size(col("types")))

df.write.mode("overwrite").parquet(destination)

print(f"{env} | SOR → SOT finalizado")