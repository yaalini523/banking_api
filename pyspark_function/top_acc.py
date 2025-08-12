from pyspark.sql import SparkSession
from pyspark.sql.functions import sum, desc

spark = SparkSession.builder \
    .appName("ReadPostgres") \
    .config("spark.jars", "/home/yaalini/libs/postgresql-42.7.7.jar") \
    .getOrCreate()

df = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://localhost:5432/bankdb") \
    .option("dbtable", '"public"."Transaction"') \
    .option("user", "postgres") \
    .option("password", "yaalini") \
    .option("driver", "org.postgresql.Driver") \
    .load()

top_10_acc = df.groupBy("account_id") \
    .agg(sum("amount").alias("total_amount")) \
    .orderBy(desc("total_amount")) \
    .limit(10)

top_10_acc.show()


input("enter...")

spark.stop()
