import threading
import queue
import time

def foo(i, result):
   result += [i, i + 1, i + 2]

begin = time.time()
threads = []
for i in range(0, 20, 3):
   result = []
   t = threading.Thread(target=foo, args=(i,result))
   t.start()
   threads.append((t, result))

s = []
for t, result in threads:
   t.join()
   s += result
end = time.time()

print(s, end - begin)