
import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext

from pyspark.sql.functions import col
from pyspark.sql.types import IntegerType, DoubleType


# 2. PARAMETROS

args = getResolvedOptions(sys.argv, ['ENV', 'BUCKET'])

env = args['ENV']
bucket = args['BUCKET']

# 3. SPARK

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# 4. CAMINHOS

source = f"s3://{bucket}/SOR/datasus/internacoes/"
destination = f"s3://{bucket}/SOT/datasus/internacoes/"

# 5. LEITURA

df = spark.read.parquet(source)

# 6. REGRAS DE NEGOCIO

# remover registros inválidos
df = df.filter(col("val_tot").isNotNull())

# manter apenas colunas relevantes
df = df.select(
    "uf_zi",
    "ano_cmpt",
    "mes_cmpt",
    "idade",
    "sexo",
    "val_tot",
    "dt_particao"
)

# garantir tipos
df = df.withColumn("idade", col("idade").cast(IntegerType()))
df = df.withColumn("val_tot", col("val_tot").cast(DoubleType()))

# 7. ESCRITA
df.write \
    .mode("overwrite") \
    .partitionBy("dt_particao") \
    .parquet(destination)

# 8. LOG
print(f"{env} | SOR to SOT completed")