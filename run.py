from PIL import Image, ImageDraw, ImageFont
import sys
import os

CELL_W, CELL_H = 400, 600
composenum = int(0)

def load_image(path, idx):
    try:
        im = Image.open(path).convert("RGBA")
    except:
        im = Image.new("RGBA", (CELL_W, CELL_H), (0, 0, 0, 255))
    return im.resize((CELL_W, CELL_H), Image.LANCZOS)

def compose(indices, folder, groups):
    global composenum
    if groups == 4:
        cols, rows = 4, 1
    else:
        cols, rows = 3, 2

    layout = []
    for r in range(rows):
        for c in range(cols):
            layout.append((c, r))

    out = Image.new("RGBA", (CELL_W*cols, CELL_H*rows), (255,255,255,255))

    for i, idx in enumerate(indices):
        if i >= groups: break
        path = os.path.join(folder, f"{idx}.png")
        im = load_image(path, idx)
        x, y = layout[i]
        out.paste(im, (x*CELL_W, y*CELL_H))

    if folder == 'art':
        filename = f"art.png"
        out.convert("RGB").save(filename)
        print(f"已輸出:{filename}")
    else:
        composenum = composenum  + 1
        filename = f"compose{composenum}.png"
        out.convert("RGB").save(filename)
        print(f"已輸出:{filename}")
        Image.open(f"{filename}")

def parse_input(s, groups):
    parts = s.split()
    nums = [p for p in parts if not p.startswith("-")]
    flags = [p for p in parts if p.startswith("-")]
    
    if len(nums) != groups:
        print(f"plz enter {groups} number!")
        return None, None

    try:
        nums = [int(n) for n in nums]
    except:
        print("invalid input!")
        return None, None

    if not all(1 <= n <= 89 for n in nums):
        print("invalid input!")
        return None, None

    folder = "imagine"
    if "-a" in flags:
        folder = "art"

    return nums, folder

if __name__ == "__main__":
    groups = 0
    while groups != 4 and groups !=6 :
        groups = int(input("How many groups:").strip())
        if (groups != 4 and groups !=6):
            print("invalid groups number!")
    while True:
        s = input("Enter card number:").strip()
        if len(s) == 0:
            continue
        if s == "exit":
            break
        nums, folder = parse_input(s, groups)

        if nums is None:
            continue  

        compose(nums, folder, groups)