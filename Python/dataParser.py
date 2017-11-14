import json
import re


chatHist = open('../Data/Unparsed/Danger_Logs.json', 'r', encoding='utf-8')

chatHist = json.load(chatHist)

# Server IDs
namsla = '250040817366990848'
devchat = '370359173453447184'

newText = open('../Data/Parsed/anon_discord.txt', 'w', encoding='utf-8')

msgRemoved = 0
i = 0

# Take only messages less than this
MSG_CHAR_LIMIT = 125
# Take only this many messages
TOTAL_MSG_LIMIT = 10000
# Take only messages matching stuff on the American keyboard
USA = re.compile("^[\x20-\x7F]*$")



for msg in chatHist['data'][namsla]:
    x = chatHist['data'][namsla][msg]['m']
    
    x=bytes(x, 'utf-8').decode('utf-8','')

    if(len(x) <= 0):
        msgRemoved=msgRemoved+1
    # elif(len(x) >= MSG_CHAR_LIMIT):
    #     msgRemoved=msgRemoved+1
    elif(USA.match(x) == None):
        msgRemoved=msgRemoved+1
    else:
        print(x)
        newText.write(x + '\n')
        # newText.write('\n')
        i=i+1

    if(i > TOTAL_MSG_LIMIT):
        break

newText.close()
    
print('Done!')
print('Total messages removed: ', end="")
print(msgRemoved)
