import json


chatHist = open('../Data/Danger_Logs.json', 'r', encoding='utf-8')

chatHist = json.load(chatHist)

# Server IDs
namsla = '250040817366990848'
devchat = '370359173453447184'

newText = open('../Data/new.txt', 'w', encoding='utf-8')

biggestStr = 0
i = 0

for msg in chatHist['data'][namsla]:
    x = chatHist['data'][namsla][msg]['m']
    
    x=bytes(x, 'utf-8').decode('utf-8','')

    if(len(x) > biggestStr):
        biggestStr = len(x)

    # Ommit lines with nothing on them 
    if(len(x) <= 0):
        print()
    else:
        print(x)
        newText.write(x + '\n')
        newText.write('\n')
        i=i+1

    if(i > 10000):
        break

newText.close()
    
print('Done!')
print('Biggest Msg was: ')
print(biggestStr)
