import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext

from pyspark.sql.functions import col, length, when


args = getResolvedOptions(sys.argv, ['ENV', 'BUCKET'])
env = args['ENV']
bucket = args['BUCKET']


sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session


source = f"s3://{bucket}/SOR/movies/"
destination = f"s3://{bucket}/SOT/movies/"


df = spark.read.parquet(source)


# garantir colunas em lowercase (segurança)
df = df.toDF(*[c.lower() for c in df.columns])

# dicionário de tradução / padronização
colunas_ptbr = {
    "title": "titulo",
    "runtime_min": "duracao_minutos",
    "title_length": "tamanho_titulo",
    "release_year": "ano_lancamento",
    "genre": "genero",
    "rating": "avaliacao",
    "votes": "quantidade_votos",
    "director": "diretor"
}

# aplicar rename apenas nas colunas existentes
for col_original, col_nova in colunas_ptbr.items():
    if col_original in df.columns:
        df = df.withColumnRenamed(col_original, col_nova)


# remover nulos críticos antes de tudo
df = df.dropna(subset=["titulo", "duracao_minutos"])


# tamanho do título
df = df.withColumn("tamanho_titulo", length(col("titulo")))


# classificar duração
df = df.withColumn(
    "categoria_duracao",
    when(col("duracao_minutos") < 90, "curto")
    .when((col("duracao_minutos") >= 90) & (col("duracao_minutos") <= 120), "medio")
    .otherwise("longo")
)


# popularidade (se existir)
if "popularity_score" in df.columns:
    df = df.withColumnRenamed("popularity_score", "pontuacao_popularidade")

    df = df.withColumn(
        "categoria_popularidade",
        when(col("pontuacao_popularidade") < 50, "baixa")
        .when((col("pontuacao_popularidade") >= 50) & (col("pontuacao_popularidade") <= 80), "media")
        .otherwise("alta")
    )

# salvar particionado
df.write \
    .mode("overwrite") \
    .partitionBy("ano_lancamento") \
    .parquet(destination)


print(f"{env} | SOR to SOT movies completed")