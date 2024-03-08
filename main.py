from fastapi import FastAPI, File, UploadFile
import uvicorn
from PIL import Image
import numpy as np
import tensorflow as tf

# Import your existing functions
from find_waldo import load_image_into_numpy_array, draw_box

app = FastAPI()

# Load the TensorFlow model
model_path = './frozen_inference_graph.pb'
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.compat.v1.GraphDef()
    with open(model_path, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

@app.post("/detect_waldo")
async def detect_waldo(file: UploadFile = File(...)):
    # Read the image data
    image = Image.open(file.file)
    image_np = load_image_into_numpy_array(image)

    # Run the TensorFlow model
    with detection_graph.as_default():
        with tf.compat.v1.Session(graph=detection_graph) as sess:
            # Get the tensors
            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
            boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
            scores = detection_graph.get_tensor_by_name('detection_scores:0')
            classes = detection_graph.get_tensor_by_name('detection_classes:0')
            num_detections = detection_graph.get_tensor_by_name('num_detections:0')

            # Actual detection
            (boxes, scores, classes, num_detections) = sess.run(
                [boxes, scores, classes, num_detections],
                feed_dict={image_tensor: np.expand_dims(image_np, axis=0)}
            )

            # Check if Waldo was found
            if scores[0][0] < 0.1:
                return {"message": "Waldo not found :("}

            # Draw the bounding box
            fig, ax = draw_box(boxes[0][0], image_np)
            ax.imshow(image_np)

            # Save the image with the bounding box
            output_path = "output.png"
            fig.savefig(output_path)

            return {"message": "Waldo found", "output_image": output_path}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
