from pyspark.sql import SparkSession
from pyspark.sql.functions import count

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
    

tot_acc = df.groupby("status").agg(
    count("id").alias("total_account")  
)

tot_acc.show()

input("enter...")

spark.stop()
