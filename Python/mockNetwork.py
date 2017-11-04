import random 
import sys

# Returns the trained network
def trainNetwork(network, msgs):
    return network
# Returns the loaded network
def loadNetwork(filepath):
    network=0
    return network

# Returns the success or failure of the save 
def saveNetwork(network, filepath):
    return True

def runNetwork(msg):
    responses = ['hello', 'whats up', 'sup', 'yayaya', 'happy birthday', 'im a real person i swear']
    return random.choice(responses)

def main():
    run = True
    while run == True:
        call = sys.stdin.readline().split()
        if call[0] == 'runNetwork':
            res = runNetwork(call[1])
        elif call[0] == 'saveNetwork':
            res = saveNetwork(call[1], call[2])
        elif call[0] == 'loadNetwork':
            res = loadNetwork(call[1])
        elif call[0] == 'trainNetwork':
            res = trainNetwork(call[1], call[2])
        print(res)


main()