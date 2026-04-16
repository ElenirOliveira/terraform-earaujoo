import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext

from pyspark.sql.functions import col, count, avg, round


# 1. PARAMETROS

args = getResolvedOptions(sys.argv, ['ENV', 'BUCKET'])
env = args['ENV']
bucket = args['BUCKET']


# 2. SPARK

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session


# 3. CAMINHOS

source = f"s3://{bucket}/SOT/movies/"
destination = f"s3://{bucket}/SPEC/movies/"


# 4. LEITURA

df = spark.read.parquet(source)

# 5. AGREGAÇÕES (INSIGHTS)

# análise por gênero
df_spec = df.groupBy("genre").agg(
    count("*").alias("qtd_filmes"),
    round(avg("runtime_min"), 2).alias("duracao_media"),
    round(avg("title_length"), 2).alias("titulo_medio")
)


# 6. ESCRITA

df_spec.write \
    .mode("overwrite") \
    .parquet(destination)


# 7. LOG
# =
print(f"{env} | SOT to SPEC movies completed")