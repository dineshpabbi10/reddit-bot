import os

def getCwd():
    return os.getcwd()

def createFolder(root,name):
    if not os.path.exists(os.path.join(root,name)):
        os.makedirs(os.path.join(root,name))
