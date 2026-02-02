from datasets import load_dataset
import os

ds = load_dataset("reach-vb/pokemon-blip-captions", split="train", streaming=True)

image_dir = "data/images"
caption_dir = "data/captions"
os.makedirs(image_dir, exist_ok=True)
os.makedirs(caption_dir, exist_ok=True)

print("Starting streaming extraction...")

# 2. Iterate just like before
for i, row in enumerate(ds):
    img = row["image"]
    caption = row["text"]

    if img.mode != "RGB":
        img = img.convert("RGB")
    
    img.save(os.path.join(image_dir, f"{i}.jpg"), "JPEG")

    with open(os.path.join(caption_dir, f"{i}.txt"), "w", encoding="utf-8") as f:
        f.write(caption)

    if i % 50 == 0:
        print(f"Processed {i} images...")

print("Done!")