import datetime
import os
from time import sleep
import praw


def get_timestamp():
    """
    Returns the current timestamp for logging
    :return: timestamp: Format of m/dd [hh:mm]
    """
    dt = str(datetime.datetime.now().month) + '/' + str(datetime.datetime.now().day) + ' '
    hr = str(datetime.datetime.now().hour) if len(str(datetime.datetime.now().hour)) > 1 else '0' + str(
        datetime.datetime.now().hour)
    minute = str(datetime.datetime.now().minute) if len(str(datetime.datetime.now().minute)) > 1 else '0' + str(
        datetime.datetime.now().minute)
    t = '[' + hr + ':' + minute + '] '
    return dt + t


def login_bot(file_path: str) -> tuple[praw.Reddit, str]:
    """
    Create a reddit instance from login.txt
    The login.txt file must follow this format: <subreddit>:<user_agent>:<id>:<secret>:<refresh_token>
    :param file_path: path to your login.txt file.
    :return: (reddit instance, subreddit to use)

    """
    try:
        f = open(os.path.join(file_path, 'login.txt'), 'r')
        subreddit, user_agent, client_id, secret, refresh = f.readline().split('||', 5)
        f.close()
        r = praw.Reddit(client_id=client_id,
                        client_secret=secret,
                        refresh_token=refresh.strip(),
                        user_agent=user_agent)

        print(get_timestamp() + "OAuth session opened as /u/" + r.user.me().name)
    except Exception as e:
        print(get_timestamp() + str(e))
        print(get_timestamp() + "Setup error in Results \n")
        sleep(1)
        exit()

    return r, subreddit
