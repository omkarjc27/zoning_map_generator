import tensorflow as tf
from tensorflow import keras
import pandas as pd

def load_csvs():
	location = "/dataset/"	
	return pd.read_csv(location+"train.csv"),pd.read_csv(location+"test.csv"),pd.read_csv(location+"validation.csv")

def load_img(path,valu):
    location="/dataset/"
    img = tf.io.decode_jpeg(tf.io.read_file(location+"images_train_test_val/"+path),channels=3)
    img = tf.cast(img, tf.float32)
    img = tf.image.resize(img, [224,224])
    img = keras.applications.vgg16.preprocess_input(img)
    return img,valu

def load_test_img(path):
    img = tf.io.decode_jpeg(tf.io.read_file(path),channels=3)
    img = tf.cast(img, tf.float32)
    img = tf.image.resize(img, [224,224])
    img = keras.applications.vgg16.preprocess_input(img)
    return img