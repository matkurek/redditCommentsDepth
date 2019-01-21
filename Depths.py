import praw
import numpy as np
import matplotlib.pyplot as plt

#set your reddit information to enable praw
reddit = praw.Reddit(client_id='',
                     client_secret='',
					 password='',
                     user_agent='',
					 username='')

#top 50 subreddits
listOfSubs = ['funny' ,'AskReddit' ,'todayilearned' ,'science' ,'worldnews' ,'pics' ,'IAmA' ,'gaming' ,'videos' ,'movies' ,'aww' ,'Music' ,'blog' ,'gifs' ,'news' ,'explainlikeimfive' ,'askscience' ,'EarthPorn' ,'books' ,'television' ,'mildlyinteresting' ,'LifeProTips' ,'Showerthoughts' ,'space' ,'DIY' ,'Jokes' ,'gadgets' ,'nottheonion' ,'sports' ,'tifu' ,'food' ,'photoshopbattles' ,'Documentaries' ,'Futurology' ,'history' ,'InternetIsBeautiful' ,'dataisbeautiful' ,'UpliftingNews' ,'listentothis' ,'GetMotivated' ,'personalfinance' ,'OldSchoolCool' ,'philosophy' ,'Art' ,'nosleep' ,'WritingPrompts' ,'creepy' ,'TwoXChromosomes' ,'Fitness' ]

maxDepth = 15
suma_up = [0] * maxDepth
ilosc = [0] * maxDepth
number_of_posts = 0

for sub in listOfSubs:
    print(sub)
    subreddit = reddit.subreddit(sub)
    top_posts = subreddit.top(time_filter='all', limit=30 )

    for submission in top_posts:
        #print(submission.title)
        submission.comments.replace_more(limit=0) #limit=0 żeby tylko jedną paczkę pobierało
        submission.comment_sort = 'best'
        comment_queue = submission.comments[:]  # Seed with top-level [:10] żeby 10 pierwszych
        while comment_queue:
        	comment = comment_queue.pop(0)
        	#print(comment.author, ' ', comment.ups, ' Głębokość: ', comment.depth)
        	suma_up[comment.depth] += comment.ups
        	ilosc[comment.depth] += 1
        	comment_queue.extend(comment.replies)
    print(suma_up)
    print(ilosc)

sum = np.array(suma_up)
qty = np.array(ilosc)
histo = sum/qty
print(histo)


for ile in qty:
    number_of_posts+=ile

# Create scatter plot
plt.scatter(range(0,maxDepth), histo, s=qty * (1000/qty[0]), label='Size translates to quantity')
plt.yscale('log', basey=2)

plt.xticks(np.arange(0, 10, 1))

plt.title('Average upvotes for each comment level depth \n (All Comments until "More comments...")')
plt.xlabel('Comment level depth')
plt.ylabel('Avg. Upvotes')

legend = plt.legend(loc='upper right', shadow=True, fontsize='medium')
legend.get_frame().set_facecolor('ivory')

print(number_of_posts)

plt.show()
