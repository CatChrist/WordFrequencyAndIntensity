from tqdm import tqdm
import praw
from os import system as sys

reddit = praw.Reddit(
  client_id = "uN1ESkVn6Zc4xE8Z7bQ5hA",
  client_secret = "1DPFUZyDcoGGURNDiicQMQjN7xBWLA",
  user_agent = "Reddit Crawling v0.5 by /u/lsjame02",
  username = "lsjame02",
  password = "UofLCSE393"
)

def fetchComments(subreddit_name):
    print("Fetching Comments From r/{}...".format(subreddit_name))
    total_comment_count = 0
    total_error_count = 0
    with open(subreddit_name + '_submission_data.csv') as rf:
        rf.readline() #skips the first line which includes the key for the csv
        with open(subreddit_name + '_comment_data.csv', 'w') as wf:
            wf.write('Comment ID,Submission ID,Content,Author,Time Created(UTC),# of Upvotes\n')
            for submission_data in tqdm(rf.readlines()):
                submission_id = submission_data[:6]
                submission = reddit.submission(submission_id)
                commentForrest = submission.comments
                commentForrest.replace_more()

                for comment in commentForrest:

                    try:
                        comment_id = comment.id
                        content = comment.body
                        author = comment.author.name
                        created_time = comment.created_utc
                        upvotes = comment.score

                        columns = [comment_id, submission_id, content, author, created_time, upvotes]

                        for column in columns:
                            column = str(column)
                            column = column.replace(',', '')
                            column = column.replace("’", "")
                            column = column.replace("'", "")
                            column = column.replace('.', '')
                            column = column.replace("“", '"')
                            column = column.replace("”", '"')
                            column = column.replace("\n"," ")
                            column = column.replace("\t"," ")
                            column = " ".join(column.split())
                            column = column.encode("ascii", "ignore")
                            column = column.decode()

                            if (column != str(upvotes)):
                                wf.write(column + ',')
                            else:
                                wf.write(column)
                        total_comment_count+=1
                        wf.write('\n')

                    except:
                        total_error_count+=1

    print("Done with {} comments retrieved and {} omitted.".format(total_comment_count, total_error_count))
    return [subreddit_name, total_comment_count, total_error_count]

def printData(data):
    print("{} subreddit returned {} comments with {} errors.".format(data[0],data[1],data[2]))


askRedditData = fetchComments("askReddit")
conspiracyData = fetchComments("conspiracy")
coronavirusData = fetchComments("coronavirus")

sys('cls')

printData(askRedditData)
printData(conspiracyData)
printData(coronavirusData)

input("\aPress Enter to exit.")
