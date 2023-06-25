import os

# _, _, images = next(os.walk("/Users/mo/Desktop/MSc thesis/ai/second/manipulated/images/"))
# _, _, labels = next(os.walk("/Users/mo/Desktop/MSc thesis/ai/second/manipulated/labels/"))
# images = sorted(images)
# labels = sorted(labels)

# This file is used to move all files to set up 

_, _, files = next(os.walk("/Users/mo/Desktop/MSc thesis/ai/data/valid/"))

print("starting to move files")
for i in range(len(files)):
    print(i,"/", len(files))
    if files[i][-4:] == ".png":
        os.rename(f"/Users/mo/Desktop/MSc thesis/ai/data/valid/{files[i]}",
                  f"/Users/mo/Desktop/MSc thesis/ai/data/valid/images/{files[i]}")
    elif files[i][-4:] == ".txt":
        os.rename(f"/Users/mo/Desktop/MSc thesis/ai/data/valid/{files[i]}",
                  f"/Users/mo/Desktop/MSc thesis/ai/data/valid/labels/{files[i]}")

    """
    if i < 1125:
        os.rename(f"/Users/mo/Desktop/MSc thesis/ai/second/manipulated/images/{images[i]}",
                  f"/Users/mo/Desktop/MSc thesis/ai/data/test/{images[i]}")
        os.rename(f"/Users/mo/Desktop/MSc thesis/ai/second/manipulated/labels/{labels[i]}",
                  f"/Users/mo/Desktop/MSc thesis/ai/data/test/{labels[i]}")
    elif i < 2250:
        os.rename(f"/Users/mo/Desktop/MSc thesis/ai/second/manipulated/images/{images[i]}",
                  f"/Users/mo/Desktop/MSc thesis/ai/data/valid/{images[i]}")
        os.rename(f"/Users/mo/Desktop/MSc thesis/ai/second/manipulated/labels/{labels[i]}",
                  f"/Users/mo/Desktop/MSc thesis/ai/data/valid/{labels[i]}")
    else:
        os.rename(f"/Users/mo/Desktop/MSc thesis/ai/second/manipulated/images/{images[i]}",
                  f"/Users/mo/Desktop/MSc thesis/ai/data/train/{images[i]}")
        os.rename(f"/Users/mo/Desktop/MSc thesis/ai/second/manipulated/labels/{labels[i]}",
                  f"/Users/mo/Desktop/MSc thesis/ai/data/train/{labels[i]}")
    """
print("done")
