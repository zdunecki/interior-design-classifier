import tensorflow as tf
import numpy as np
import json
import os

with open('../output/model.json', 'r') as f:
    model_json = json.dumps(json.load(f))

model = tf.keras.models.model_from_json(model_json)
model.load_weights('../output/weights.h5')

training_folder = "../data/test/validation/"
rustic_folder = os.path.join(training_folder, "industrial")

labels = [
    "bohemian",
    "classic",
    "coastal",
    "farm-house",
    "glam",
    "industrial",
    "mid-century-modern",
    "minimal",
    "preppy",
    "rustic",
    "scandinavian",
    "transitional"
]

for file_name in os.listdir(rustic_folder):
    file_path = os.path.join(rustic_folder, file_name)
    img_pred = tf.keras.preprocessing.image.load_img(
        file_path,
        target_size=(150, 150, 3)
    )
    img_pred = tf.keras.preprocessing.image.img_to_array(img_pred)

    img_pred = np.expand_dims(img_pred, axis=0)
    img_pred = img_pred / 255

    result = model.predict(img_pred)
    values = result[0].tolist()

    sorted_match = sorted(
        list(map(lambda args: (args[1], labels[args[0]]), enumerate(values))),
        key=lambda x: x[0],
        reverse=True
    )

    print(
        file_name + ":",
        ", ".join(list(
            map(lambda args: str(args[0] + 1) + ": " + args[1][1], enumerate(sorted_match[0: 3]))
        ))
    )
