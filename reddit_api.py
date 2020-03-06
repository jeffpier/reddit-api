""" Import all the things """
import datetime
import praw
import json
import os
import sys

""" Authentication GLOBALS """
C_ID = ""
C_SECRET = ""
USER_AGENT = ""
USER_NAME = ""
PASSWD = ""

""" Subreddit GLOBALS """
SUBREDDIT = 'wallstreetbets'
POST_PULL_COUNT = 100

""" Write path """
WRITE_PATH = '/home/reddit/wallstreetbets'


def main():
    """ Authenticate """
    try:
        reddit = praw.Reddit(client_id=C_ID, client_secret=C_SECRET, user_agent=USER_AGENT)
    except Exception:
        sys.exit('Could not authenticate with Reddit.')

    """ Verify the Subreddit exists """
    try:
        reddit.subreddits.search_by_name(SUBREDDIT, exact=True)
        subreddit = reddit.subreddit(SUBREDDIT)
        subreddit_pull = subreddit.new(limit=POST_PULL_COUNT)
    except Exception:
        sys.exit('Could not find subreddit \'{}\''.format(SUBREDDIT))


    """ Pull the posts and write the file to JSON """
    try:
        for submission in subreddit_pull:
            item = reddit.submission(submission.id)
            created_timestamp = datetime.datetime.fromtimestamp(item.created_utc)
            filename = subreddit.display_name + '-' + submission.id + '.json'
            data = []
            """ Check if post has been edited """
            if item.edited > 0:
                edited_timestamp = datetime.datetime.fromtimestamp(item.edited)
                data.append({
                    'created': created_timestamp.strftime('%m-%d-%Y %H:%M:%S'),
                    'id': item.id,
                    'author': str(item.author),
                    'title': item.title,
                    'description': item.selftext.replace('\n', ' '),
                    'permalink': item.permalink,
                    'url': item.url,
                    'up_votes': item.ups,
                    'down_votes': item.downs,
                    'score': item.score,
                    'total_awards': item.total_awards_received,
                    'comments': item.num_comments,
                    'nsfw': item.over_18,
                    'crossposts': item.num_crossposts,
                    'stickied': item.stickied,
                    'edited': edited_timestamp.strftime('%m-%d-%Y %H:%M:%S')
                })
            else:
                data.append({
                    'created': created_timestamp.strftime('%m-%d-%Y %H:%M:%S'),
                    'id': item.id,
                    'author': str(item.author),
                    'title': item.title,
                    'description': item.selftext.replace('\n', ' '),
                    'permalink': item.permalink,
                    'url': item.url,
                    'up_votes': item.ups,
                    'down_votes': item.downs,
                    'score': item.score,
                    'total_awards': item.total_awards_received,
                    'comments': item.num_comments,
                    'nsfw': item.over_18,
                    'crossposts': item.num_crossposts,
                    'stickied': item.stickied,
                    'edited': False
                })

            """ Write the JSON to file """
            if not os.path.exists(os.path.join(WRITE_PATH, filename)):
                try:
                    with open(os.path.join(WRITE_PATH, filename), 'w', newline='', encoding="utf-8") as f:
                        json.dump(data[0], f)
                except Exception:
                    sys.exit("Error writing the JSON file {}".format(os.path.join(WRITE_PATH, filename)))

    except Exception:
        sys.exit('Error with the API pull, try adjusting the number of posts to pull in variable POST_PULL_COUNT.')


if __name__ == '__main__':
    main()
