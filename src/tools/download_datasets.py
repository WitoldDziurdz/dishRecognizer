import wget

caltech_256_url = 'http://www.vision.caltech.edu/Image_Datasets/Caltech256/256_ObjectCategories.tar'
food_11k_url = 'http://grebvm2.epfl.ch/lin/food/Food-11.zip'
food-101_url = 'http://data.vision.ee.ethz.ch/cvl/food-101.tar.gz'

wget.download(caltech_256_url)
wget.download(food_11k_url)
wget.download(food-101_url)
