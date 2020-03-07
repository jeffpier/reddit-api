""" Import all the things """
import datetime
import praw
import json
import os
import sys

from praw.models import MoreComments

""" Authentication GLOBALS """
C_ID = ""
C_SECRET = ""
USER_AGENT = ""
USER_NAME = ""
PASSWD = ""

""" Subreddit GLOBALS """
SUBREDDIT = 'stocks'
POST_PULL_COUNT = 10

""" Write path """
WRITE_PATH_POST = '/posts'
WRITE_PATH_COMMENT = '/comments'


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
        subreddit_pull = subreddit.hot(limit=POST_PULL_COUNT)
    except Exception:
        sys.exit('Could not find subreddit \'{}\''.format(SUBREDDIT))

    """ Pull the posts and write the file to JSON """
    try:
        for submission in subreddit_pull:
            data = []
            item = reddit.submission(submission.id)
            created_timestamp = datetime.datetime.fromtimestamp(item.created_utc)
            filename = submission.id + '.json'

            """ Check if post has been edited """
            if item.edited > 0:
                edited_timestamp = datetime.datetime.fromtimestamp(item.edited)
                data.append({
                    'created': created_timestamp.strftime('%Y-%m-%dT%H:%M:%S.%f'),
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
                    'edited': edited_timestamp.strftime('%Y-%m-%dT%H:%M:%S.%f')
                })
            else:
                data.append({
                    'created': created_timestamp.strftime('%Y-%m-%dT%H:%M:%S.%f'),
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

            """ Write the post JSON to file """
            if not os.path.exists(os.path.join(WRITE_PATH_POST, filename)):
                try:
                    with open(os.path.join(WRITE_PATH_POST, filename), 'w', newline='', encoding="utf-8") as f:
                        json.dump(data[0], f)
                except Exception:
                    sys.exit("Error writing the post JSON file {}".format(os.path.join(WRITE_PATH_POST, filename)))

            ''' Get the top-level comments for the post '''
            comments = reddit.submission(item.id)

            for comment in comments.comments:
                if isinstance(comment, MoreComments):
                    continue
                data = []
                filename = comment.id + '.json'
                created_timestamp = datetime.datetime.fromtimestamp(comment.created_utc)

                """ Check if post has been edited """
                if comment.edited > 0:
                    edited_timestamp = datetime.datetime.fromtimestamp(comment.edited)
                    data.append({
                        'created': created_timestamp.strftime('%Y-%m-%dT%H:%M:%S.%f'),
                        'id': str(comment.id),
                        'parent_post': item.id,
                        'author': str(comment.author),
                        'description': comment.body.replace('\n', ' '),
                        'permalink': comment.permalink,
                        'subreddit': SUBREDDIT,
                        'up_votes': comment.ups,
                        'down_votes': comment.downs,
                        'score': comment.score,
                        'total_awards': comment.total_awards_received,
                        'controversiality': comment.controversiality,
                        'depth': comment.depth,
                        'edited': edited_timestamp.strftime('%Y-%m-%dT%H:%M:%S.%f')
                    })
                else:
                    data.append({
                        'created': created_timestamp.strftime('%Y-%m-%dT%H:%M:%S.%f'),
                        'id': str(comment.id),
                        'parent_post': item.id,
                        'author': str(comment.author),
                        'description': comment.body.replace('\n', ' '),
                        'permalink': comment.permalink,
                        'subreddit': SUBREDDIT,
                        'up_votes': comment.ups,
                        'down_votes': comment.downs,
                        'score': comment.score,
                        'total_awards': comment.total_awards_received,
                        'controversiality': comment.controversiality,
                        'depth': comment.depth,
                        'edited': False
                    })

                """ Write the comment JSON to file """
                if not os.path.exists(os.path.join(WRITE_PATH_COMMENT, filename)):
                    try:
                        with open(os.path.join(WRITE_PATH_COMMENT, filename), 'w', newline='', encoding="utf-8") as f:
                            json.dump(data[0], f)
                    except Exception:
                        sys.exit("Error writing the comment JSON file {}".format(os.path.join(WRITE_PATH_COMMENT, filename)))

    except Exception:
        sys.exit('Error with the API pull, try adjusting the number of posts to pull in variable POST_PULL_COUNT.')


if __name__ == '__main__':
    main()
