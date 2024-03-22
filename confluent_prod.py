from confluent_kafka import Producer
import time 
from json import dumps
import csv



# CSV 파일을 분할하여 각 Producer에게 전송하는 함수
def send_messages(producer, topic, data, flush_count):
    read_count = 0
    for row in data:
        message = ','.join(row)
        producer.produce(topic, dumps(message))
        read_count += 1
        if read_count % flush_count == 0:
            producer.flush()
            print("flushed")
    else:
        producer.flush()

# CSV 파일을 읽어서 데이터를 가져오는 함수
def read_csv(file):
    with open(file, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
    return rows

if __name__ == "__main__":
    start = time.time()
    csv_data = read_csv('vehicle_history.csv')
    producer = Producer(
        {'bootstrap.servers': 'localhost:9092'}
    )

    send_messages(producer, "test_topic2", csv_data, 10000)

    print(f'[All Done]: {time.time()-start}')