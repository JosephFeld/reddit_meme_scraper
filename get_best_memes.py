import praw
import requests
import mimetypes
import os
from get_reddit_object import reddit # contains my client secret and stuff

def create_directory(path):
    """
    Creates a new directory at the given path.
    If the directory already exists, it does nothing.

    Parameters:
        path (str): The path of the directory to create.
    """
    try:
        os.makedirs(path, exist_ok=True)
        print(f"Directory created (or already exists): {path}")
    except Exception as e:
        print(f"Error creating directory '{path}': {e}")



def download_image_auto_extension(url, base_filename):
  """
  From Gemini:

  Downloads an image from the given URL, automatically determining the extension.

  Args:
    url (str): The URL of the image to download.
    base_filename (str): The desired base filename (without extension).
  """

  filename = 'blank.png'

  try:
    response = requests.get(url)
    if response.status_code == 200:
      content_type = response.headers.get('Content-Type')

      if content_type:
        extension = mimetypes.guess_extension(content_type)
        if extension:
          filename = f"{base_filename}{extension}"
        else:
          print(f"Warning: Could not determine extension for Content-Type: {content_type}. Saving as {base_filename}")
          filename = base_filename
      else:
        print(f"Warning: No Content-Type header found. Saving as {base_filename}")
        filename = base_filename

      with open(filename, "wb") as f:
        f.write(response.content)
      print(f"Image downloaded successfully: {filename}")
    else:
      print(f"Failed to download image. Status code: {response.status_code}")

  except requests.exceptions.RequestException as e:
    print(f"Error downloading image: {e}")

  return filename

def get_best_memes(folder, subreddits = ['me_irl', 'dankmemes', 'pics', '196']):
    create_directory(folder)

    submissions = []
  
    for subreddit in subreddits:
        for submission in reddit.subreddit(subreddit).top(limit=2, time_filter='day'):
          if "text/html;" not in submission.url:
              filename = download_image_auto_extension(submission.url, f"{folder}/{submission.id}")
              submission.output_filename = filename
          else:
              submission.output_filename = "blank.png"

          submissions.append(submission)

    return submissions


