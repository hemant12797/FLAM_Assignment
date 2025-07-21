from PIL import Image, ImageDraw, ImageFilter
import numpy as np
from rembg import remove

def remove_background(input_path, output_path):
    with open(input_path, 'rb') as i:
        input_image = i.read()
    output_image = remove(input_image)
    with open(output_path, 'wb') as o:
        o.write(output_image)

def blend_with_shadow(person_path, background_path, output_path,
                      position=(400, 400), size=(250, 400), light_dir=(1, -1)):
    person = Image.open(person_path).convert("RGBA").resize(size)
    background = Image.open(background_path).convert("RGBA")

    shadow = person.copy().convert("RGBA")
    shadow_np = np.array(shadow)
    shadow_np[..., :3] = 0
    shadow_np[..., 3] = shadow_np[..., 3] * 0.5
    shadow = Image.fromarray(shadow_np).filter(ImageFilter.GaussianBlur(radius=8))

    offset = (position[0] + int(light_dir[0]*50), position[1] + int(light_dir[1]*50))
    background.paste(shadow, offset, shadow)
    background.paste(person, position, person)

    draw = ImageDraw.Draw(background)
        # Draw light direction arrow from top-right corner
    bg_width, _ = background.size
    

    background.save(output_path)

# Run the pipeline
remove_background("source.png", "person_no_bg.png")
blend_with_shadow("person_no_bg.png", "target.png", "final_output.png")
