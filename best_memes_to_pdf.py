from make_pdf import *
from get_best_memes import *
from datetime import datetime

def format_submission_text(submission):
    title = submission.title
    caption = f"""r/{submission.subreddit.display_name}: u/{submission.author.name}
{submission.selftext}"""
    image = submission.output_filename
    return (title,caption,image)

#SETTINGS==========
subreddits = ['me_irl', 'dankmemes', 'pics', '196', 'news', 'wholesomememes']
output_folder = "outputs"

#=============

create_directory(output_folder)

timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
memes_folder = f"{output_folder}/{timestamp}"

best_memes = get_best_memes(memes_folder, subreddits=subreddits)

c = get_canvas(f"{output_folder}/{timestamp}.pdf")

for i in range(0,len(best_memes)-1,2):
    print(i)
    t1,c1,i1 = format_submission_text(best_memes[i])
    t2,c2,i2 = format_submission_text(best_memes[i+1])
    
    
    draw_page(c, [i1,i2], [t1,t2], [c1,c2])

save_pdf(c)
print("Saved!")
