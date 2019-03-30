import threading
import queue
import time

def foo(i, result):
   result += [i]*100

begin = time.time()
threads = []
numthread = 10
n = 1000000000000
s = []
for i in range(n):
   s.append(i)
# k = n//numthread
# for i in range(0, n, k):
#    result = []
#    t = threading.Thread(target=foo, args=(i,result))
#    t.start()
#    threads.append((t, result))

# s = []
# for t, result in threads:
#    t.join()
#    s += result
end = time.time()

print(s, end - begin)