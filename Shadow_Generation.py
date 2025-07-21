from PIL import Image, ImageOps, ImageFilter
import numpy as np

# === Load the object image (with transparent background ideally) ===
image_path = "person_no_bg.png"  # Replace with your image path
person = Image.open(image_path).convert("RGBA")

# === Create a solid black silhouette from the person ===
shadow = person.copy()
shadow = ImageOps.grayscale(shadow)         # Convert to grayscale
shadow = ImageOps.colorize(shadow, black="#101010", white="black")  # All black
shadow.putalpha(person.split()[-1])         # Keep original alpha

# === Stretch shadow horizontally to the right ===
width, height = shadow.size
stretch_ratio = 1.0  # Equal to height
new_width = int(height * stretch_ratio)
shadow_stretched = shadow.resize((new_width, height))

# === Skew shadow to simulate ground contact ===
# Move top of shadow to same vertical level as the object’s base
shadow_skew = shadow_stretched.transform(
    (width, height),
    Image.AFFINE,
    (0.8, 0.3, 1,      # Horizontal stretch
     0, 1, 0),     # Vertical no skew
    resample=Image.BICUBIC
)

# === Blur the shadow for realism ===
shadow_blurred = shadow_skew.filter(ImageFilter.GaussianBlur(5))

# === Create canvas and paste both shadow and object ===
offset_x = int(width * 0.3)  # Adjust this to control closeness
canvas = Image.new("RGBA", (width + new_width, height), (0, 0, 0, 0))
canvas.paste(shadow_blurred, (offset_x, 0), shadow_blurred)
canvas.paste(person, (0, 0), person)


# === Show or Save ===
canvas.show()
canvas.save("shadow.png")
