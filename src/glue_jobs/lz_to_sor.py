import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext

args = getResolvedOptions(sys.argv, ['ENV', 'BUCKET'])

env = args['ENV']
bucket = args['BUCKET']

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Caminhos
source = f"s3://{bucket}/LZ/earaujo-terraform-state"
destination = f"s3://{bucket}/SOR/..................parquet"

# Leitura
df = spark.read.json(source)

# Transformação
df = df.dropDuplicates()

# Escrita
df.write.mode("overwrite").parquet(destination)

print(f"{env} | LZ → SOR finalizado")