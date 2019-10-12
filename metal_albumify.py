from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import numpy as np 
from scipy.ndimage import filters
from scipy import misc, ndimage
import random
import requests
import time
import os 
import math
import cv2

DEBUG = os.environ["DEBUG"].lower() == "true"

class AlbumCover:
    def __init__(self, bg_url, logo_path):
        # https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/entities-object#media
        if not DEBUG:
            self.bg = Image.open(requests.get(bg_url, stream=True).raw) #I really don't want to save this on Heroku
        else:
            self.bg = Image.open(bg_url)
        self.bg = self.resize(self.bg)
        self.logo = Image.open(logo_path)
        self.bg_size = self.bg.size
        self.logo = self.resize(self.logo, self.resize_logo(25))
        self.logo_size = self.logo.size

    def resize_logo(self, percent):
        target_width = self.bg_size[0] * percent / 100
        target_height = self.bg_size[1] * percent / 100
        # maintain aspect ratio
        resize_width = target_width * self.logo.size[0] / self.logo.size[1]
        resize_height = target_height * self.logo.size[1] / self.logo.size[0]
        return (int(resize_width), int(resize_height))

    def logo_placement(self):
        # basic calcs
        top_right = (0, 0)
        bottom = self.bg_size[1] - self.logo_size[1]
        center_width = (self.bg_size[0]  / 2) - (self.logo_size[0] / 2)
        left = self.bg_size[0] - self.logo_size[0]
        print(f'left: {left}')
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
        path_for_post_to_twitter = f'./corpus/img/output/test_out/{time.time()}.png'
        self.bg.paste(self.logo, self.logo_placement(), self.logo)
        self.bg.save(path_for_post_to_twitter) # save it for debugging\
        # cv2.imwrite(f'{path_for_post_to_twitter}.cv2.png', self.bg_cv2)
        return path_for_post_to_twitter

    def transform_image(self):
        # i think the workflow here should be:
        # enhance/dehance a random number of times.
        # add noise a random number of times.
        # enhance/dehance
        # fry = random.randint(1, 6)
        # print(f'fry = {fry}')
        # for x in range(0, fry):
        #     print(x)
        #     enhance = random.randint(0,5)
        #     print(f'enhance = {enhance}')
        #     enhanced = {0:self.saturate, 1:self.desaturate, 2:self.sharpen, 3:self.blur, 4:self.brighten, 5:self.darken}.get(enhance, self.bg)
        #     enhanced()

        # # add noise
        # fry = random.randint(1, 3)
        # for y in range(0, fry):
        #     print(y)
        #     noise = random.randint(0,2) #speckle just adds too much noise
        #     print(f'noise = {noise}')
        #     noisy = {0:self.gaussian_noise, 1:self.salt_n_pepper, 2:self.poisson, 3:self.speckle_noise}.get(noise, self.bg)
        #     noisy()
        # self.sharpen()
        # self.posterize()
        # self.solarize()
        # self.sobel()
        self.cellshade()
        # self.bg = self.bg.convert("L") # just greyscale it for now.

    # noise transformers
    def gaussian_noise(self):
        img = self.bg_to_nparray()
        row, col, ch = img.shape
        mean = 0.0 # ???
        var = round(random.uniform(0.01, 0.1), 2) # adjust this for FRYING LEVEL, originally 0.01
        print(f'adding gaussian noise with a var of {var}')
        sigma = var**0.5 # ???
        gauss = np.array(img.shape)
        gauss = np.random.normal(mean, sigma,(row, col, ch))
        gauss = gauss.reshape(row, col, ch)
        noisy = img + gauss
        self.nparray_to_bg(noisy.astype('uint8'))

    def salt_n_pepper(self):
        print(f'adding salt n pepper')
        image = self.bg_to_nparray()
        s_vs_p = 0.5 # salt vs pepper rate????
        amount = round(random.uniform(0.01, 1), 2) # fry amount
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
        print(f'adding poisson')
        image = self.bg_to_nparray()
        vals = len(np.unique(image))
        vals = 2 ** np.ceil(np.log2(vals))
        noisy = np.random.poisson(image * vals) / float(vals)
        self.nparray_to_bg(noisy.astype('uint8'))

    def speckle_noise(self):
        print(f'adding speckle')
        image = self.bg_to_nparray()
        row, col, ch = image.shape
        gauss = np.random.randn(row,col,ch)
        gauss = gauss.reshape(row,col,ch)        
        noisy = image + image * gauss
        self.nparray_to_bg(noisy.astype('uint8'))

    # enhancers
    def saturate(self):
        print("saturating")
        enhancer = ImageEnhance.Contrast(self.bg)
        self.bg = enhancer.enhance(round(random.uniform(1.0, 2.0), 1))
    
    def desaturate(self):
        print("desaturating")
        enhancer = ImageEnhance.Contrast(self.bg)
        self.bg = enhancer.enhance(round(random.uniform(0.3, 1.0), 1))
    
    def sharpen(self):
        print("sharpening")
        enhancer = ImageEnhance.Sharpness(self.bg)
        self.bg = enhancer.enhance(round(random.uniform(1.0, 2.0), 1))

    def blur(self):
        print("blurring")
        enhancer = ImageEnhance.Sharpness(self.bg)
        self.bg = enhancer.enhance(round(random.uniform(0.2, 1.0), 1))

    def brighten(self):
        print("brightening")
        enhancer = ImageEnhance.Sharpness(self.bg)
        self.bg = enhancer.enhance(round(random.uniform(1.0, 2.0), 2))
    
    def darken(self):
        print("darkening")
        enhancer = ImageEnhance.Sharpness(self.bg)
        self.bg = enhancer.enhance(round(random.uniform(0.3, 1.0), 2))

    # filters
    def sobel(self):
        self.nparray_to_bg(ndimage.sobel(self.bg))
    
    def color_mask(self):
        c = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        alpha = random.randint(100, 255) #0 is fully opaque, the mask shouldn't engulf the image
        color = Image.new('RGB', self.bg_size, c)
        mask = Image.new('RGBA', self.bg_size, (0,0,0, alpha))
        print(f'placing mask with color {c} and alpha {alpha} over bg')
        self.bg = Image.composite(self.bg, color, mask).convert()

    # transformers
    # cellshading
    def cellshade(self):
        img_color = self.flatten_colors()
        img_edge = self.map_edges(img_color)

        #combine color img with edge mask
        img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2RGB)
        img = cv2.bitwise_and(img_color, img_edge)

        arr = self.bgr_to_rgb(img)
        self.nparray_to_bg(arr)
        # needs to be resized again, converting between pil and cv2 messes with sizing
        self.bg = self.resize(self.bg)

    def flatten_colors(self, downsampling=1, bilateral=2):
        # this seems to be the sweet spot for consistently getting a very "cartoony look"
        number_downsampling = 1 # downsampling
        number_bilateral = 2 # bilateral filtering
        img_color = self.rgb_to_bgr()

        # both of these "flatten" the colors in the img to give it that cartoon look
        # downsample using gaussian pyramid -- look up what the fuck this is
        for _ in range(number_downsampling):
            img_color = cv2.pyrDown(img_color)

        # apply small bilateral filters, over one large one to give it more 
        # cell shaded look
        for _ in range(number_bilateral):
            img_color = cv2.pyrUp(img_color)
        return img_color

    def map_edges(self, img_color):
        # this smooths out some of the noise added by the downsamply and bilateral filtering
        # median filter to reduce noise
        img_grey = cv2.cvtColor(img_color, cv2.COLOR_RGB2GRAY)
        img_blur = cv2.medianBlur(img_grey, 7) #figure out what this number here does

        #use threshholding to create an edge mask, enhance edges
        # figure out what blocksize and C do
        img_edge = cv2.adaptiveThreshold(img_blur, 255,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY,
            blockSize=9,
            C=2)
        return img_edge

    # deep dream fuckery call will go here once i do it.

    # helpers. written out to convert between the libs for image manipulation
    def resize(self, img, dim=(400,400)):
        print(f'dim: {dim}')
        return img.resize(dim, Image.ANTIALIAS)

    def bg_to_nparray(self):
        return np.array(self.bg)
    
    def nparray_to_bg(self, arr):
        img = Image.fromarray(arr)
        img.convert('RGB')
        self.bg = img

    def rgb_to_bgr(self):
        return cv2.cvtColor(self.bg_to_nparray(), cv2.COLOR_RGB2BGR)
    
    def bgr_to_rgb(self, cv_img):
        return cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    
    # pillow wrappers
    def posterize(self):
        rand = random.randint(1,4)
        print(f'posterizing to {rand} channels')
        self.bg = ImageOps.posterize(self.bg, rand)
    
    def solarize(self):
        rand = random.randint(0, 128)
        print(f'solarizing by inverting all pixels above {rand}.')
        self.bg = ImageOps.solarize(self.bg, rand)