# =========================================================
# 1. IMPORTS (GLUE)
# =========================================================
import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext

from pyspark.sql.functions import col, to_date, concat, lpad, lit
from pyspark.sql.types import IntegerType, DoubleType

# =========================================================
# 2. PARAMETROS
# =========================================================
args = getResolvedOptions(sys.argv, ['ENV', 'BUCKET'])

env = args['ENV']
bucket = args['BUCKET']

# =========================================================
# 3. SPARK / GLUE
# =========================================================
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# =========================================================
# 4. CAMINHOS (S3)
# =========================================================
source = f"s3://{bucket}/LZ/datasus/internacoes/"
destination = f"s3://{bucket}/SOR/datasus/internacoes/"

# =========================================================
# 5. LEITURA (PARQUET DA LZ)
# =========================================================
df = spark.read.parquet(source)

# =========================================================
# 6. PADRONIZACAO
# =========================================================
df = df.toDF(*[c.lower() for c in df.columns])

# =========================================================
# 7. TRATAMENTO DE TIPOS
# =========================================================
if "ano_cmpt" in df.columns:
    df = df.withColumn("ano_cmpt", col("ano_cmpt").cast(IntegerType()))

if "mes_cmpt" in df.columns:
    df = df.withColumn("mes_cmpt", col("mes_cmpt").cast(IntegerType()))

if "idade" in df.columns:
    df = df.withColumn("idade", col("idade").cast(IntegerType()))

if "val_tot" in df.columns:
    df = df.withColumn("val_tot", col("val_tot").cast(DoubleType()))

if "dt_inter" in df.columns:
    df = df.withColumn("dt_inter", to_date(col("dt_inter"), "yyyyMMdd"))

if "dt_saida" in df.columns:
    df = df.withColumn("dt_saida", to_date(col("dt_saida"), "yyyyMMdd"))

# =========================================================
# 8. LIMPEZA
# =========================================================
df = df.dropna(subset=["uf_zi", "ano_cmpt", "mes_cmpt"])

# =========================================================
# 9. PARTICIONAMENTO
# =========================================================
df = df.withColumn(
    "dt_particao",
    concat(
        col("ano_cmpt").cast("string"),
        lit("-"),
        lpad(col("mes_cmpt").cast("string"), 2, "0")
    )
)

# =========================================================
# 10. ESCRITA (SOR)
# =========================================================
df.write \
    .mode("overwrite") \
    .partitionBy("dt_particao") \
    .parquet(destination)

# =========================================================
# 11. LOG
# =========================================================
print(f"{env} | LZ to SOR completed")