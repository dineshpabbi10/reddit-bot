import json
import praw

def getConfigObject():
    f = open('Config.json',"r")
    data = json.load(f)
    f.close()
    return data


def getRedditObject():
    config = getConfigObject()['redditConfig']
    reddit = praw.Reddit(
        client_id=config["client_id"],
        client_secret=config["client_secret"],
        password=config["password"],
        user_agent="test",
        username=config["username"]
    )
    return reddit

def getTopPosts(subredditName,redditObject,duration):
    # the subreddits you want your bot to live on
    subreddit = redditObject.subreddit(subredditName)
    topPosts = subreddit.top(duration)
    return topPosts

def getPostTitle(post,getPostContent):
    if(getPostContent):
        content = post.title+" : "+post.selftext
    else:
        content  = post.title

    return content

def getPostComments(post,numOfComments):
    post.comment_sort = 'top'
    allComments = post.comments
    formattedComments = []
    for comment in allComments:
        # Only add at most 10 comments
        if(len(formattedComments)>=numOfComments):
            break

        formattedComment = comment.body
        # Only look for comments which have length of text at most 1100 characters
        if(len(formattedComment)>800):
            pass
        else:

            try:
                authorName = comment.author.name
            except Exception as e:
                authorName = "<deleted>"

            try:
                upvotes = comment.score
            except Exception as e:
                upvotes = '<unavailable>'

            formattedComments.append({
                'id':comment.id,
                'commentAuthor':authorName,
                'comment':formattedComment,
                'commentUpvotes':upvotes
            })

    return formattedComments

def getPostAuthor(post):
    try :
        author = post.author
    except Exception as e:
        author = "<deleted>"
    return author

def getPostUpvotes(post):
    return post.score

def getPostCommentNumber(post):
    return post.num_comments

def getPostId(post):
    return post.id

def getPostUrl(post):
    return post.url

def getPostContent(post):
    return post.selftext


def getPostFormattedObject(post,numOfComments,getPostContentVar):
    return {
        "id":getPostId(post),
        "url":getPostUrl(post),
        "postTitle":getPostTitle(post,getPostContentVar),
        "postContent":getPostContent(post),
        "postAuthor":getPostAuthor(post),
        "postUpvotes":getPostUpvotes(post),
        "postCommentNumber":getPostCommentNumber(post),
        "postComments":getPostComments(post,numOfComments)
    }
        