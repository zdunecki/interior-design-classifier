from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tensorflow.keras.preprocessing.image import ImageDataGenerator

import argparse
import os

import model


def train_and_evaluate(args):
    train_dir = args.train_dir
    validation_dir = args.validation_dir
    image_height = args.image_height
    image_width = args.image_width
    batch_size = args.batch_size
    epochs = args.num_epochs

    total_train = 0
    total_val = 0

    for train_folder in os.listdir(train_dir):
        total_train = total_train + len(os.listdir(os.path.join(train_dir, train_folder)))

    for val_folder in os.listdir(validation_dir):
        total_val = total_val + len(os.listdir(os.path.join(train_dir, val_folder)))

    output_dense = len(os.listdir(train_dir))

    keras_model = model.create_keras_model((image_height, image_width), output_dense)

    train_image_generator = ImageDataGenerator(rescale=1. / 255)
    validation_image_generator = ImageDataGenerator(rescale=1. / 255)

    train_data_gen = train_image_generator.flow_from_directory(
        batch_size=batch_size,
        directory=train_dir,
        shuffle=True,
        target_size=(image_height, image_width),
        # class_mode=None
        # class_mode='binary'
    )

    val_data_gen = validation_image_generator.flow_from_directory(
        batch_size=batch_size,
        directory=validation_dir,
        target_size=(image_height, image_width),
        # class_mode=None
        # class_mode='binary'
    )

    # Train model
    keras_model.fit_generator(
        train_data_gen,
        steps_per_epoch=total_train // batch_size,
        epochs=epochs,
        validation_data=val_data_gen,
        validation_steps=total_val // batch_size
    )

    model_json = keras_model.to_json()

    with open(args.model_output, "w") as json_file:
        json_file.write(model_json)

    keras_model.save_weights(args.weights_output)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--image-width',
        type=int,
        default=int(os.environ.get("IMAGE_WIDTH", 0)),
        help='image width')
    parser.add_argument(
        '--image-height',
        type=int,
        default=int(os.environ.get("IMAGE_HEIGHT", 0)),
        help='image height')
    parser.add_argument(
        '--train-dir',
        type=str,
        default="./data/train",
        help='local training dir')
    parser.add_argument(
        '--validation-dir',
        type=str,
        default="./data/validation",
        help='local validation dir')
    parser.add_argument(
        '--num-epochs',
        type=int,
        default=int(os.environ.get("NUM_EPOCHS", 15)),
        help='number of times to go through the data, default=15')
    parser.add_argument(
        '--batch-size',
        default=int(os.environ.get("BATCH_SIZE", 128)),
        type=int,
        help='number of records to read during each training step, default=128')
    parser.add_argument(
        '--model-output',
        default=os.environ.get("MODEL_OUTPUT", ""),
        type=str,
        help='model output file')
    parser.add_argument(
        '--weights-output',
        default=os.environ.get("WEIGHTS_OUTPUT", ""),
        type=str,
        help='weights output file')
    parser.add_argument(
        '--learning-rate',
        default=.01,
        type=float,
        help='learning rate for gradient descent, default=.01')
    parser.add_argument(
        '--verbosity',
        choices=['DEBUG', 'ERROR', 'FATAL', 'INFO', 'WARN'],
        default='INFO')
    args, _ = parser.parse_known_args()
    return args


if __name__ == '__main__':
    args = get_args()
    train_and_evaluate(args)
