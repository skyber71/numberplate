import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Input

def create_model(input_shape=(224, 224, 3), n_classes=1):
    inputs = Input(shape=input_shape)

    x = Conv2D(32, (3, 3), activation='relu')(inputs)
    x = MaxPooling2D((2, 2))(x)

    x = Conv2D(64, (3, 3), activation='relu')(x)
    x = MaxPooling2D((2, 2))(x)

    x = Conv2D(128, (3, 3), activation='relu')(x)
    x = MaxPooling2D((2, 2))(x)

    x = Flatten()(x)
    x = Dense(128, activation='relu')(x)

    class_output = Dense(n_classes, activation='sigmoid', name='class_output')(x)
    bbox_output = Dense(4, name='bbox_output')(x)

    model = Model(inputs=inputs, outputs=[class_output, bbox_output])
    return model

model = create_model()
model.compile(optimizer='adam', 
              loss={'class_output': 'binary_crossentropy', 'bbox_output': 'mse'}, 
              metrics={'class_output': 'accuracy', 'bbox_output': 'mse'})
