import re


data = open('../Data/Unparsed/supreme.conversations.txt', 'r', encoding='utf-8')
newText = open('../Data/Parsed/supreme_cornell.txt', 'w', encoding='utf-8')

msgRemoved = 0
i = 0

# Take only messages less than this
MSG_CHAR_LIMIT = 125
# Take only this many messages
TOTAL_MSG_LIMIT = 10000
# Take only messages matching stuff on the American keyboard
USA = re.compile("^[\x20-\x7F]*$")

for msg in data:
    msg = msg.split("+++$+++")[7]
    
    msg=bytes(msg, 'utf-8').decode('utf-8','')

    if(len(msg) <= 0):
        msgRemoved=msgRemoved+1
    # elif(len(x) >= MSG_CHAR_LIMIT):
    #     msgRemoved=msgRemoved+1
    elif(USA.match(msg) == None):
        msgRemoved=msgRemoved+1
    else:
        print(msg)
        newText.write(msg)
        i=i+1

    if(i > TOTAL_MSG_LIMIT):
        break

newText.close()
    
print('Done!')
print('Total messages removed: ', end="")
print(msgRemoved)
