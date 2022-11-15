# Crypto_Bot
from sklearn import tree
import imageio.v3 as iio

im1 = iio.imread('melon1.png')
im2 = iio.imread('melon2.png')

image = [[im1], [im2]]
info = ["Cartoon", "Real"]

classifier = tree.DecisionTreeClassifier()
classifier = classifier.fit(image, info)
print(*classifier.predict([[iio.imread(input())]]))
