from redditModule.redditModule import getConfigObject,getRedditObject,getTopPosts,getPostFormattedObject
from videoModule.videoModule import createTitleImage,generateAudiosForPost,generateVideoAndAudio,combineAudioAndVideo,generateVideoHelper
from utilModule.utilFunc import createFolder,getCwd,cleanDirectory
from tqdm import tqdm

config = getConfigObject()
redditObject = getRedditObject()
resourceMap = {}

print("1. Fetching Top Posts from subreddit: "+config['redditConfig']['subReddit'])
topPosts = getTopPosts(config['redditConfig']['subReddit'],redditObject,config['redditConfig']['duration'])

formattedPostObjects = []

print("2. Creating folder to generate resources")
createFolder(getCwd(),"export")

print("3. Processing Fetched Data")
posts = []
for submission in topPosts:
    posts.append(submission)

for i in tqdm(range(len(posts))):
    if posts[i].score>config['redditConfig']['score']:
        post = getPostFormattedObject(posts[i],
                config['redditConfig']['numberOfComments'],
                config['redditConfig']['getPostContent'])
        if(len(post["postTitle"]) > config['redditConfig']['postLength']):
            pass
        else:
            if(config['redditConfig']['getPostImage'] == True):
                url = post["url"]
                if url.endswith("jpg") or url.endswith("jpeg") or url.endswith("png"):
                    formattedPostObjects.append(post)
                else:
                    
                    pass
            else:
                formattedPostObjects.append(post)

for submission in formattedPostObjects:
     resourceMap[submission["id"]] = {
        "titleImagePath":"",
        "commentImagePaths":[],
        "titleAudioPath":"",
        "commentAudioPaths":[],
        "commentResourcePaths":{}
    }

print("4. Creating Images for Submissions")
for i in tqdm(range(len(formattedPostObjects))):
    createTitleImage(formattedPostObjects[i],i,resourceMap,config['redditConfig']['getPostImage'],config['redditConfig']['getPostContent'])

print("5. TODO : Creating audio files for submissions")
for i in tqdm(range(len(formattedPostObjects))):
    generateAudiosForPost(formattedPostObjects[i],resourceMap)

print("6. TODO : Combining Generated resources into one video")
generateVideoHelper("output1",10,resourceMap,config['redditConfig']['titleSilenceDuration'])
combineAudioAndVideo("output1")

print("7. TODO : Cleaning up redundant generated resources")
cleanDirectory("output1")