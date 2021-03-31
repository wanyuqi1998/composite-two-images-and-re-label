from PIL import Image
import random
import os




def compute(a0, b0, c0, d0, old_bound, new_pos, new_bound):
    a = (float(a0) * old_bound[0] + new_pos[0]) / new_bound[0]
    b = (float(b0) * old_bound[1] + new_pos[1]) / new_bound[1]
    c = (float(c0) * old_bound[0] + new_pos[0]) / new_bound[0]
    d = (float(d0) * old_bound[1] + new_pos[1]) / new_bound[1]
    str_out = str(a) + " " + str(b) + " " + str(c) + " " + str(d)
    return str_out


def composite(img1, img2):
    # img1 is object, img2 is background

    newImage = []
    for item in img1.getdata():
        if item[:3] == (255, 255, 255):
            newImage.append((255, 255, 255, 0))
        else:
            newImage.append(item)

    img1.putdata(newImage)

    sizeW, sizeH = img1.size

    lim_w = img2.size[0]
    lim_h = img2.size[1]

    # ratio
    toCheckW = lim_w / sizeW
    toCheckH = lim_h / sizeH
    if toCheckW >= 5 or sizeH >= 5:
        if toCheckH <= 20 or toCheckW <= 20:
            img1 = img1.resize((int(img1.size[0] / 5), int(img1.size[1] / 5)))
            sizeW, sizeH = img1.size

    else:
        print("background is too small in comparison with foreground")

    # new position
    x = random.randint(0, lim_w - sizeW)
    y = random.randint(0, lim_h - sizeH)

    img2.paste(img1, (x, y), img1)

    bbox_x1, bbox_y1 = x, y  # upper left
    bbox_x2, bbox_y2 = x + sizeW, y + sizeH  # bottom right

    new_pos = bbox_x1,bbox_y1,bbox_x2,bbox_y2

    return img2, new_pos


folder_b = 'img'
folder_f = 'animals/images/trainAnimals'
backgrounds = os.listdir(folder_b)
objs = os.listdir(folder_f)

folder_f_l = 'animals/labels/trainAnimals'
# labels = os.listdir(folder_f_l)

for index in range(len(backgrounds)):
    src = folder_b + '/' + backgrounds[index]
    background = Image.open(src).convert("RGBA")
    mask = folder_f + '/' + objs[index]
    foreground = Image.open(mask).convert("RGBA")

    im_n = objs[index][:-4]
    if "." in im_n:
        target = im_n+"txt"

    else:
        target = im_n+".txt"
    try: label = open(folder_f_l + '/' + target, 'r').readline().split()
    except: continue

    print(index)

    old_label = label[1:]


    output_img, pos = composite(foreground, background)

    if len(old_label) < 4: continue
    else:
        new_label = compute(old_label[0],old_label[1],old_label[2],old_label[3], foreground.size, pos, background.size)

    img_save = "composite/img/"+objs[index]

    output_img = output_img.convert('RGB')
    output_img.save(img_save)

    new_label_p = "composite/label/"+target
    new_label_f = open(new_label_p,"w")

    new_label_f.write(str(label[0])+" "+new_label)