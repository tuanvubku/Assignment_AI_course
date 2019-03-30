import itertools
import time
def intialState(n, k):
    matches = []
    if n*k % 2 == 1:
        return None
    for i in range(n):
        matches.append([])
        for j in range(1, k//2 + 1):
            matches[i] += [(i + j) % n, (i - j) % n]
        if k % 2 == 1:
            matches[i].append((i + (n // 2) + 1) % n)
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
        return True
    else:
        return False

def calculateS(matches,points):
    return list(map(lambda x: sum(map(lambda i: points[i], x))/len(x), matches))

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
    file = open("data/input.txt","r")
    n, k = file.readline()[:-1].split(" ")
    n, k = int(n), int(k)
    points = []
    for index in range(n):
        points.append(int(file.readline()))
    file.close()
    # run algorithm
    average = sum(points)/len(points)
    matches = intialState(n,k)
    S = calculateS(matches, points)
    #print(S)
    minIndex, maxIndex = findMinMax(S)
    #print("average: ",average)
    #print(matches)
    while True:
        print('heuristic', heuristic(S))
        print("thay he:", thayHeuristic(matches,points) )
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
        begin = time.time()
        S = calculateS(matches, points)
        end = time.time()
        print('calculateS', end - begin)
        begin = time.time()
        minIndex, maxIndex = findMinMax(S)
        end = time.time()
        print('findMinMax: ', end - begin)
        #print(matches)
    # write output
    return 0


main('input.txt', 'output.txt')
