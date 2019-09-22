import time
import praw
import config
import os


def bot_login():
    return praw.Reddit(username=config.username,
                       password=config.password,
                       client_id=config.client_id,
                       client_secret=config.client_secret,
                       user_agent=config.username + "'s searching comment bot v01"
                       )


def run_bot(searching_comment, comments_replied):
    print("Obtaining comments")

    for comment in searching_comment.subreddit('test').comments(limit=25):
        if "dog" in comment.body and comment.id not in comments_replied and comment.author != r.user.me():
            print("String found!!")
            comment.reply("I also love dogs! [Here](https://i.imgur.com/Je6bYdS.jpg) is an image of one!")
            print("Replied to comment " + comment.id)

            comments_replied.append(comment.id)

            with open("comments_replied_to.txt", "a") as f:
                f.write(comment.id + "\n")
    print("Sleeping")
    time.sleep(10)


def check_saved_comments():
    if not os.path.isfile("comments_replied_to.txt"):
        comments_file = []
    else:
        with open("comments_replied_to.txt", "r") as f:
            comments_file = f.read().split("\n")
            comments_file = list(filter(None, comments_file))
    return comments_file


r = bot_login()
comments_replied_to = check_saved_comments()
print(comments_replied_to)
while True:
    run_bot(r, comments_replied_to)
