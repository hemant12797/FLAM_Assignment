import cv2
import numpy as np
import matplotlib.pyplot as plt

def draw_shadow_direction_arrow(image_path, output_path="shadow_direction.png"):
    # Load image and convert to grayscale
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape

    # Enhance contrast (optional)
    gray = cv2.equalizeHist(gray)

    # Threshold to isolate shadows (dark regions)
    _, shadow_mask = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY_INV)

    # Edge detection
    edges = cv2.Canny(shadow_mask, 50, 150)

    # Detect lines (possible shadows)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=80, minLineLength=60, maxLineGap=10)

    angles = []
    directions = []

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            dx, dy = x2 - x1, y1 - y2
            angle = np.arctan2(dx, dy)
            angles.append(angle)
            directions.append((dx, dy))

        # Average direction
        avg_dx = int(np.mean([d[0] for d in directions]))
        avg_dy = int(np.mean([d[1] for d in directions]))

        # Normalize direction vector
        norm = np.sqrt(avg_dx**2 + avg_dy**2)
        if norm == 0:
            avg_dx, avg_dy = 50, 50  # default fallback
        else:
            avg_dx = int(150 * (avg_dx / norm))
            avg_dy = int(150 * (avg_dy / norm))

        # Arrow start and end points
        start = (w // 2, h // 2)
        end = (start[0] + avg_dx, start[1] + avg_dy)

        # Draw the arrow on the image
        cv2.arrowedLine(img, start, end, (0, 255, 255), 5, tipLength=0.2)
        print(f"Arrow drawn from {start} to {end}")
    else:
        print("No shadows detected.")
        return

    # Save and show output
    cv2.imwrite(output_path, img)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title("Estimated Shadow Direction")
    plt.axis("off")
    plt.show()

# Run on your target image
draw_shadow_direction_arrow("target.png")
