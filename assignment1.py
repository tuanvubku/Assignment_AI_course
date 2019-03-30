import itertools

# def compare(a, b):
#     if a[0] == b[0]:
#         return a[1] - b[1]
#     return a[0] - b[0]

# def pick(status, min_x, min_y):
#     for i in range(min_x, len(status)):
#         if status[i] == 0:
#             continue
#         for j in range(i + 1, len(status)):
#             if status[j] == 0:
#                 continue
#             if compare((i, j), (min_x, min_y)) >= 0:
#                 return [i, j]
#     return None

# def search(status, k, n, min_x, min_y):
#     matches = []
#     # min_x = 0
#     # min_y = 1
    
#     while sum(status) > 0:
#         # tmp = list(map(lambda x: (x[0] + 1, x[1] + 1), matches))
#         #print(matches)
#         #print(min_x, min_y)
#         couple = pick(status, 0, 1)
#         print(couple)
#         if not couple:
#             # pop 1 couple out of stack
#             previous = matches[-1]
#             status[previous[0]] += 1
#             status[previous[1]] += 1
#             matches = matches[:-1]
            
#             # modify min_x, min_y
#             min_x = previous[0]
#             min_y = previous[1]
#         else:
#             status[couple[0]] -= 1
#             status[couple[1]] -= 1
#             matches.append((couple[0], couple[1]))
#             min_x = couple[0]
#             min_y = couple[1]
        
#         # increase min_x or min_y
#         if min_y == n - 1:
#             min_x += 1
#             min_y = min_x + 1
#         else:
#             min_y += 1
#         #print(matches)
#     return matches

# def search(status, n, min_x, min_y):
#     # print(status)
#     #print(min_x, min_y)
#     #return 1,2 or 1,3 .....
#     solutions = []
#     couple = pick(status, min_x, min_y)
#     #print(couple, min_x, min_y, status)
#     if (not couple) or (couple[0] != min_x) or (couple[1] != min_y):
#         return None
#     #print('hello')

#     status[min_x] -= 1
#     status[min_y] -= 1

#     # base case
#     if sum(status) == 0:
#         return [[couple]]

#     for i in range(min_x, n):
#         for j in range(i + 1, n):
#             if compare((i, j), (min_x, min_y)) > 0:
#                 subResult = search(status.copy(), n, i, j)
#                 if not subResult:
#                     continue
#                 else:
#                     solutions += list(map(lambda x: [couple] + x, subResult))
                   
    
#     if min_x == 0:
#         for x in solutions:
#             if(len(x) == 25):
#                 print(x)
#     return solutions

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
            

def main(file_input, file_output):
    # read input 
    file = open("input.txt","r")
    n, k = file.readline()[:-1].split(" ")
    n, k = int(n), int(k)
    points = []
    #for index in range(n):
    #    points.append(int(file.readline()))
    file.close()
    # run algorithm
    # if k and n are all odd => cannot find solution
    #status = [k]*n
    #average = sum(points)/len(points)
    matches = intialState(n,k)
    print(matches)
    print(check(matches, k))
    # write output
    return 0


main('input.txt', 'output.txt')
