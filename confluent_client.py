from confluent_kafka.admin import AdminClient, NewTopic, NewPartitions

admin_client = AdminClient({'bootstrap.servers': 'localhost:9092'})

topic_list = []
topic_list.append(NewTopic("test", 5, 1))

admin_client.create_topics(topic_list)

# Modify partitions (uncomment if needed)
# partitions = {'topic1': NewPartitions(4)}
# admin_client.create_partitions(partitions)

print("Topics created successfully")