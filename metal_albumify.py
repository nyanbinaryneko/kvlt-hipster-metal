from PIL import Image
import random
import requests
import time
import os 

DEBUG = os.environ["DEBUG"].lower() == "true"

class AlbumCover:
    def __init__(self, bg_url, logo_path):
        # https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/entities-object#media
        if not DEBUG:
            self.bg = Image.open(requests.get(bg_url, stream=True).raw) #I really don't want to save this on Heroku
        else:
            self.bg = Image.open(bg_url)
        self.logo = Image.open(logo_path)
        self.bg_size = self.bg.size
        self.logo = self.logo.resize(self.resize_logo(25), Image.ANTIALIAS)
        self.logo_size = self.logo.size
        self.logo_placement = self.logo_placement()

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
        return_values = {0:top_right,1:top_left,2:top_center,3:bottom_left,4:bottom_center}
        return return_values.get(rnd,top_right)

    def paste_logo_image(self):
        # img = background_img.convert("L") #transformation()
        self.transform_image()
        path_for_post_to_twitter = f'./corpus/img/output/{time.time()}.jpg'
        self.bg.paste(self.logo, self.logo_placement, self.logo)
        self.bg.save(path_for_post_to_twitter) # save it for debugging\
        return path_for_post_to_twitter

    def transform_image(self):
        self.bg = self.bg.convert("L") # just greyscale it for now.
