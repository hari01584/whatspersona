import praw
import pandas as pd
from praw.models import MoreComments

reddit = praw.Reddit(client_id='dZ-kE8RNQnHDoBZbdAaVDg', client_secret='v4_CbTupSbZZiLYynwko1ZhJ0TjZjg', user_agent='praw scrape')

LIMIT = 1000

hot_posts = reddit.subreddit('depression').hot(limit=LIMIT)
posts = []

i=0
for post in hot_posts:
    print(i,post)
    for top_level_comment in post.comments:
        if isinstance(top_level_comment, MoreComments):
            continue
        reply = top_level_comment.body
        break
    
    posts.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, reply, post.created])
    i+=1

posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'reply','created'])
print(posts)

posts.to_csv('depression_data.csv')