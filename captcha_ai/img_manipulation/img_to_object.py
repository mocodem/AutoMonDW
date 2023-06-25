import os
import uuid

from PIL import Image, ImageDraw
import random
import pybboxes as pbx

# Define the dictionary for object types and their corresponding folders
obj_dict = {
    1: {'folder': "images"},
    2: {'folder': "background"},
}

def yolocrop():
    # Perform YOLO cropping on images based on YOLO bounding box annotations
    _, _, files = next(os.walk("/Users/mo/Desktop/MSc thesis/ai/second/images"))
    for file in files:
        name = file[:-4]
        img = Image.open(f"/Users/mo/Desktop/MSc thesis/ai/second/images/{name}.png")
        f = open(f"/Users/mo/Desktop/MSc thesis/ai/second/labels/{name}.txt", "r")
        labels = f.read().split(" ")[1:]
        labels = [float(i) for i in labels]
        yolo_bbox1 = (labels[0], labels[1], labels[2], labels[3])
        W, H = img.size
        bbox = pbx.convert_bbox(yolo_bbox1, from_type="yolo", to_type="voc", image_size=(W, H))
        img2 = img.crop(bbox)
        img2.save(f"/Users/mo/Desktop/MSc thesis/ai/second/reduced/{name}_reduced.png")

def load(obj_dict, PATH_MAIN: str = ""):
    # Load images from folders specified in the object dictionary
    for k, _ in obj_dict.items():
        folder_name = obj_dict[k]['folder']
        files_imgs = sorted(os.listdir(os.path.join(PATH_MAIN, folder_name)))
        files_imgs = [os.path.join(PATH_MAIN, folder_name, f) for f in files_imgs]
        obj_dict[k]['images'] = files_imgs
    print("The first five files from the sorted list of battery images:", obj_dict[1]['images'][:5])
    return obj_dict

def generate():
    # Generate manipulated images by pasting reduced images onto random backgrounds
    _, _, reduced_images = next(os.walk("/Users/mo/Desktop/MSc thesis/ai/second/reduced"))
    _, _, backgrounds = next(os.walk("/Users/mo/Desktop/MSc thesis/ai/captcha_manipulation/background"))
    for idx, img_name in enumerate(reduced_images):
        c_type = None
        if "text" in img_name:
            c_type = 0
        elif "number" in img_name:
            c_type = 1
        elif "image" in img_name:
            c_type = 2
        print(f"{idx}/{len(reduced_images)}")
        img = Image.open("/Users/mo/Desktop/MSc thesis/ai/second/reduced/"+img_name)
        x, y = img.size
        for background_name in backgrounds:
            try:
                background = Image.open("/Users/mo/Desktop/MSc thesis/ai/captcha_manipulation/background/"+background_name)
                b_x, b_y = background.size
                if b_x-x < 1 or b_y-y < 1:
                    continue
                x2 = random.randint(0, b_x-x)
                y2 = random.randint(0, b_y-y)
                background.paste(img, (x2, y2))
                bbox = (x2, y2, x2+x, y2+y)
                name = str(uuid.uuid4())
                print(f"{img_name} with {background_name} -> {name}")
                background.save("/Users/mo/Desktop/MSc thesis/ai/second/manipulated/images/" + name + ".png")
                with open(f"/Users/mo/Desktop/MSc thesis/ai/second/manipulated/labels/{name}.txt", "w") as f:
                    f.write(f'{c_type} {str(pbx.convert_bbox(bbox, from_type="voc", to_type="yolo", image_size=(b_x, b_y))).replace(",", "").replace("(", "").replace(")","")}')
            except:
                pass

generate()
