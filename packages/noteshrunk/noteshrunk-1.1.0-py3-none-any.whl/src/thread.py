import os, time
from concurrent.futures import ThreadPoolExecutor

def test(a, b):
    print(f"a={a}, b={b}")
    time.sleep(3)

with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:

    for a, b in zip(range(10), range(10)):
        executor.submit(test, a=a, b=b)

    executor.shutdown(wait=True)
