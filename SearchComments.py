import praw
import config


def bot_login():
    return praw.Reddit(username=config.username,
                       password=config.password,
                       client_id=config.client_id,
                       client_secret=config.client_secret,
                       user_agent=config.username + "'s searching comment bot v01"
                       )


def run_bot(searching_comment):
    for comment in searching_comment.subreddit('test').comments(limit=25):
        if "dog" in comment.body:
            print("String found!!")
            comment.reply("I also love dogs! [Here](https://i.imgur.com/Je6bYdS.jpg) is an image of one!")


r = bot_login()
run_bot(r)
