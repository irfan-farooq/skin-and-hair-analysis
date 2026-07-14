import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import MobileNetV3Small
import numpy as np
import matplotlib.pyplot as plt
import os


IMG_SIZE    = 224    
BATCH_SIZE  = 16    
EPOCHS_HEAD = 15     # phase 1: train only your head
EPOCHS_FINE = 25     # phase 2: fine-tune last layers
DATA_DIR    = "data/"
MODEL_PATH  = "models/hair_mobilenetv3.keras"
CLASSES     = ["straight", "textured"]

datagen = keras.preprocessing.image.ImageDataGenerator(
    rescale=1./255,          
    rotation_range=30,        
    horizontal_flip=True,    
    brightness_range=[0.8, 1.2], 
    zoom_range=0.1,         
    validation_split=0.2     
)

train_data = datagen.flow_from_directory(
    DATA_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="categorical", 
    subset="training",
    classes=CLASSES,
    shuffle=True
)

val_data = datagen.flow_from_directory(
    DATA_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="validation",
    classes=CLASSES,
    shuffle=False               
)

print(f"Train samples: {train_data.samples}")
print(f"Val samples:   {val_data.samples}")
print(f"Classes: {train_data.class_indices}")

# Load MobileNetV3 WITHOUT its top classifier
base_model = MobileNetV3Small(
    input_shape=(IMG_SIZE, IMG_SIZE, 3),
    include_top=False,      # remove Google's 1000-class head
    weights="imagenet"      # keep all pretrained weights
)

# FREEZE base 
base_model.trainable = False


inputs  = keras.Input(shape=(IMG_SIZE, IMG_SIZE, 3))
x       = base_model(inputs, training=False)


x       = layers.GlobalAveragePooling2D()(x)


x       = layers.Dropout(0.3)(x)


x       = layers.Dense(128, activation="relu")(x)
x       = layers.Dropout(0.2)(x)


outputs = layers.Dense(2, activation="softmax")(x)

model = keras.Model(inputs, outputs)
model.summary()  




model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=5e-4),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)


callbacks = [
   
    keras.callbacks.EarlyStopping(
        monitor="val_accuracy",
        patience=6,
        restore_best_weights=True 
    ),
  
    keras.callbacks.ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.5,       
        patience=2,
        min_lr=1e-7
    )
]

print("── Phase 1: Training head ──")


history1 = model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS_HEAD,
    callbacks=callbacks,
    
)


print("── Phase 2: Fine-tuning ──")

# Unfreeze base model
base_model.trainable = True

# Re-freeze EXCEPT last 20 layers
for layer in base_model.layers[:-20]:
    layer.trainable = False

# Recompile 
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=1e-5),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

history2 = model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS_FINE,
    callbacks=callbacks,
    
)


os.makedirs("models", exist_ok=True)
model.save("models/hair_mobilenetv3.keras")
print(f"Model saved → {MODEL_PATH}")



def plot_history(h1, h2):
  
    acc = h1.history["accuracy"] + h2.history["accuracy"]
    val_acc = h1.history["val_accuracy"] + h2.history["val_accuracy"]
    loss = h1.history["loss"] + h2.history["loss"]
    val_loss = h1.history["val_loss"] + h2.history["val_loss"]

    epochs = range(1, len(acc) + 1)

    plt.figure(figsize=(12, 4))

    plt.subplot(1, 2, 1)
    plt.plot(epochs, acc, label="Train accuracy")
    plt.plot(epochs, val_acc, label="Val accuracy")
    plt.title("Accuracy over epochs")
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(epochs, loss, label="Train loss")
    plt.plot(epochs, val_loss, label="Val loss")
    plt.title("Loss over epochs")
    plt.legend()

    plt.tight_layout()
    plt.savefig("training_curves.png")
    plt.show()

plot_history(history1, history2)


from sklearn.metrics import confusion_matrix, classification_report
import numpy as np

# Get predictions on validation set
val_data.reset()
y_pred = model.predict(val_data)
y_pred_classes = np.argmax(y_pred, axis=1)
y_true = val_data.classes

print(classification_report(y_true, y_pred_classes,
      target_names=CLASSES))

cm = confusion_matrix(y_true, y_pred_classes)
print("Confusion matrix:")
print(cm)