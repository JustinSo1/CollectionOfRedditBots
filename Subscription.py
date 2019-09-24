import time

import praw


def main():
    keyword = "Viberg"
    file_name = 'usernames.txt'
    # Time delay required by Reddit
    time_delay = 2

    # Login for bot
    reddit_bot = authenticate()
    username = get_usernames(file_name)
    subreddit_name = "FrugalMaleFashionCDN"
    subject = keyword + " submission found!"
    run_bot(reddit_bot, subreddit_name, username, keyword, time_delay, subject)


def authenticate():
    return praw.Reddit('subscriptionbot', user_agent="subscription bot v01")


# def define_keyword(self, keyword: str):
#     self.keyword = keyword


def get_usernames(filename) -> set:
    try:
        with open(filename, "r") as file:
            usernames = file.read().split("\n")
            usernames = set(list(filter(None, usernames)))
    except IOError:
        print("Error: File " + filename + " was not found in the current directory")
        quit()
    return usernames


def send_message(bot, username, subject, body):
    try:
        bot.redditor(username).message(subject, body)
    except praw.exceptions.APIException as e:
        if "USER_DOESNT_EXIST" in e.args[0]:
            print("redditor " + username + " not found, no message sent")
        return
    print("Sent message to  " + username + "!")


def run_bot(bot, subreddit, user_list: set, keyword, time_delay, subject):
    print("Obtaining submissions")
    for submission in bot.subreddit(subreddit).hot(limit=30):
        if keyword in submission.title and submission.author != bot.user.me():
            for user in user_list:
                send_message(bot, user, subject, submission.url)
                time.sleep(time_delay)


if __name__ == '__main__':
    main()
