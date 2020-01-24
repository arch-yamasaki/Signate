#%%
import os, sys, json, glob
from PIL import Image, ImageDraw, ImageFont


# %%
from glob import glob

colors = {
            "red": (255,0,0), "green": (0,255,0), "blue": (0,0,255),
            "yellow": (255,255,0), "purple": (255,0,255), "black": (0,0,0),
            "white": (255,255,255)
        }
category_color_dict = {
    1: colors["black"], 2: colors["blue"], 3: colors["red"],
    4: colors["blue"], 5: colors["red"], 6: colors["yellow"],
    7: colors["purple"],   8: colors["green"], 9: colors["black"]}


FONT = ImageFont.truetype("mincho.ttf", 40)


#%%
def write_category_box(img, box, category_id):
    draw = ImageDraw.Draw(img)
    draw.rectangle(box, outline=category_color_dict[category_id])

def write_japanese(img, text, pos):
    draw = ImageDraw.Draw(img)
    draw.text(pos, text, fill=(0, 0, 0), font=FONT)

def write_rectangle_from_json(annos_path, image_path, output_path, kind="train"):
    basename = os.path.basename(annos_path)
    basename = basename.split(".")[0]
    img = Image.open(image_path)
    
    with open(annos_path) as f:
        annos_dict = json.load(f)

    attributes_dict = annos_dict["attributes"]
    book_type = attributes_dict["年代"] if "年代" in attributes_dict else "年代不明"
    year = attributes_dict["出版年"] if "出版年" in attributes_dict else "出版年不明"
    write_japanese(img, year, (50, 50))
    write_japanese(img, book_type, (350, 50))

    obj_infos = annos_dict["labels"]
    for obj_info in obj_infos:
        bbox_dict = obj_info["box2d"] # box2d_dict = {'x1': 1219, 'x2': 1241, 'y1': 284, 'y2': 1046}
        bbox = list(bbox_dict.values())
        category_id = int(obj_info["category"][:1])
        write_category_box(img, bbox, category_id)
    img.save(output_path, quality=90)

def get_dataset_dicts(dataset_dir, kind="train", limit_num=99999):
    images_dir = os.path.join(dataset_dir, f"{kind}_images")
    annos_dir = os.path.join(dataset_dir, f"{kind}_annotations")
    output_dir = os.path.join(dataset_dir, f"{kind}_rect_images")
    os.makedirs(output_dir, exist_ok=True)

    annos_paths = glob(annos_dir + "/*")
    for idx, annos_path in enumerate(annos_paths):
        basename = os.path.basename(annos_path)
        basename = basename.split(".")[0]
        image_path = os.path.join(images_dir, f"{basename}.jpg")
        output_path = os.path.join(output_dir, f"{basename}.jpg")
        write_rectangle_from_json(annos_path, image_path, output_path)

#%%
get_dataset_dicts("dataset")

# %%
