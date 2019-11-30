import tensorflow as tf
import numpy as np
import json
import os

with open('./output/model.json', 'r') as f:
    model_json = json.dumps(json.load(f))

model = tf.keras.models.model_from_json(model_json)
model.load_weights('./output/weights.h5')

# tf.saved_model.save(model, "new_weights.h5")