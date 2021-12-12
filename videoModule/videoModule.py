from typing import Counter
from PIL import Image,ImageDraw,ImageFont
from utilModule.utilFunc import *
from gtts import gTTS
import cv2
import moviepy.editor as mp

MAX_STR_SIZE = 70
AudioSegment.converter = os.path.join(getCwd(),"bin","ffmpeg")

def createTitleImage(post,i,resourceMap):
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
    savePath = os.path.join(getCwd(),"export",str(post["id"])+"_title.png")
    im.save(savePath)
    resourceMap[post["id"]]['titleImagePath'] = savePath
    # generate images for comment
    for i in range(len(post['postComments'])):
        createCommentImage(post,post['postComments'][i],i,resourceMap)



def createCommentImage(post,comment,i,resourceMap):
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
    savePath = os.path.join(getCwd(),"export",str(post["id"])+"_comment_"+str(i)+".png")
    im.save(savePath)
    # resourceMap[post["id"]]["commentImagePaths"].append(savePath)
    resourceMap[post["id"]]["commentResourcePaths"][comment["id"]] = [savePath]

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

def generateAudiosForPost(post,resourceMap):
    tts = gTTS(post['postTitle'])
    savePath = os.path.join(getCwd(),"export",str(post["id"])+"_title.mp3")
    tts.save(savePath)
    resourceMap[post["id"]]['titleAudioPath'] = savePath
    for i in range(len(post['postComments'])):
        savePath = os.path.join(getCwd(),"export",str(post["id"])+"_comment_"+str(i)+".mp3")
        tts = gTTS(post['postComments'][i]['comment'])
        tts.save(savePath)
        resourceMap[post["id"]]["commentResourcePaths"][post['postComments'][i]["id"]].append(savePath)
        # resourceMap[post["id"]]['commentAudioPaths'].append(savePath)

def generateVideoHelper(video_name,framerate,resourceMap):
    audioFile = AudioSegment.empty()
    generateVideoAndAudio(video_name,framerate,resourceMap,audioFile)

def generateVideoAndAudio(video_name,framerate,resourceMap,audioFile):
    # fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    cv2.VideoWriter()
    video = cv2.VideoWriter(os.path.join(getCwd(), video_name + ".avi"), 0, framerate , (1280, 720))
    for ids in resourceMap.keys():
        titleImagePath = resourceMap[ids]['titleImagePath']
        titleAudioPath = resourceMap[ids]['titleAudioPath']
        titleAudioLength = getAudioLength(titleAudioPath)*framerate
        audioFile = combineAudio(audioFile,titleAudioPath)
        second_of_silence = AudioSegment.silent(duration=1000)
        audioFile = audioFile+second_of_silence
        frame = cv2.imread(titleImagePath)
        for i in range(int(titleAudioLength)):
            video.write(frame)
        
        for i in resourceMap[ids]['commentResourcePaths'].keys():
            commentImagePath = resourceMap[ids]['commentResourcePaths'][i][0]
            commentAudioPath = resourceMap[ids]['commentResourcePaths'][i][1]
            commentAudioLength = getAudioLength(commentAudioPath)*framerate
            frame = cv2.imread(commentImagePath)
            audioFile = combineAudio(audioFile,commentAudioPath)
            audioFile = audioFile+second_of_silence
            for j in range(int(commentAudioLength)):
                video.write(frame)
    video.release()
    audioFile.export(os.path.join(getCwd(), video_name + ".mp3"), format="mp3")
    cv2.destroyAllWindows()


def combineAudioAndVideo(file_name):
    video = mp.VideoFileClip(os.path.join(getCwd(), file_name + ".avi"))
    video.write_videofile(os.path.join(getCwd(), file_name + "_final.mp4"), audio=os.path.join(getCwd(), file_name + ".mp3"))




