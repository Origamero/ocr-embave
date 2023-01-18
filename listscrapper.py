from collections import defaultdict
from PIL import Image
from dotenv import dotenv_values
from directoryscanner import getCover, get_lists
# will convert the image to text string
import pytesseract

from models import Result, User, check_user
config = dotenv_values(".env")

def get_image_as_text(photo_path):
  pytesseract.pytesseract.tesseract_cmd = config['TESSERACT_PATH']
  img = Image.open(photo_path)
  text = pytesseract.image_to_string(img)
  return text

def search(user: User):
  lists = get_lists()
  for folder, photos in lists.items():
    for photo in photos:
      photo_path = r"%s\%s" % (folder, photo)
      text = get_image_as_text(photo_path)
      lines = text.split('\n')
      for line in lines:
        if(check_user(user, line)):
          result = Result(listInfo=lines[0],row=line,cover=get_image_as_text(getCover(folder)))
          return result

          