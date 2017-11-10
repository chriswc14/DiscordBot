import json


chatHist = open('../Data/Danger_Logs.json', 'r', encoding='utf-8')

chatHist = json.load(chatHist)

# Server IDs
namsla = '250040817366990848'
devchat = '370359173453447184'

newText = open('../Data/new.txt', 'w', encoding='utf-8')

biggestStr = 0
i = 0

# Take only messages less than this
MSG_CHAR_LIMIT = 200
# Take only this many messages
TOTAL_MSG_LIMIT = 10000


for msg in chatHist['data'][namsla]:
    x = chatHist['data'][namsla][msg]['m']
    
    x=bytes(x, 'utf-8').decode('utf-8','')

    if(len(x) > biggestStr):
        biggestStr = len(x)

    # Ommit lines with nothing on them 
    if(len(x) <= 0):
        print()
    # Don't take messages with more than 200 characters
    elif(len(x) >= MSG_CHAR_LIMIT):
        print(x)
    else:
        print(x)
        newText.write(x + '\n')
        newText.write('\n')
        i=i+1
    # Only pull 
    if(i > TOTAL_MSG_LIMIT):
        break

newText.close()
    
print('Done!')
print('Biggest Msg was: ')
print(biggestStr)
