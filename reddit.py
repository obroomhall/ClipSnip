import os
import praw
from praw.models import MoreComments

client_id = os.environ['reddit_client_id']
client_secret = os.environ['reddit_client_secret']
user_agent='testscript by /u/autogifbot'

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)


def get_quote_candidates(submission_id):

    submission = reddit.submission(id=submission_id)

    candidates = []

    for top_level_comment in submission.comments:
        if not isinstance(top_level_comment, MoreComments) and top_level_comment.score > 0:
            candidates.append(top_level_comment.body)

    return candidates
