from kafka import KafkaProducer
from json import dumps
import time
import csv


csv_file = 'gt.csv'

producer = KafkaProducer(
    acks='all', #메시지 전송 완료에 대한 체크
    compression_type='gzip', #메시지 전달할 때 압축(None, gzip, snappy, lz4 등)
    #압축은 메세지의 양이 많으면서 xml,json처럼 정형화되고 반복되는 구조에 하는 것이 좋다
    bootstrap_servers=['localhost:9092'], #전달하고자 하는 카프카 브로커의 주소 리스트
    retries=5,  # 메시지 전송 실패 시 최대 5번 재시도
    retry_backoff_ms=1000,  # 재시도 간격을 100ms로 설정
    api_version=(0,11,5),
    value_serializer=lambda x:dumps(x).encode('utf-8') #메시지의 값 직렬화
)

def read_csv(file):
    with open(file, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
    return rows

data = read_csv(csv_file)

start = time.time()

# for row in data:
#     message = ','.join(row)
#     producer.send('topic1', message)
#     producer.flush()
for i in range(1000):
    data = {'str': f'result{i}'}
    producer.send('topic1', value=data) #내부 버퍼에 쌓아두고
    producer.flush() #broker에게 전달

print(f'[Done]: {time.time()-start}')