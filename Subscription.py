import time

import praw


def main():
    keyword = input("Enter keyword to search for: ")
    file_name = 'usernames.txt'
    questions_file = 'questions.txt'
    # Time delay required by Reddit
    time_delay = 2

    # Login for bot
    reddit_bot = authenticate()
    username = get_usernames(file_name)
    question = questions_database(questions_file)
    subreddit_name = input("Enter subreddit name to search in (E.g FrugalMaleFashionCDN): ")
    subject = keyword + " submission found!"
    while True:
        run_bot(reddit_bot, subreddit_name, username, keyword, time_delay, subject, question)


def authenticate():
    return praw.Reddit('subscriptionbot', user_agent="subscription bot v01")


def questions_database(questions_file):
    try:
        with open(questions_file, "r") as file:
            questions = file.read().split("\n")
            questions = set(list(filter(None, questions)))
    except IOError:
        print("Error: File " + questions_file + " was not found in the current directory")
        open(questions_file, "w+")
    return questions


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
            print("Redditor " + username + " not found, no message sent")
        return
    print("Sent message to " + username + "!")


def run_bot(bot, subreddit, user_list: set, keyword, time_delay, subject, question):
    print("Obtaining submissions")
    for submission in bot.subreddit(subreddit).hot(limit=30):
        if keyword in submission.title and submission.author != bot.user.me() and submission.title not in question:
            question.add(submission.title)
            with open("questions.txt", "a") as f:
                f.write(submission.title + "\n")
            for user in user_list:
                send_message(bot, user, subject, submission.url)
                time.sleep(time_delay)


if __name__ == '__main__':
    main()
