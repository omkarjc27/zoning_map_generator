from data import load_csvs,load_img
import tensorflow as tf
from tensorflow import keras
import pandas as pd
import matplotlib.pyplot as plt

# Import Data

train_ds,test_ds,val_ds=load_csvs()

train_ds['Filename']=train_ds['Filename'].apply(lambda x:"train/"+x)
val_ds['Filename']=val_ds['Filename'].apply(lambda x:"validation/"+x)
ds = pd.concat([train_ds,val_ds]).sample(frac=1).reset_index(drop=True)

test_ds['Filename']=test_ds['Filename'].apply(lambda x:"test/"+x)

# Load images to tf.dataset

dataset = tf.data.Dataset.from_tensor_slices((ds.Filename.values,ds.Label.values))

AUTOTUNE = tf.data.AUTOTUNE
train_ds = dataset.take(int(0.8*len(ds)))
val_ds = dataset.take(int(0.2*len(ds)))

train = train_ds.map(load_img,num_parallel_calls=AUTOTUNE).batch(32).prefetch(buffer_size=AUTOTUNE)
val   = val_ds.map(load_img,num_parallel_calls=AUTOTUNE).batch(32).prefetch(buffer_size=AUTOTUNE)

# Define Model

base_model = keras.applications.VGG16(weights="imagenet",include_top=False)
avg = keras.layers.GlobalAveragePooling2D()(base_model.output)
output = keras.layers.Dense(classes, activation="softmax")(avg)
model = keras.Model(inputs=base_model.input, outputs=output)

for layer in base_model.layers:
    layer.trainable = False

# Train Model

model.compile(loss="sparse_categorical_crossentropy",optimizer="adam",metrics=["accuracy"])
history = model.fit(train_ds, epochs=3, validation_data=val_ds,verbose=1)

# Plotting Metrics

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']
epochs_range = range(len(history.history['val_loss']))
plt.figure(figsize=(8, 8))

plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')

plt.show()


# Testing

test_x = tf.data.Dataset.from_tensor_slices((test_ds.Filename.values,test_ds.Label.values))
test_x = test_x.map(load_img).batch(32)

score = model.evaluate(test_x, verbose = 0) 

print('Test loss:', score[0]) 
print('Test accuracy:', score[1])

# Save model for later use

model.save("land_classifier.h5")