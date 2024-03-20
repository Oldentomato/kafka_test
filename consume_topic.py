from pyspark.sql import SparkSession
import os
# os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-10_2.12:3.2.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0 pyspark-shell'

sc = SparkSession.builder.getOrCreate()

sc.sparkContext.setLogLevel('ERROR')

#Read stream
log = sc.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:29092") \
    .option("subscribe", "test1") \
    .option("startingOffsets", "earliest") \
    .load() 

#Write stream - console
query = log.selectExpr("CAST(value AS STRING)") \
    .writeStream \
    .format("console") \
    .option("truncate", "false") \
    .start()

#Write stream - HDFS
query2 = log.selectExpr("CAST(value AS STRING)") \
    .writeStream \
    .outputMode("append") \
    .option("checkpointLocation", "/check") \
    .option("path", "/test") \
    .start()

query.awaitTermination()
query2.awaitTermination()