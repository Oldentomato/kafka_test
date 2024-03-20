from kafka import KafkaAdminClient
from kafka.admin.new_topic import NewTopic
from kafka.admin.new_partitions import NewPartitions

client = KafkaAdminClient(bootstrap_servers=['localhost:9092'])

topic_list = []
#데이터의 순서가 중요할 경우 파티션을 1개로 할 것
topic_list.append(NewTopic(name="test_topic", num_partitions=5, replication_factor=1)) #replication_factor의 수는 broker의 수보다 작아야함(여러대의 broker에 복제되는 수임)
topic_rsp = client.create_topics(new_topics=topic_list, validate_only=False)

# modify partition
# partition_rsp = client.create_partitions({
#     'topic1': NewPartitions(4)
# })

print(topic_rsp)