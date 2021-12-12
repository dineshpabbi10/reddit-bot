from typing import Counter
from PIL import Image,ImageDraw,ImageFont
from utilModule.utilFunc import *
from gtts import gTTS

MAX_STR_SIZE = 70
def createSingleImage(post,i):
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
    im.paste(redditImageIcon,(10,240))
    im.paste(upvoteImageIcon,(30,170))
    font = ImageFont.truetype("staticFiles/arial.ttf", 34)
    fontAuthor = ImageFont.truetype("staticFiles/arial.ttf", 16)
    imgDraw = ImageDraw.Draw(im)
    imgDraw.text((120, 260),multiLineHeader,(82,82,82),font=font)
    imgDraw.text((130, 240),"author: ",(82,82,82),font=fontAuthor)
    imgDraw.text((185, 240),"u/"+str(post['postAuthor']),(0,76,153),font=fontAuthor)
    imgDraw.text((130, 170),str(post['postUpvotes']),(82,82,82),font=font)
    im.save(os.path.join(getCwd(),"export",str(i)+"_title.png"))

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
