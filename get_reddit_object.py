import praw
#make an app here https://www.reddit.com/prefs/apps and then put in the values. This just reads, so you don't need the whole song and dance of getting more permissions.
reddit = praw.Reddit(
        client_id="YOUR CLIENT ID",
        client_secret="YOUR CLIENT SECRET",
        user_agent="meme_scraper",
    )
