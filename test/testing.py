import requests
import threading
import time


def make_request():
    print('got call')
    try:
        r = requests.get('http://localhost:8081/ping')
        print(r.text)
    except Exception as e:
        print('exception', e)


start = time.time()
for i in range(100):
    print(i)
    t = threading.Thread(target=make_request)
    t.start()
    t.join()
end = time.time()
print('Time taken ', end-start)
