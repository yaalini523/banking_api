from pyspark.sql import SparkSession
from pyspark.sql.functions import avg

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
    

bal = df.groupby("account_type").agg(
    avg("balance").alias("total_balance")  
)

bal.show()

input("enter...")

spark.stop()
