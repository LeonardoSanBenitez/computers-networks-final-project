# Math manipulation
import numpy as np
import pandas as pd
import math

# Vizualization
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib import pyplot # for rcnn compatibility

# Image processing
import cv2
from io import BytesIO


# deep learning
from mrcnn.config import Config
from mrcnn.model import MaskRCNN
from keras.preprocessing.image import img_to_array
from mrcnn.visualize import random_colors, apply_mask, find_contours, patches, Polygon  # Export workarround


# define the custom configuration in  (the other variables have good default values)
class config(Config):
  NAME = "barnInstanceSegmentation"
  GPU_COUNT = 1
  IMAGES_PER_GPU = 1
  NUM_CLASSES = 1 + 80
  DETECTION_MIN_CONFIDENCE = 0.4
  DETECTION_NMS_THRESHOLD = 0.1
  DETECTION_MAX_INSTANCES = 150
  #I think that the input size can be modified

class InstanceSegmentation:
  def __init__(self, weight_path, img_height=256, img_width=256):
    self.class_names = ['BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane',
                        'bus', 'train', 'truck', 'boat', 'traffic light',
                        'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird',
                        'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear',
                        'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie',
                        'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
                        'kite', 'baseball bat', 'baseball glove', 'skateboard',
                        'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
                        'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
                        'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
                        'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed',
                        'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote',
                        'keyboard', 'cell phone', 'microwave', 'oven', 'toaster',
                        'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
                        'teddy bear', 'hair drier', 'toothbrush']

    self.rcnn = MaskRCNN(mode='inference', model_dir='./predictive_models/rcnn', config=config()) # define the model
    self.rcnn.keras_model._make_predict_function()
    self.rcnn.load_weights(weight_path, by_name=True) # load coco model weights

  def _display_instances(self, image, boxes, masks, class_ids, class_names,
                        scores=None, title="",
                        figsize=(16, 16), ax=None,
                        show_mask=True, show_bbox=True,
                        colors=None, captions=None, verbose=True, save_img=False, image_path=""):
    """
    boxes: [num_instance, (y1, x1, y2, x2, class_id)] in image coordinates.
    masks: [height, width, num_instances]
    class_ids: [num_instances]
    class_names: list of class names of the dataset
    scores: (optional) confidence scores for each box
    title: (optional) Figure title
    show_mask, show_bbox: To show masks and bounding boxes or not
    figsize: (optional) the size of the image
    colors: (optional) An array or colors to use with each object
    captions: (optional) A list of strings to use as captions for each object
    """
    # Number of instances
    N = boxes.shape[0]
    if not N:
        print("\n*** No instances to display *** \n")
    else:
        assert boxes.shape[0] == masks.shape[-1] == class_ids.shape[0]

    _, ax = plt.subplots(1, figsize=figsize)

    # Generate random colors
    colors = colors or random_colors(N)

    # Show area outside image boundaries.
    height, width = image.shape[:2]
    ax.set_ylim(height + 10, -10)
    ax.set_xlim(-10, width + 10)
    ax.axis('off')
    ax.set_title(title)

    masked_image = image.astype(np.uint32).copy()
    for i in range(N):
      color = colors[i]

      # Bounding box
      if not np.any(boxes[i]):
        # Skip this instance. Has no bbox. Likely lost in image cropping.
        continue
      y1, x1, y2, x2 = boxes[i]
      if show_bbox:
        p = patches.Rectangle((x1, y1), x2 - x1, y2 - y1, linewidth=2,
                            alpha=0.7, linestyle="dashed",
                            edgecolor=color, facecolor='none')
        ax.add_patch(p)

      # Label
      if not captions:
        class_id = class_ids[i]
        score = scores[i] if scores is not None else None
        label = class_names[class_id]
        caption = "{} {:.3f}".format(label, score) if score else label
      else:
        caption = captions[i]
      ax.text(x1, y1 + 8, caption,
              color='w', size=11, backgroundcolor="none")

      # Mask
      mask = masks[:, :, i]
      if show_mask:
        masked_image = apply_mask(masked_image, mask, color)

      # Mask Polygon
      # Pad to ensure proper polygons for masks that touch image edges.
      padded_mask = np.zeros(
          (mask.shape[0] + 2, mask.shape[1] + 2), dtype=np.uint8)
      padded_mask[1:-1, 1:-1] = mask
      contours = find_contours(padded_mask, 0.5)
      for verts in contours:
        # Subtract the padding and flip (y, x) to (x, y)
        verts = np.fliplr(verts) - 1
        p = Polygon(verts, facecolor="none", edgecolor=color)
        ax.add_patch(p)
    ax.imshow(masked_image.astype(np.uint8))
    if save_img:
      plt.savefig(image_path,bbox_inches='tight', pad_inches=-0.5,orientation= 'landscape')
    if verbose:
      plt.show()
    #   return ax
    buff = BytesIO()
    plt.savefig(buff, format="png", bbox_inches='tight', pad_inches=-0.1, orientation= 'landscape')
    buff.seek(0)
    return buff

  def _preProcessFrame(self, frame):
    #frame = cv2.flip(frame, 0)
    #brightness = 20
    #contrast = -20
    #frame = np.int16(frame) * (contrast/127+1) - contrast + brightness
    #frame = np.clip(frame, 0, 255)
    frame = np.uint8(frame)
    return frame

  def predict (self, raw_image=None, verbose=0):
    if raw_image==None:
        raw_image = plt.imread('static/img/last_image.jpg')
    raw_image = self._preProcessFrame(raw_image)

    if verbose: plt.imshow(raw_image)
        
    img = img_to_array (raw_image)
    if verbose: print('Shape on input: ', img.shape)
    results = self.rcnn.detect([img], verbose=verbose)
    
    img = self._display_instances(img, 
                        results[0]['rois'], 
                        results[0]['masks'], 
                        results[0]['class_ids'],
                        self.class_names, 
                        results[0]['scores'],
                        title='Frame instance segmentation',
                        verbose=verbose,
                        save_img=True,
                        image_path='static/img/last_image_segmented.jpg')
    return img