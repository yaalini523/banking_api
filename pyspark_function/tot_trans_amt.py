from pyspark.sql import SparkSession
from pyspark.sql.functions import sum, count

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
    
#df_credits = df.filter(df.transaction_type == "Credit")

tot_amt = df.groupby("account_id","transaction_type").agg(
    sum("amount").alias("total_amount")  
)

tot_amt.show()

input("enter...")

spark.stop()
