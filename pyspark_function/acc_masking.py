from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.types import StringType

spark = SparkSession.builder \
    .appName("ReadPostgres") \
    .config("spark.jars", "/home/yaalini/libs/postgresql-42.7.7.jar") \
    .getOrCreate()

df = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://localhost:5432/bankdb") \
    .option("dbtable", '"public"."Account"') \
    .option("user", "postgres") \
    .option("password", "yaalini") \
    .option("driver", "org.postgresql.Driver") \
    .load()

def mask_account_number(acc_num):
    if acc_num is None:
        return None
    acc_str = str(acc_num)
    
    if len(acc_str) <= 4:
        return acc_str
    return "*" * (len(acc_str) - 4) + acc_str[-4:]

mask_account_number_udf = udf(mask_account_number, StringType())

df_masked = df.withColumn("masked_account_number", mask_account_number_udf(col("account_number")))

df_masked.select("account_number","masked_account_number").show()
    

input("enter...")

spark.stop()
