import random
inputFile = open("data/input.txt","w")
n = input("Please enter n = ")
k = input("Please enter k = ")
if int(n) % 2 ==1 and int(k) % 2 ==1 :
    print("At least one input is even!")
inputFile.write(n + " " +k)
inputFile.write("\n")

for x in range(int(n)):
    t = random.randint(1,2*int(n))
    inputFile.write(str(t))
    inputFile.write("\n")

inputFile.close()