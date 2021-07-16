import random
import time
import traceback

import praw
from prawcore.exceptions import PrawcoreException


def main():
    users = {}
    # Gets 100 historical comments
    comment_stream = subreddit.stream.comments(pause_after=-1, skip_existing=True)
    # Gets 100 historical submission
    submission_stream = subreddit.stream.submissions(pause_after=-1, skip_existing=True)
    while True:
        try:
            for submission in submission_stream:
                if submission is None:
                    break
                comment = submission.reply(f"BEEP BEEP! [I give it a {random.randint(0, 100)} out of 100.]")
                # Pins, distinguishes, and locks the comment
                comment.mod.distinguish(how="yes", sticky=True)

            for comment in comment_stream:
                if comment is None:
                    break
                if 'u/roadrunner_rates' not in comment.body.lower():
                    continue

                # Iterate over users and delete the record of users which mentioned bot more than 30 minutes ago
                for key, value in list(users.items()):
                    now = time.time()
                    age = now - value
                    # 30 mins to seconds is 1800
                    if age > 1800:
                        del users[key]

                try:
                    # If author is in the users dictionary then it means his time hasn't expired
                    last_mention_time = users[comment.author.name]
                    now = time.time()
                    cool_down_timer = (last_mention_time + 1800) - now
                    cool_down_timer = cool_down_timer // 60
                    try:
                        comment.author.message("Your cool down timer hasn't expired!",
                                               f"Your cool down timer hasn't expired. You can use bot command after "
                                               f"{cool_down_timer} minutes")
                    except Exception:
                        # if a user has disabled PM from strangers
                        pass
                    continue
                except KeyError:
                    # If user doesn't exist in the dictionary
                    pass

                if 'thank' in comment.body.lower():
                    response = comment.reply(f"BEEP BEEP! [You're welcome, u/{comment.author.name}!]")
                else:
                    response = comment.reply(f"BEEP BEEP! [I give it a {random.randint(0, 100)} out of 100.]")
                response.mod.distinguish(how="yes")
                users[comment.author.name] = time.time()

        except (PrawcoreException, AttributeError):
            # prints traceback
            traceback.print_exc()
            # Sleeps for 10 second
            time.sleep(10)

            # Refreshes the stream
            comment_stream = subreddit.stream.comment(pause_after=-1, skip_existing=True)
            submission_stream = subreddit.stream.submissions(pause_after=-1, skip_existing=True)


if __name__ == '__main__':
    reddit = praw.Reddit('roadrunner_rates', user_agent='RoadRunnerRate by u/is_Fake_Account')
    subreddit = reddit.subreddit('meepmeeproadrunner')
    print("roadrunner_rates is now live!")
    main()
    print("roadrunner_rates has stopped running!")
