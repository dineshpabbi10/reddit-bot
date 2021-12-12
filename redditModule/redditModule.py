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

def getTopPosts(subredditName,redditObject):
    # the subreddits you want your bot to live on
    subreddit = redditObject.subreddit(subredditName)
    topPosts = subreddit.top('day')
    return topPosts

def getPostTitle(post):
    return post.title

def getPostComments(post):
    post.comment_sort = 'top'
    allComments = post.comments
    formattedComments = []
    for comment in allComments:
        # Only add at most 10 comments
        if(len(formattedComments)>10):
            break

        formattedComment = comment.body
        # Only look for comments which have length of text at most 1100 characters
        if(len(formattedComment)>1100):
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
                'commentAuther':authorName,
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

def getPostFormattedObject(post):
    return {
        "postTitle":getPostTitle(post),
        "postAuthor":getPostAuthor(post),
        "postUpvotes":getPostUpvotes(post),
        "postCommentNumber":getPostCommentNumber(post),
        "postComments":getPostComments(post)
    }
        