import tensorflow as tf
from tensorflow import keras 
import pandas as pd
import urllib.request
import itertools
import os
import numpy as np
import shutil

model = tf.keras.models.load_model('../input/land-scene-classifier/land_classifier.h5')
filenames = ["".join(p) for p in itertools.product(['0','1','2','3'], repeat=5)]

# Download Images
shutil.rmtree("./images",ignore_errors=True)
os.makedirs('./images')
for i in range(len(filenames)):
    quadkey = filenames[i]
    if i%100==0:print(quadkey) 
    urllib.request.urlretrieve("http://ecn.t0.tiles.virtualearth.net/tiles/a02301023020111{}.jpeg?g=10583".format(quadkey), "./images/02301023020111{}.jpeg".format(quadkey))
print("Done.")

# Create Dataset
eval_ds = tf.data.Dataset.from_tensor_slices((df.path.values))
eval_ds = eval_ds.map(load_test_img).batch(32)

# Make Predictions
prediction = model.predict(eval_ds)
print(prediction)

# Classes with max probability 
ans = []
for i in range(len(prediction)):
    ans.append(np.argmax(prediction[i]))

# Create CSV with all answers 
df = pd.DataFrame({'path': filenames,'value':ans,})
df.head()
df.to_csv('map_data.csv')