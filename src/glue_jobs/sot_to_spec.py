import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext

from pyspark.sql.functions import col, sum, avg, count


# 2. PARAMETROS
args = getResolvedOptions(sys.argv, ['ENV', 'BUCKET'])

env = args['ENV']
bucket = args['BUCKET']

# 3. SPARK
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# 4. CAMINHOS
source = f"s3://{bucket}/SOT/datasus/internacoes/"
destination = f"s3://{bucket}/SPEC/datasus/internacoes/"

# 5. LEITURA
df = spark.read.parquet(source)


# 6. AGREGACOES (METRICAS)
df_spec = df.groupBy("uf_zi").agg(
    sum("val_tot").alias("total_custo"),
    avg("idade").alias("idade_media"),
    count("*").alias("qtd_internacoes")
)

# 7. ESCRITA
df_spec.write \
    .mode("overwrite") \
    .parquet(destination)

# 8. LOG
print(f"{env} | SOT to SPEC completed")