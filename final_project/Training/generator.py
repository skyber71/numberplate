import numpy as np
import tensorflow as tf
import cv2
import os
from tensorflow.keras.utils import Sequence

class DataGenerator(Sequence):
    def __init__(self, image_dir, label_dir, batch_size=32, image_size=(224, 224), n_classes=1):
        self.image_dir = image_dir
        self.label_dir = label_dir
        self.batch_size = batch_size
        self.image_size = image_size
        self.n_classes = n_classes
        self.image_paths = os.listdir(image_dir)
        self.indexes = np.arange(len(self.image_paths))
        self.on_epoch_end()

    def __len__(self):
        return int(np.floor(len(self.image_paths) / self.batch_size))

    def __getitem__(self, index):
        batch_indexes = self.indexes[index * self.batch_size:(index + 1) * self.batch_size]
        image_paths_batch = [self.image_paths[k] for k in batch_indexes]
        return self.__data_generation(image_paths_batch)

    def on_epoch_end(self):
        np.random.shuffle(self.indexes)

    def __data_generation(self, image_paths_batch):
        images = np.empty((self.batch_size, *self.image_size, 3))
        labels = np.empty((self.batch_size, self.n_classes + 4))

        for i, image_path in enumerate(image_paths_batch):
            image = cv2.imread(os.path.join(self.image_dir, image_path))
            image = cv2.resize(image, self.image_size)
            images[i,] = image / 255.0

            label_path = os.path.join(self.label_dir, image_path.replace('.jpg', '.txt'))
            with open(label_path) as f:
                label = f.readline().strip().split()
                labels[i, 0] = int(label[0])
                labels[i, 1:] = [float(x) for x in label[1:]]

        return images, labels
