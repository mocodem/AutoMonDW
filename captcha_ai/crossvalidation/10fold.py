import os
from random import shuffle
import shutil
import yaml
from ultralytics import YOLO


# YOLO Custom Method
# gather all data and split into 10 folds
num_folds = 10

def gather():
    # Gather image and label file paths for test, train, and valid datasets
    _, _, test_img_files = next(os.walk("/Users/mo/Desktop/MSc thesis/ai/data/test/images"))
    _, _, test_label_files = next(os.walk("/Users/mo/Desktop/MSc thesis/ai/data/test/labels"))
    _, _, train_img_files = next(os.walk("/Users/mo/Desktop/MSc thesis/ai/data/train/images"))
    _, _, train_label_files = next(os.walk("/Users/mo/Desktop/MSc thesis/ai/data/train/labels"))
    _, _, valid_img_files = next(os.walk("/Users/mo/Desktop/MSc thesis/ai/data/valid/images"))
    _, _, valid_label_files = next(os.walk("/Users/mo/Desktop/MSc thesis/ai/data/valid/labels"))

    # Create file paths for image and label files
    test_img_files = ["/Users/mo/Desktop/MSc thesis/ai/data/test/images/" + file_name for file_name in test_img_files]
    test_label_files = ["/Users/mo/Desktop/MSc thesis/ai/data/test/labels/" + file_name for file_name in test_label_files]
    train_img_files = ["/Users/mo/Desktop/MSc thesis/ai/data/train/images/" + file_name for file_name in train_img_files]
    train_label_files = ["/Users/mo/Desktop/MSc thesis/ai/data/train/labels/" + file_name for file_name in train_label_files]
    valid_img_files = ["/Users/mo/Desktop/MSc thesis/ai/data/valid/images/" + file_name for file_name in valid_img_files]
    valid_label_files = ["/Users/mo/Desktop/MSc thesis/ai/data/valid/labels/" + file_name for file_name in valid_label_files]

    # print(len(test_img_files) == len(test_label_files))
    # print(len(train_img_files) == len(train_label_files))
    # print(len(valid_img_files) == len(valid_label_files))

    # Verify that the number of image files matches the number of label files
    all_img = test_img_files + train_img_files + valid_img_files
    all_label = test_label_files + train_label_files + valid_label_files
    all_img.sort()
    all_label.sort()
    print("collected all images and labels:", len(all_img)==len(all_label)) # 12043

    # Create indexes for data folding
    index = list(range(0, len(all_img)))
    shuffle(index)
    k, m = divmod(len(index), num_folds)
    index_folds = list((index[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(num_folds)))
    print("created indexes of",len(index_folds),"folds")
    input("sure to proceed moving all files? ")

    # Move images and labels into fold directories
    for fold in range(num_folds):
        print("moving images and labels into fold:",fold)
        img_dir = f'/Users/mo/Desktop/MSc thesis/ai/crossvalidation/data/fold_{fold}/images/'
        label_dir = f'/Users/mo/Desktop/MSc thesis/ai/crossvalidation/data/fold_{fold}/labels/'
        os.makedirs(img_dir, exist_ok=True)
        os.makedirs(label_dir, exist_ok=True)
        for i_index in index_folds[fold]:
            shutil.copyfile(all_img[i_index], img_dir+all_img[i_index].split("/")[-1])
            shutil.copyfile(all_label[i_index], label_dir+all_label[i_index].split("/")[-1])
    print("created 10 directories for each fold with all data")

def create_yaml():
    # Generate a YAML file for each fold
    for fold in range(num_folds):
        all_folds = [f"/Users/mo/Desktop/MSc thesis/ai/crossvalidation/data/fold_{fold2}/images/" if fold2 != fold else None for fold2 in range(10)]
        all_folds.remove(None)
        data_yaml = dict(
            train=all_folds,
            val=f'/Users/mo/Desktop/MSc thesis/ai/crossvalidation/data/fold_{fold}/images/',
            nc=4,
            names=['0', '1', '2', 'c']
        )
        with open(f'/Users/mo/Desktop/MSc thesis/ai/crossvalidation/data/data_fold_{fold}.yaml', 'w') as outfile:
            yaml.dump(data_yaml, outfile, default_flow_style=True)

def create_yaml_colab():
    """
    # connect drive folder
    from google.colab import drive
    drive.mount('/content/drive')
    # file path: drive/MyDrive/Endgame/data/
    # import yolo
    !pip install ultralytics==8.0.20
    from IPython import display
    display.clear_output()
    import ultralytics
    ultralytics.checks()
    from ultralytics import YOLO
    model = YOLO('yolov8n.pt')
    num_folds = 10
    for i in range(num_folds):
        print("------------- iteration:",i,"-------------")
        model.train(data=f"/content/drive/MyDrive/Endgame/data/data_fold_{i}.yaml", epochs=1)
        print("------------- done:",i,"-------------")
    """
    for fold in range(num_folds):
        all_folds = [f"/home/moses/Desktop/ai/data/fold_{fold2}/images/" if fold2 != fold else None for fold2 in range(10)]
        all_folds.remove(None)
        data_yaml = dict(
            train=all_folds,
            val=f'/home/moses/Desktop/ai/data/fold_{fold}/images/',
            nc=4,
            names=['0', '1', '2', 'c']
        )
        with open(f'/Users/mo/Desktop/MSc thesis/ai/crossvalidation/thinkpad/data_fold_{fold}.yaml', 'w') as outfile:
            yaml.dump(data_yaml, outfile, default_flow_style=True)

def train_model():
    model = YOLO('yolov8n.pt')
    for i in range(num_folds):
        print("------------- iteration:",i,"-------------")
        model.train(data=f'/Users/mo/Desktop/MSc thesis/ai/crossvalidation/data/data_fold_{i}.yaml', epochs=1)
        print("------------- done:",i,"-------------")
