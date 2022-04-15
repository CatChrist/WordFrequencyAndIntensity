def getCommentsWithWord(word):
    if (word == ''):
        return False
    with open("conspiracy_comment_data.csv") as con_rf:
        with open("coronavirus_comment_data.csv") as corona_rf:
            con_rf.readline()## Discards the top
            corona_rf.readline() ## line (ie: key)
            conspiracy_comments = con_rf.readlines()
            coronavirus_comments = corona_rf.readlines()

            with open(word+'.csv', 'w') as wf:
                for comment in conspiracy_comments:
                    if word in comment.lower():
                        wf.write(comment)
                for comment in coronavirus_comments:
                    if word in comment.lower():
                        wf.write(comment)

userInput = ''
while (userInput != 'end'):
    getCommentsWithWord(userInput)
    userInput = input('word to search for: ')

