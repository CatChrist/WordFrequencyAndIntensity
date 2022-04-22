def getCommentsWithWord(word, subreddit):
    if (word == ''):
        return False
    try:
        with open(subreddit + "_comment_data.csv") as rf:
                rf.readline()## Discards the top
                comments = rf.readlines()## line (ie: key)

                with open(subreddit + '_words/' + word + '_in_' + subreddit + '.csv', 'w') as wf:
                    for comment in comments:
                        if word in comment.lower():
                            wf.write(comment)
    except:
        print("Error opening " + subreddit + "_comment_data.csv")


# userInput = ''
# while (userInput != 'end'):
#     userInput = input('word,subreddit: ')
#     try:
#         userInput = userInput.split(',')
#         word = userInput[0]
#         subreddit = userInput[1]
#         getCommentsWithWord(word, subreddit)
#     except:
#         print("Error with input.")

words = ['covid',
         'vaccine',
         'government',
         'news',
         'work',
         'money',
         'old',
         'time',
         'fuck',
         'years',
         'mask',
         'public']

subreddits = [
    'conspiracy',
    'coronavirus',
    'askReddit']

for subreddit in subreddits:
    print('Getting comments from ' + subreddit)
    for word in words:
        getCommentsWithWord(word, subreddit)
