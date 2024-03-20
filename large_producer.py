from kafka import KafkaProducer
import csv
import math
import concurrent.futures
import time
from json import dumps

topic_name = "test_topic"
# Kafka Broker 설정
bootstrap_servers = 'localhost:9092'
# CSV 파일 경로
csv_file = 'gt.csv'
# Kafka Producer 개수
num_producers = 100

# Kafka Producer 생성 함수
def create_producer():
    return KafkaProducer(    
            acks='all', #메시지 전송 완료에 대한 체크
            compression_type='gzip', 
            #메시지 전달할 때 압축(None, gzip, snappy, lz4 등),
            retries=5,  # 메시지 전송 실패 시 최대 5번 재시도
            retry_backoff_ms=1000,  # 재시도 간격을 100ms로 설정
            bootstrap_servers=bootstrap_servers,
            api_version=(0,11,5),
            value_serializer=lambda x:dumps(x).encode('utf-8')
            )

# CSV 파일을 분할하여 각 Producer에게 전송하는 함수
def send_messages(producer, topic, data):
    for row in data:
        message = ','.join(row)
        producer.send(topic, message)

# CSV 파일을 읽어서 데이터를 가져오는 함수
def read_csv(file):
    with open(file, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
    return rows

# CSV 파일을 분할하여 전송할 데이터를 생성하는 함수
def split_data(data, num_chunks):
    chunk_size = math.ceil(len(data) / num_chunks)
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

if __name__ == "__main__":
    start = time.time()
    # CSV 파일 읽기
    data = read_csv(csv_file)
    # 데이터 분할
    # chunks = split_data(data, num_producers)

    # for chunk in chunks:
    #     print(len(chunk))

    # ThreadPoolExecutor를 사용하여 병렬로 Producer 생성
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_producers) as executor:
        # Producer를 생성하고 데이터 전송
        futures = []
        for i in range(0,num_producers):
            producer = executor.submit(create_producer)
            future = executor.submit(send_messages, producer.result(), topic_name, data)
            futures.append(future)

    # 모든 작업 완료 대기
    for i,future in enumerate(concurrent.futures.as_completed(futures)):
        future.result()

    print(f'[All Done]: {time.time()-start}')
