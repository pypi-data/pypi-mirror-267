# Onebag

---

I found myself often reusing the same helpers for a lot of my personal projects, so finally decided to gather them all together and make it easier for me to use them anywhere I wanted. The result is this Python package: Onebag

# Installation & Updating

---

Onebag can be installed with pip.
` pip install onebag`

# Usage

---

login_bot --> 
Logs a user into reddit and returns a `praw.reddit` instance.
- `file_path` should be the absolute path to a `login.txt` file.
- `login.txt` should take the following format  
  `<subreddit>:<user_agent>:<id>:<secret>:<refresh_token>`
Explanation of items:
```yaml
subreddit: The subreddit you plan on targeting
user_agent: A general user_agent that Reddit will see. ex. Reddit bot by /u/username
id: At least 14 character string listed under personal user script for desired application
secret: The client secret listed adjacent to secret for the application. Should be at least 27 characters
refresh_token: A generated refresh token. See https://praw.readthedocs.io/en/stable/tutorials/refresh_token.html#refresh-token
```

get_timestamp --> Returns a current timestamp in the `m/dd [hh:mm]` format. Especially useful for logging.


# Contributing

---

Feel free to open an issue if you encounter any bugs or have any major suggestions. Pull Requests are also welcome.
Response times may vary.

# License

---
[MIT](https://choosealicense.com/licenses/mit/)