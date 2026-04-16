
import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext

from pyspark.sql.functions import col, length, when

# =========================================================
# 1. PARAMETROS
# =========================================================
args = getResolvedOptions(sys.argv, ['ENV', 'BUCKET'])
env = args['ENV']
bucket = args['BUCKET']

# =========================================================
# 2. SPARK
# =========================================================
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# =========================================================
# 3. CAMINHOS
# =========================================================
source = f"s3://{bucket}/SOR/movies/"
destination = f"s3://{bucket}/SOT/movies/"

# =========================================================
# 4. LEITURA
# =========================================================
df = spark.read.parquet(source)

# =========================================================
# 5. REGRAS DE NEGÓCIO
# =========================================================

# tamanho do título
df = df.withColumn("title_length", length(col("title")))

# classificar duração do filme
df = df.withColumn(
    "duration_category",
    when(col("runtime_min") < 90, "short")
    .when((col("runtime_min") >= 90) & (col("runtime_min") <= 120), "medium")
    .otherwise("long")
)

# classificar popularidade (se existir coluna)
if "popularity_score" in df.columns:
    df = df.withColumn(
        "popularity_category",
        when(col("popularity_score") < 50, "low")
        .when((col("popularity_score") >= 50) & (col("popularity_score") <= 80), "medium")
        .otherwise("high")
    )

# =========================================================
# 6. FILTROS
# =========================================================
df = df.filter(col("title").isNotNull())

# =========================================================
# 7. ESCRITA
# =========================================================
df.write \
    .mode("overwrite") \
    .parquet(destination)

# =========================================================
# 8. LOG
# =========================================================
print(f"{env} | SOR to SOT movies completed")