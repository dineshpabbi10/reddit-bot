from redditModule.redditModule import getConfigObject,getRedditObject,getTopPosts,getPostFormattedObject
from videoModule.videoModule import createTitleImage,generateAudiosForPost
from utilModule.utilFunc import createFolder,getCwd
from tqdm import tqdm

config = getConfigObject()
redditObject = getRedditObject()

print("1. Fetching Top Posts from subreddit: "+config['redditConfig']['subReddit'])
topPosts = getTopPosts(config['redditConfig']['subReddit'],redditObject)

formattedPostObjects = []

print("2. Creating folder to generate resources")
createFolder(getCwd(),"export")

print("3. Processing Fetched Data")
posts = []
for submission in topPosts:
    posts.append(submission)

for i in tqdm(range(len(posts))):
    if posts[i].score>8000:
        formattedPostObjects.append(getPostFormattedObject(posts[i]))

print("4. Creating Images for Submissions")
for i in tqdm(range(len(formattedPostObjects))):
    createTitleImage(formattedPostObjects[i],i)

print("5. TODO : Creating audio files for submissions")
for i in tqdm(range(len(formattedPostObjects))):
    generateAudiosForPost(formattedPostObjects[i])

print("6. TODO : Combining Generated resources into one video")

print("7. TODO : Cleaning up redundant generated resources")
