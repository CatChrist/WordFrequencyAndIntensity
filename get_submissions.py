import praw
from os import system as sys

##################

reddit = praw.Reddit(
  client_id = "",
  client_secret = "",
  user_agent = "Reddit Crawling v1.0 by /u/lsjame02",
  username = "",
  password = ""
)

##################

subreddit_name = "askReddit"

def fetchSubmissions(subreddit_name):
  subreddit = reddit.subreddit(subreddit_name)

  print("Fetching Submissions From r/{}...".format(subreddit_name))
  total_submission_count = 0
  with open(subreddit_name + '_submission_data.csv', 'w') as wf:
    wf.write('Submission ID,Title,Content,Author,Time Created(UTC),# of Upvotes,Upvote Ratio\n')
    for submission in subreddit.top('year'):

      try:
        submission_id = submission.id
        title = submission.title
        content = submission.selftext
        author = submission.author.name
        created_time = submission.created_utc
        upvotes = submission.score
        upvote_ratio = submission.upvote_ratio

        columns = [submission_id, title, author, created_time, upvotes, upvote_ratio]

        for column in columns:
          column = str(column)
          column = column.replace(',', '')
          column = column.replace("’", "'")
          column = column.replace("“", '"')
          column = column.replace("”", '"')
          column = column.replace("\n"," ")
          column = column.replace("\t"," ")
          column = " ".join(column.split())
          column = column.encode("ascii", "ignore")
          column = column.decode()
          if (column != str(upvote_ratio)):
            wf.write(column + ',')
          else:
            wf.write(column)
        
        total_submission_count+=1
        wf.write('\n')

      except:
        print("A piece of data could not be retreived from this submission, discarding it and moving on.")

  print("Done, with {} results retrieved.".format(total_submission_count))

  return [subreddit_name, total_submission_count]

def printData(data):
  print("{} subreddit returned {} submissions.".format(data[0],data[1]))

askRedditData =fetchSubmissions("askReddit")
conspiracyData =fetchSubmissions("conspiracy")
coronavirusData =fetchSubmissions("coronavirus")

sys('cls')

printData(askRedditData)
printData(conspiracyData)
printData(coronavirusData)


input("\aPress Enter to exit.")

  