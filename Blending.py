from PIL import Image, ImageEnhance, ImageOps, ImageDraw

# Load images
person_img = Image.open("shadow.png").convert("RGBA")
background = Image.open("target.png").convert("RGBA")

# Resize person image
scale_factor = 0.8
new_size = (int(person_img.width * scale_factor), int(person_img.height * scale_factor))
person_img = person_img.resize(new_size, Image.Resampling.LANCZOS)

# Position the person realistically
position = (int(person_img.width * 0.3), int(person_img.height * 0.6))

# Create a shadow
shadow = person_img.copy().convert("L")
shadow = ImageOps.colorize(shadow, black="black", white="black")
shadow = shadow.convert("RGBA")
shadow.putalpha(80)  # Set transparency

# Create transparent shadow layer
shadow_layer = Image.new("RGBA", background.size, (0, 0, 0, 0))
shadow_offset = (position[0] + 80, position[1] - 30)
shadow_layer.paste(shadow, shadow_offset, shadow)

# Composite shadow with background
composite = Image.alpha_composite(background, shadow_layer)

# Paste person on top
composite.paste(person_img, position, person_img)

# Save result
composite.save("final_output.png")
