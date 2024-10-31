


from PIL import Image, ImageDraw, ImageFont

def adjust_annex5_geo (filename, output_file, HEIGHT = 5.31, WIDTH= 8.122, POINT="T241_g"):
    adjust_img (filename, output_file, HEIGHT, WIDTH, GEO=True, POINT=POINT)

def adjust_annex5_panoramic (filename, output_file, HEIGHT = 5.31, WIDTH  = 7.45) :
    adjust_img (filename, output_file, HEIGHT, WIDTH )

def adjust_annex5_detail (filename, output_file, HEIGHT=3.5, WIDTH=4.05) :
    adjust_img (filename, output_file, HEIGHT , WIDTH)

def zoom_img (image, factor):

    width, height = image.size
    
    # Calculate crop box for center zoom
    crop_width = int(width / factor)
    crop_height = int(height / factor)
    left = (width - crop_width) // 2
    top = (height - crop_height) // 2
    right = left + crop_width
    bottom = top + crop_height
    
    # Crop and resize back to original size
    cropped_image = image.crop((left, top, right, bottom))
    return cropped_image



def create_annotation () :
    
    font_size = 12
    font_path = "/usr/share/fonts/truetype/lato/Lato-Medium.ttf"
    # Choose a font and font size
    try:
        font = ImageFont.truetype(font_path, font_size)  # Adjust font size as needed
    except IOError:
        font = ImageFont.load_default()
        
        
    for i in range(1,1000):
        box_width, box_height = 45, 20
        image = Image.new("RGB", (box_width, box_height), "white")
        draw = ImageDraw.Draw(image)
        
        text = f"T-{i}"
        text_height = font_size
        text_width = draw.textlength(text, font=font)
        border_thickness = 1
        draw.rectangle(
            [(0, 0), (box_width - 1, box_height - 1)],  # Coordinates of the rectangle
            outline="black",
            width=border_thickness
        )
        
        text_x = (box_width - text_width) // 2
        text_y = (box_height - text_height) // 2
        
        draw.text((text_x, text_y + 1), text, fill="black", font=font)
        
        image.save(f"annotation/T{i}_g.png")


def adjust_img (filename, output_file, HEIGHT , WIDTH, GEO=False, POINT = "T242_g"):
    
    # TARGET PARAMETERS
    W_RATIO  = WIDTH / HEIGHT
    H_RATIO = HEIGHT / WIDTH
    
    img = Image.open(filename)
 
    dpi = 300 * 0.32
    
    cm_to_px = lambda cm: int((cm * dpi) / 2.54)
 
    img_w_ratio = img.width  / img.height
    img_h_ratio = img.height / img.width 
    
    W_DIFF = W_RATIO - img_w_ratio
    H_DIFF = H_RATIO - img_h_ratio

    TOP = 0
    RIGHT = 0
    BOTTOM = 0
    LEFT = 0
 
    if W_DIFF < 0:
        DELTA  =  - W_DIFF * img.height * 0.5
        LEFT   = DELTA
        RIGHT  = img.width - DELTA
        TOP    = 0
        BOTTOM = img.height
        cropped_img = img.crop((LEFT, TOP, RIGHT, BOTTOM))
        resized_img = cropped_img.resize((cm_to_px(WIDTH), cm_to_px(HEIGHT)))
    
 
    if H_DIFF < 0:
        DELTA = - H_DIFF * img.width * 0.5
        LEFT = 0
        RIGHT = img.width
        TOP = DELTA
        BOTTOM = img.height - DELTA
        cropped_img = img.crop((LEFT, TOP, RIGHT, BOTTOM))
        resized_img = cropped_img.resize((cm_to_px(WIDTH),cm_to_px(HEIGHT)))
   
    
    if GEO:
        
        overlay = Image.open("annotation/NORTH.png")
        annot   = Image.open(f"annotation/{POINT}.png")
        annot_x =  resized_img.width - annot.width - 3
        annot_y =  resized_img.height - annot.height - 3
        
        x_offset = resized_img.width - overlay.width - 4
        y_offset = 4
        
        position = (x_offset,y_offset)
        resized_img.paste(overlay, position, mask=overlay)
        resized_img.paste(annot, (annot_x, annot_y))
        draw = ImageDraw.Draw(resized_img)
        draw.rectangle(
            [(0, 0), (resized_img.width-1, resized_img.height-1)],  # Coordinates of the rectangle
            outline="black",
            width=1
        )
        resized_img.save(output_file, format="JPEG",quality=95)
        
        return
    
    draw = ImageDraw.Draw(resized_img)
    draw.rectangle(
            [(0, 0), (resized_img.width-1, resized_img.height-1)],  # Coordinates of the rectangle
            outline="black",
            width=1
        )
    resized_img.save(output_file, format="JPEG",quality=95)
    


if __name__ == "__main__":
    print("imgConverter")
    create_annotation()


