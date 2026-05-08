import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
import os

# ---------------------------------------------------
# DATASET PATH
# ---------------------------------------------------

dataset_path = "app/image_model/road_surface_dataset"

# ---------------------------------------------------
# IMAGE SETTINGS
# ---------------------------------------------------

IMG_SIZE = (224, 224)
BATCH_SIZE = 32

# ---------------------------------------------------
# IMAGE GENERATOR
# ---------------------------------------------------

datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2,
    rotation_range=10,
    zoom_range=0.1,
    horizontal_flip=True
)

train_data = datagen.flow_from_directory(
    dataset_path,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training'
)

val_data = datagen.flow_from_directory(
    dataset_path,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation'
)

# ---------------------------------------------------
# MODEL
# ---------------------------------------------------

base_model = tf.keras.applications.MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights='imagenet'
)

base_model.trainable = False

model = models.Sequential([
    base_model,

    layers.GlobalAveragePooling2D(),

    layers.Dense(128, activation='relu'),

    layers.Dropout(0.3),

    layers.Dense(
        train_data.num_classes,
        activation='softmax'
    )
])

# ---------------------------------------------------
# COMPILE
# ---------------------------------------------------

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# ---------------------------------------------------
# TRAIN
# ---------------------------------------------------

history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=5
)

# ---------------------------------------------------
# SAVE MODEL
# ---------------------------------------------------

model.save("app/image_model/road_image_classifier.h5")

print("\nImage classification model saved successfully!")

# ---------------------------------------------------
# ACCURACY GRAPH
# ---------------------------------------------------

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])

plt.title("Training Accuracy")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")

plt.legend(['Train', 'Validation'])

plt.savefig("results/image_model_accuracy.png")

print("Accuracy graph saved!")