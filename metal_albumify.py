from PIL import Image
import numpy as np 
from scipy.ndimage import filters
from scipy import misc
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
        # path_for_post_to_twitter = f'./corpus/img/output/{time.time()}.jpg'
        # self.bg.paste(self.logo, self.logo_placement, self.logo)
        # self.bg.save(path_for_post_to_twitter) # save it for debugging\
        self.bg.save("./corpus/img/output/out_test_speckle.jpg")
        return "./corpus/img/output/out_test_speckle.jpg"
        # return path_for_post_to_twitter

    def transform_image(self):
        # self.gaussian_noise()
        # self.salt_n_pepper()
        # self.poisson()
        # self.speckle_noise()
        # self.bg = self.bg.convert("L") # just greyscale it for now.

    # noise transformers
    def gaussian_noise(self):
        img = self.bg_to_nparray()
        row, col, ch = img.shape
        mean = 0.0 # ???
        var = 10 # adjust this for FRYING LEVEL, originally 0.01
        sigma = var**0.5 # ???
        gauss = np.array(img.shape)
        gauss = np.random.normal(mean, sigma,(row, col, ch))
        gauss = gauss.reshape(row, col, ch)
        noisy = img + gauss
        self.nparray_to_bg(noisy.astype('uint8'))

    def salt_n_pepper(self):
        image = self.bg_to_nparray()
        s_vs_p = 0.5 # salt vs pepper rate????
        amount = 0.004 # fry amount
        out = image
        # Generate Salt '1' noise
        num_salt = np.ceil(amount * image.size * s_vs_p)
        coords = [np.random.randint(0, i - 1, int(num_salt))
            for i in image.shape]
        out[coords] = 255
        # Generate Pepper '0' noise
        num_pepper = np.ceil(amount* image.size * (1. - s_vs_p))
        coords = [np.random.randint(0, i - 1, int(num_pepper))
            for i in image.shape]
        out[coords] = 0
        self.nparray_to_bg(out)
    
    def poisson(self):
        image = self.bg_to_nparray()
        vals = len(np.unique(image))
        vals = 2 ** np.ceil(np.log2(vals))
        noisy = np.random.poisson(image * vals) / float(vals)
        # print(type(noisy))
        self.nparray_to_bg(noisy.astype('uint8'))

    def speckle_noise(self):
        image = self.bg_to_nparray()
        row, col, ch = image.shape
        gauss = np.random.randn(row,col,ch)
        gauss = gauss.reshape(row,col,ch)        
        noisy = image + image * gauss
        return self.nparray_to_bg(noisy.astype('uint8'))

    # helpers. written out to convert between the libs for image manipulation
    def bg_to_nparray(self):
        return np.array(self.bg)
    
    def nparray_to_bg(self, arr):
        self.bg = Image.fromarray(arr)
