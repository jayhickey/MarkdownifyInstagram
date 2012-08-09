#  
#   MARKDOWNIFY INSTAGRAM
#
#   Markdownify Instagram pairs with an IFTTT recipe to automatically create an embedded Instagram markdown post
#   
#   Use the recipe found here: http://ifttt.com/myrecipes/personal/1541166/share
#
#   Inputs: {{IFTTT_Read_Path}}, {{Draft_Write_Path}}, {{Local_Image_URL_Path}}, {{Website}}
#   Example: python MarkdownifyInstagram.py /home/blog/secondcrack/www/media/instagram/ /home/blog/Dropbox/Blog/drafts/ /media/instagram/ http://jayhickey.com

import os
import sys
import re 
import glob
import urllib
from time import localtime, strftime

def read_file(file):
    # Check for filename for Instagram file from IFTTT
    f = open("%s" % (files), mode="r")
    fileLines = f.readlines()
    fileDict = {}

    # Create a dictionary with the Instagram info
    for line in fileLines:
        x = re.search(r'([\w\@\.]+)\s*:\s*(.*)', line)
        if x != None:
            fileDict[x.group(1)] = x.group(2)
    f.close()
    return fileDict

def create_draft(fileDict, draftLoc, localImg):
    
    # Embed the photo with markdown
    draft = open(draftLoc + "/%s.md" % (fileDict['Caption']), mode="w")
    draft.write(fileDict['Caption'] + '\n')
    draft.write("=====================\n")
    draft.write("Link: %s" % (fileDict['URL']) + "\n")
    draft.write("publish-not-yet\n\n")
    print localImg
    draft.write("![%(1)s](%(2)s)\n\n" % {"1" : fileDict['Caption'], "2" : localImg})
    #draft.write("%s\n\n" % fileDict['Caption'])
    draft.write("(Via [Instagram](http://instagram.com))")
    draft.close()


if __name__ == '__main__':

    Local_Image_URL_Path = ''
    Website = ''

    IFTTT_Read_Path = sys.argv[1]

    Draft_Write_Path = sys.argv[2]

    # These parameters are optional
    if len(sys.argv) >= 4:
        Local_Image_URL_Path = sys.argv[3]
    if len(sys.argv) == 5:
        Website = sys.argv[4]

    fileList = glob.glob(IFTTT_Read_Path + '*instagr.am*.txt')
    
    for files in fileList:

        # Read the Instagram data
        fileDict = read_file(files)

        if Local_Image_URL_Path != '' or Website != '':
            # Make a local copy of the image (dated)
            image = urllib.URLopener()
            eventTime = strftime("%Y-%m-%d_%I%M%S", localtime())
            fileName, fileExtension = os.path.splitext(fileDict['Source'])
            localImgPath = IFTTT_Read_Path + eventTime + fileExtension
            image.retrieve(fileDict['Source'], localImgPath)
            imgURL = Website + Local_Image_URL_Path + eventTime + fileExtension
        else:
            imgURL = fileDict['Source']

        # Create a markdown draft
        create_draft(fileDict, Draft_Write_Path, imgURL)
        
        # Delete the Instagram text file from IFTTT
        os.remove(files)
