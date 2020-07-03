import torchvision
import numpy as np
import cv2

class model():

    def __init__(self):
        self.model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)
        self.model.eval()
        self.classes = [
                'background', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
                'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'street sign',
                'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse',
                'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'hat', 'backpack',
                'umbrella', 'shoe', 'eye glasses', 'handbag', 'tie', 'suitcase', 'frisbee',
                'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove',
                'skateboard', 'surfboard', 'tennis racket', 'bottle', 'plate', 'wine glass',
                'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich',
                'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair',
                'couch', 'potted plant', 'bed', 'mirror', 'dining table', 'window', 'desk',
                'toilet', 'door', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
                'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'blender', 'book',
                'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush', 'hair brush']

    def get_predict(self, image_pil, img_cv):
        image_tensor = torchvision.transforms.functional.to_tensor(image_pil)
        output = self.model([image_tensor])
        out_img = self.__create_img_from_out(img_cv, output, self.classes)
        return out_img


    def __create_img_from_out(self, img, output, classes):
        # random color for each class
        colors = np.random.uniform(0, 255, size=(len(classes), 3))

        # iterate over the network output for all boxes
        for mask, box, box_class, score in zip(output[0]['masks'].detach().numpy(),
                                               output[0]['boxes'].detach().numpy(),
                                               output[0]['labels'].detach().numpy(),
                                               output[0]['scores'].detach().numpy()):

            # filter the boxes by score
            if score > 0.5:
                # transform bounding box format
                box = [(box[0], box[1]), (box[2], box[3])]

                # overlay the segmentation mask on the image with random color
                # img[(mask > 0.5).squeeze(), :] = np.random.uniform(0, 255, size=3)

                # draw the bounding box
                cv2.rectangle(img=img,
                              pt1=box[0],
                              pt2=box[1],
                              color=(255, 255, 255),
                              thickness=2)

                # extract class name
                class_name = classes[box_class]
                # select class color
                color = colors[box_class]
                # display the box class label
                cv2.putText(img=img,
                            text=class_name,
                            org=box[0],
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=1,
                            color=color,
                            thickness=2)
        return img