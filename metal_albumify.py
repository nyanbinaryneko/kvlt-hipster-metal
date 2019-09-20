from PIL import Image
img = Image.open('./corpus/img/test.jpg').convert('L')
img.save('./corpus/img/output/out1.jpg')