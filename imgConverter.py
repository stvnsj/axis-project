


from PIL import Image

def adjust_annex5_geo (filename, output_file, HEIGHT = 5.31, WIDTH= 8.12):
    adjust_img (filename, output_file, HEIGHT, WIDTH )

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


def adjust_img (filename, output_file, HEIGHT , WIDTH):
    
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
 
    if W_DIFF < 0:
        DELTA =  - W_DIFF * img.height * 0.5
        LEFT_MARGIN = DELTA
        RIGHT_MARGIN = img.width - DELTA
        cropped_img = img.crop((LEFT_MARGIN, 0, RIGHT_MARGIN, img.height))
        resized_img = cropped_img.resize((cm_to_px(WIDTH), cm_to_px(HEIGHT)))
        resized_img.save(output_file, format="JPEG",quality=95)
        
        
 
    if H_DIFF < 0:
        DELTA = - H_DIFF * img.width * 0.5
        TOP_MARGIN = DELTA
        BOTTOM_MARGIN = img.height - DELTA
        cropped_img = img.crop((0, TOP_MARGIN, img.width, BOTTOM_MARGIN))
        resized_img = cropped_img.resize((cm_to_px(WIDTH),cm_to_px(HEIGHT)))
        resized_img.save(output_file, format="JPEG",quality=95)


if __name__ == "__main__":
    print("imgConverter")


