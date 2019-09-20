from PIL import Image
forground_img = Image.open('./corpus/img/testlogo.png') # open test logo
background_img = Image.open('./corpus/img/test.jpg') # open background

background_img.paste(forground_img, (0,0), forground_img) # paste her on?
img = background_img.convert("L") #transformation
img.save('./corpus/img/output/out2.jpg')

