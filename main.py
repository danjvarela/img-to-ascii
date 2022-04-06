"""
A program that converts image, converts it into ascii characters and outputs it as a text file.
"""

from PIL import Image
import numpy as np
from datetime import datetime

# grayscale density in string
asciiChars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1\{\}[]?-_+~<>i!lI;:,\"^`'. "

"""
Modify the resolution and the file path to your liking.
html output will be under the outputs directory.
"""
# output image resolution
imgResolution = 100
# image directory string
filepath = 'sample_inputs/saitama.png'

# converts each pixel value to ascii character
def convertToString(pixel_values):
  # initialize empty 2d string array
  strArr = np.empty((pixel_values.shape[0], pixel_values.shape[1]), dtype=str)
  for i in range(pixel_values.shape[0]):
    for j in range(pixel_values.shape[1]):
      # calculate the grayscale value
      grayScale = 0.21 * pixel_values[i, j, 0] + 0.72 * pixel_values[i, j, 1] + 0.07 * pixel_values[i, j, 2]
      # calculate the index
      index = int(grayScale * len(asciiChars) / 255) - 1
      ascii = asciiChars[index]
      # account for html entities
      if ascii == ' ':
        ascii = '&nbsp;'
      elif ascii == '>':
        ascii = '&gt;'
      elif ascii == '<':
        ascii = '&lt;'
      elif ascii == '&':
        ascii = '&amp;'
      elif ascii == '"':
        ascii = '&quot;'
      elif ascii == '\'':
        ascii = '&#39;'
      elif ascii == '`':
        ascii = '&#96;'
      # parse the ascii character
      strArr[i, j] = ascii
  return strArr


def main():
  img = Image.open(filepath).convert("RGB")

  # get img actual width and height
  width, height = img.size
  maxWidth = width
  maxHeight = height

  # adjust image size
  if width > imgResolution and height > imgResolution:
    if width < height:
      maxWidth = imgResolution
      maxHeight = int(height * imgResolution / width)
    else:
      maxHeight = imgResolution
      maxWidth = int(width * imgResolution / height)
  elif width > imgResolution:
    maxWidth = imgResolution
    maxHeight = int(height * imgResolution / width)
  elif height > imgResolution:
    maxHeight = imgResolution
    maxWidth = int(width * imgResolution / height)

  img = img.resize((maxWidth, maxHeight), Image.Resampling.LANCZOS)  # resize the image

  # get the rgb values of each pixel
  pxl_values = list(img.getdata())

  # convert to 3D numpy array
  pxl_values = np.array(pxl_values).reshape((maxHeight, maxWidth, 3))

  # convert to ascii characters using the numberToAscii function
  ascii_img = convertToString(pxl_values)

  # accumulate everything into one string
  img_string = '<br>\n'.join([''.join(row) for row in ascii_img])

  # file name according to current date and time
  date_string = datetime.now().strftime("%d-%m-%Y-%H:%M:%S")

  # html templete
  htmltemplate = f'<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<meta http-equiv="X-UA-Compatible" content="IE=edge">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<link rel="stylesheet" href="style.css">\n<title>Document</title>\n</head>\n<body>\n{img_string}\n</body>\n</html>'

  # write to an html file
  with open('outputs/' + date_string + '.html', 'w') as f:
    f.write(htmltemplate)


if __name__ == '__main__':
  main()
