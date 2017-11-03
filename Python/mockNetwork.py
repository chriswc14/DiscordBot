import random 

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
    print(runNetwork('bruh'))

main()