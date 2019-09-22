import sys
import time
import praw


def authenticate():
    return praw.Reddit('newsletterbot', user_agent="newsletter bot v01")


def get_usernames(filename):
    try:
        with open(filename, "r") as file:
            usernames = file.read().split("\n")
            usernames = list(filter(None, usernames))
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


def main():
    if len(sys.argv) != 4:
        print("usage: Newsletter_bot.py file \"subject\" \"body\"")

    filename = sys.argv[1]
    subject = sys.argv[2]
    body = sys.argv[3]

    reddit_bot = authenticate()
    username = get_usernames(filename)

    for user in username:
        send_message(reddit_bot, user, subject, body)
        time.sleep(5)


if __name__ == '__main__':
    main()
