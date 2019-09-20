from PIL import Image
# how to make graphic design your passion in 5 lines of python after an import statement
"""
foreground_img = Image.open('./corpus/img/testlogo.png') # open test logo
background_img = Image.open('./corpus/img/test.jpg') # open background

background_img.paste(foreground_img, (0,0), foreground_img) # paste her on?
img = background_img.convert("L") #transformation
img.save('./corpus/img/output/out2.jpg') # save it

TODO: same as above with rescaling the image to a percent of original and placing it programmatically instead of stupidly
"""

# lowest hanging fruit is resize and paste in the (0,0) corner. Let's start there

foreground_img = Image.open('./corpus/img/testlogo.png') # open test logo
background_img = Image.open('./corpus/img/test.jpg') # open background

bg_size = background_img.size
fg_size = foreground_img.size
# it aint python without dumbass debugging statements
print(f'background size: {bg_size}')
print(f'foreground size: {fg_size}')
print(f'foreground is {(fg_size[0]/bg_size[0])*100}% of bg width and  {(fg_size[1]/bg_size[1])*100}% of bg height')

# for ease, let's say a logo is always 25% of the total image size, which is 400x400 pixels in this example
target_width = bg_size[0] * 0.25
target_height = bg_size[1] * 0.25

# maintain aspect ratio
resize_width = target_width * (fg_size[0] / fg_size[1])
resize_height = target_height * (fg_size[1] / fg_size[0])

# it aint python without dumbass debugging statements
print(f'background size: {bg_size}')
print(f'foreground size: {fg_size}')
print(f'foreground is {(resize_width/bg_size[0])*100}% of bg width and  {(resize_height/bg_size[1])*100}% of bg height')
"""
background size: (400, 400)
foreground size: (303, 245)
foreground is 75.75% of bg width and  61.25000000000001% of bg height
background size: (400, 400)
foreground size: (303, 245)
foreground is 30.918367346938773% of bg width and  20.214521452145213% of bg height

#yatta
"""
resize = (int(resize_width), int(resize_height)) # cast to int because it yelled at me, and i'm too lazy to figure out floating point shit for perfection

foreground_img = foreground_img.resize(resize, Image.ANTIALIAS)

# background_img.paste(foreground_img, (0,0), foreground_img) # paste her on?
# save without converting this time
# background_img.save('./corpus/img/output/out3.jpg')

"""
resize to aspect ratio done. let's move it to quadrants
metal logos tend to be top right (0.0) ✔️, 
top center (???, 0), 
top left (max - logo_w, 0)✔️,
bottom left (max - logo_w, max_y - logo_h) ✔️, 
and bottom center (???,max_y - logo_h)
lowest hanging fruit is top left.
"""

# top left:
fg_size = foreground_img.size # get the resize from above.
top_left = (bg_size[0] - fg_size[0], 0) # should be right...or left?
# background_img.paste(foreground_img, top_left, foreground_img) # paste her on?
# save without converting this time
# background_img.save('./corpus/img/output/out4.jpg')

# bottom left:
bottom_left = (bg_size[0] - fg_size[0], bg_size[1] - fg_size[1])
background_img.paste(foreground_img, bottom_left, foreground_img) # paste her on?
# save without converting this time
background_img.save('./corpus/img/output/out5.jpg')


