import os, time
import multiprocessing

def test(a, b):
    print(f"a={a}, b={b}")
    time.sleep(3)

with multiprocessing.Pool(os.cpu_count()) as pool:

    for a, b in zip(range(10), range(10)):
        pool.apply_async(test, a, b)

    pool.close()

