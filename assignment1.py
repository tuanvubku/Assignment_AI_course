import itertools
import time
import threading

# def intialState(n, k):
#     matches = []
#     numthread = 10
#     threads = []
#     k = n//numthread
#     for i in range(0, n, k):
#         result = []
#         t = threading.Thread(target=subIntialState, args=(n, k, list(range(i, i+k)), result))
#         t.start()
#         threads.append((t, result))
#     for t, result in threads:
#         t.join()
#         matches += result 
#     return matches

# def subIntialState(n, k, lst, result):
#     print('thread')
#     matches = []
#     if n*k % 2 == 1:
#         return None
#     for i in lst:
#         temp = []
#         for j in range(1, k//2 + 1):
#             temp.append((i + j) % n)
#             temp.append((i - j) % n)
#         if k % 2 == 1:
#             temp.append((i + (n // 2) + 1) % n)
#         matches.append(temp)
#     result = matches

def intialState(n, k):
    matches = []
    if n*k % 2 == 1:
        return None
    for i in range(n):
        temp = []
        for j in range(1, k//2 + 1):
            temp.append((i + j) % n)
            temp.append((i - j) % n)
        if k % 2 == 1:
            temp.append((i + (n // 2) + 1) % n)
        matches.append(temp)
    return matches


def check(matches, k):
    count = [0]*len(matches)
    for i in range(len(matches)):
        for j in matches[i]:
            if j == i: 
                return False
            count[j] += 1
    if all(map(lambda x: x == k, count)):
        return True
    else:
        return False            

def moveState(matches, points, s, average, minIndex, maxIndex):
    maxArr = matches[maxIndex]
    minArr = matches[minIndex]
    optimalValue = abs(s[minIndex] - average) + abs(s[maxIndex] - average)

    cached = []
    for i in range(len(maxArr)):
        if maxArr[i] == minIndex or maxArr[i] in minArr:
            continue
        for j in range(len(minArr)):
            if minArr[j] == maxIndex or minArr[j] in maxArr:
                continue
            maxArr[i], minArr[j] = minArr[j], maxArr[i]
            sMin, sMax = calculateS([minArr,maxArr], points)
            newValue = abs(sMin - average) + abs(sMax - average)
            if newValue < optimalValue:
                optimalValue = newValue
                cached = [i, j]
            maxArr[i], minArr[j] = minArr[j], maxArr[i]
    if len(cached) > 0:
        print('min cached', cached[1])
        print('max cached', cached[0])
        print(minArr[cached[1]])
        maxArr[cached[0]], minArr[cached[1]] = minArr[cached[1]], maxArr[cached[0]]
        s[maxIndex] = sum(map(lambda i: points[i], maxArr))/len(maxArr)
        s[minIndex] = sum(map(lambda i: points[i], minArr))/len(minArr)
        return True
    else:
        return False

# def subCalculateS(matches, points):
#     s = [0]*len(matches)
#     for i in range(len(matches)):
#         for j in matches[i]:
#             s[i] += points[j]
#         s[i] //= len(matches[i])
#     return s

def calculateS(matches,points):
    return list(map(lambda x: sum(map(lambda i: points[i], x))/len(x), matches))
    # numthread = 10
    # threads = []
    # s = []
    # k = len(matches)//numthread
    # if len(matches) < 20:
    #     return subCalculateS(matches, points)
    # for i in range(0, len(matches), k):
    #     print('thread ', i)
    #     t = threading.Thread(target=subCalculateS, args=(matches[i:i+k], points))
    #     t.start()
    #     threads.append(t)
    # for t in threads:
    #     s += t.join()

def findMinMax(s):
    minIndex = 0
    maxIndex = 0
    for i in range(1, len(s)):
        if s[i] > s[maxIndex]:
            maxIndex = i
        if s[i] < s[minIndex]:
            minIndex = i
    return maxIndex, minIndex

def thayHeuristic(matches, points):
    result = 0
    s = calculateS(matches, points)
    for i in range(len(s)):
        for j in range(i + 1, len(s)):
            result += abs(s[i] - s[j])
    return result
            

def heuristic(s):
    average = sum(s)/len(s)
    return sum(map(lambda x: abs(x - average), s))


def main(file_input, file_output):
    # read input 
    begin = time.time()
    file = open("data/input.txt","r")
    n, k = file.readline()[:-1].split(" ")
    n, k = int(n), int(k)
    points = []
    for index in range(n):
        points.append(int(file.readline()))
    file.close()
    end = time.time()
    print("read file ", end - begin )
    # run algorithm
    begin = time.time()
    average = sum(points)/len(points)
    end = time.time()
    print('average:', end - begin)
    begin = time.time()
    matches = intialState(n, k)
    end = time.time()
    print('Initial state:', end - begin)
    
    S = calculateS(matches, points)
    #print(S)
    minIndex, maxIndex = findMinMax(S)
    #print("average: ",average)
    #print(matches)
    while True:
        begin = time.time()
        print('heuristic', heuristic(S))
        end = time.time()
        print('loz:', end - begin)
        
        #begin = time.time()
        # print("thay he:", thayHeuristic(matches,points) )
        # end = time.time()
        # print('loz thay', end - begin)
        #print(check(matches, k))
        # print('min', matches[minIndex])
        # print('max', matches[maxIndex])
        begin = time.time()
        change = moveState(matches,points,S,average,minIndex,maxIndex)
        end = time.time()
        print('moveState: ', end - begin)
        
        if not change:
            break
        print("min", minIndex, "max", maxIndex)
        # begin = time.time()
        # S = calculateS(matches, points)
        # end = time.time()
        # print('calculateS', end - begin)
        begin = time.time()
        minIndex, maxIndex = findMinMax(S)
        end = time.time()
        print('findMinMax: ', end - begin)
        #print(matches)
    # write output
    print(matches)
    print('loz thay', thayHeuristic(matches, points))
    return 0


main('input.txt', 'output.txt')
