from PIL import Image
import random
import requests
import time
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
"""
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
"""
background size: (400, 400)
foreground size: (303, 245)
foreground is 75.75% of bg width and  61.25000000000001% of bg height
background size: (400, 400)
foreground size: (303, 245)
foreground is 30.918367346938773% of bg width and  20.214521452145213% of bg height

#yatta
"""
"""
resize = (int(resize_width), int(resize_height)) # cast to int because it yelled at me, and i'm too lazy to figure out floating point shit for perfection

foreground_img = foreground_img.resize(resize, Image.ANTIALIAS)

# background_img.paste(foreground_img, (0,0), foreground_img) # paste her on?
# save without converting this time
# background_img.save('./corpus/img/output/out3.jpg')
"""
"""
resize to aspect ratio done. let's move it to quadrants
metal logos tend to be top right (0.0) ✔️, 
top center (???, 0), 
top left (max - logo_w, 0)✔️,
bottom left (max - logo_w, max_y - logo_h) ✔️, 
and bottom center (???,max_y - logo_h)
lowest hanging fruit is top left.
"""
"""
# top left:
fg_size = foreground_img.size # get the resize from above.
top_left = (bg_size[0] - fg_size[0], 0) # should be right...or left?
# background_img.paste(foreground_img, top_left, foreground_img) # paste her on?
# save without converting this time
# background_img.save('./corpus/img/output/out4.jpg')

# bottom left:
bottom = bg_size[1] - fg_size[1]
bottom_left = (bg_size[0] - fg_size[0], bottom)
# background_img.paste(foreground_img, bottom_left, foreground_img) # paste her on?
# save without converting this time
# background_img.save('./corpus/img/output/out5.jpg')

# top center:
center_width = (bg_size[0]  / 2) - (fg_size[0] / 2)
top_center = (int(center_width), 0)
# background_img.paste(foreground_img, top_center, foreground_img) # paste her on?
# save without converting this time
# background_img.save('./corpus/img/output/out6.jpg')

# bottom center
top_center = (int(center_width), bottom)
# background_img.paste(foreground_img, top_center, foreground_img) # paste her on?
# save without converting this time
# background_img.save('./corpus/img/output/out7.jpg')
"""
"""
TODO: refactor into a general manipulations, figure out deep frying
"""

class AlbumCover:
    def __int__(self, bg_url, logo_path):
        # https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/entities-object#media
        self.bg = Image.open(requests.get(bg_url, stream=True).raw) #I really don't want to save this on Heroku
        self.logo = Image.open(logo_path)
        self.bg_size = self.bg.size
        self.logo = self.logo.resize(resize_logo(25), Image.ANTIALIAS)
        self.logo_size = self.logo.size
        self.logo_placement = logo_placement()
    
        def resize_logo(self, percent):
            target_width = self.bg_size[0] * (percent / 100)
            target_height = self.bg_size[1] * (percent / 100)
            # maintain aspect ratio
            resize_width = target_width * (self.logo.size[0] / self.logo.size[1])
            resize_height = target_height * (self.logo.size[1] / self.logo.size[0])
            return (int(resize_width), int(resize_height))

        def logo_placement(self):
            # basic calcs
            top_right = (0, 0)
            bottom = self.bg_size[1] - self.logo_size[1]
            center_width = (self.bg_size[0]  / 2) - (self.logo_size[0] / 2)
            left = self.bg_size[0] - self.logo_size[0]
            # top left:
            top_left = (left, 0)
            # bottom left:
            bottom_left = (left, bottom)
            # top center:
            top_center = (int(center_width), 0)
            # bottom center
            bottom_center = (int(center_width), bottom)
            rnd = random.randint(0, 4) # get random int between 0 and 4.
            if rnd == 0:
                return top_right
            elif rnd == 1:
                return top_left
            elif rnd == 2:
                return top_center
            elif rnd == 3:
                return bottom_left
            elif rnd == 4:
                return bottom_center
            return top_right
    
    def paste_logo_image(self):
        # img = background_img.convert("L") #transformation()
        self.transform_image()
        path_for_post_to_twitter = f'./corpus/img/output/{time.time()}.jpg'
        self.bg.paste(self.logo, self.logo_placement, self.logo)
        self.bg.save(path_for_post_to_twitter) # save it for debugging\
        return path_for_post_to_twitter
    
    def transform_image(self):
        self.bg = self.bg.convert("L") # just greyscale it for now.
