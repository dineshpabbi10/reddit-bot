from typing import Counter
from PIL import Image,ImageDraw,ImageFont
from utilModule.utilFunc import *
from gtts import gTTS

MAX_STR_SIZE = 70
def createTitleImage(post,i):
    # convert title to multiline
    multiLineHeader = converToMultiline(post['postTitle'])

    # Load icons
    redditImageIcon = Image.open("staticFiles/redditIcon.png")
    upvoteImageIcon = Image.open("staticFiles/redditUpvote.png")

    # Resize Icons
    redditImageIcon = redditImageIcon.resize((100,100))
    width, height = upvoteImageIcon.size 
    upvoteImageIcon = upvoteImageIcon.resize((width//15,height//15))
    im = Image.new(mode='RGB',size=(1280,720),color=(255,255,255))
    im.paste(redditImageIcon,(10,130)) # 10,240
    im.paste(upvoteImageIcon,(30,60)) # 30,170
    font = ImageFont.truetype("staticFiles/arial.ttf", 34)
    fontTitle = ImageFont.truetype("staticFiles/arial.ttf", 45)
    fontAuthor = ImageFont.truetype("staticFiles/arial.ttf", 16)
    imgDraw = ImageDraw.Draw(im)
    imgDraw.text((120, 150),multiLineHeader,(82,82,82),font=font) # 120,260
    imgDraw.text((130, 130),"author: ",(82,82,82),font=fontAuthor) # 130,240
    imgDraw.text((10, 10),"Post #"+str(i),(82,82,82),font=fontTitle) # 10,10
    imgDraw.text((185, 130),"u/"+str(post['postAuthor']),(0,76,153),font=fontAuthor) # 185,170
    imgDraw.text((130, 60),str(post['postUpvotes']),(82,82,82),font=font) # 130,170
    im.save(os.path.join(getCwd(),"export",str(post["id"])+"_title.png"))
    # generate images for comment
    for i in range(len(post['postComments'])):
        createCommentImage(post,post['postComments'][i],i)



def createCommentImage(post,comment,i):
    # convert title to multiline
    multiLineHeader = converToMultiline(comment['comment'])

    # Load icons
    redditImageIcon = Image.open("staticFiles/redditIcon.png")
    upvoteImageIcon = Image.open("staticFiles/redditUpvote.png")

    # Resize Icons
    redditImageIcon = redditImageIcon.resize((100,100))
    width, height = upvoteImageIcon.size 
    upvoteImageIcon = upvoteImageIcon.resize((width//15,height//15))
    im = Image.new(mode='RGB',size=(1280,720),color=(255,255,255))
    im.paste(redditImageIcon,(10,130))
    im.paste(upvoteImageIcon,(30,60))
    font = ImageFont.truetype("staticFiles/arial.ttf", 34)
    fontTitle = ImageFont.truetype("staticFiles/arial.ttf", 45)
    fontAuthor = ImageFont.truetype("staticFiles/arial.ttf", 16)
    imgDraw = ImageDraw.Draw(im)
    imgDraw.text((120, 150),multiLineHeader,(82,82,82),font=font)
    imgDraw.text((10, 10),"Comment #"+str(i),(82,82,82),font=fontTitle)
    imgDraw.text((130, 130),"author: ",(82,82,82),font=fontAuthor)
    imgDraw.text((185, 130),"u/"+str(comment['commentAuthor']),(0,76,153),font=fontAuthor)
    imgDraw.text((130, 60),str(comment['commentUpvotes']),(82,82,82),font=font)
    im.save(os.path.join(getCwd(),"export",str(post["id"])+"_comment_"+str(i)+".png"))

def converToMultiline(oldString):
    words = oldString.split(" ")
    newString = ""
    newlineCounter = 1
    for i in words:
        newString = newString+" "+i
        if(len(newString)>=MAX_STR_SIZE*newlineCounter):
            newString=newString+"\n"
            newlineCounter=newlineCounter+1
    n = len(oldString)//MAX_STR_SIZE
    for i in range(1,n+1):
        oldString = oldString[:i*MAX_STR_SIZE]+"\n"+oldString[i*MAX_STR_SIZE:]
    return newString

def generateAudiosForPost(post):
    tts = gTTS(post['postTitle'])
    tts.save(os.path.join(getCwd(),"export",str(post["id"])+"_title.mp3"))
    for i in range(len(post['postComments'])):
        tts = gTTS(post['postComments'][i]['comment'])
        tts.save(os.path.join(getCwd(),"export",str(post["id"])+"_comment_"+str(i)+".mp3"))
