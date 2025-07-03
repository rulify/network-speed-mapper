import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import numpy as np
import csv

# Load your network data (format: name, up_speed, down_speed)
def load_network_data(csv_file):
    data = []
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) == 3:
                name, up, down = row
                try:
                    data.append((name.strip(), float(up), float(down)))
                except ValueError:
                    print(f"Skipping invalid row: {row}")
    return data

# Normalize for colour mapping
def normalize(values):
    arr = np.array(values)
    return (arr - arr.min()) / (arr.max() - arr.min() + 1e-5)

# Let user click points to assign to each data row
def get_coords_for_points(image_path, points):
    coords = []

    def onclick(event):
        nonlocal index
        if index < len(points):
            # Convert click back to original image size
            x_real = int(event.x / scale)
            y_real = int(event.y / scale)
            coords.append((points[index][0], x_real, y_real))
            print(f"Marked '{points[index][0]}' at ({x_real}, {y_real})")
            index += 1
            if index == len(points):
                root.destroy()
            else:
                label.config(text=f"Click on map for: {points[index][0]}")

    # Load original image
    img = Image.open(image_path)
    orig_width, orig_height = img.size

    # Resize for display (fit within 1000×800 for example)
    max_display_width = 1000
    max_display_height = 800

    scale = min(1, min(max_display_width / orig_width, max_display_height / orig_height))
    new_width = int(orig_width * scale)
    new_height = int(orig_height * scale)
    display_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # GUI
    root = tk.Tk()
    root.title("Click locations for network points")
    tk_img = ImageTk.PhotoImage(display_img)
    canvas = tk.Canvas(root, width=new_width, height=new_height)
    canvas.pack()
    canvas.create_image(0, 0, anchor=tk.NW, image=tk_img)

    index = 0
    label = tk.Label(root, text=f"Click on map for: {points[index][0]}")
    label.pack()
    canvas.bind("<Button-1>", onclick)
    root.mainloop()

    return coords, img  # Return full-res image


# Visualise on map using matplotlib
def plot_network_map(image, coords, up_speeds, down_speeds, output_file):
    fig, ax = plt.subplots()
    ax.imshow(image)

    norm_down = normalize(down_speeds)
    cmap = plt.cm.get_cmap("RdYlGn")  # red = slow, green = fast

    for i, (name, x, y) in enumerate(coords):
        colour = cmap(norm_down[i])
        circle = plt.Circle((x, y), radius=100, color=colour, alpha=0.6)
        ax.add_patch(circle)
        ax.text(x, y, name, fontsize=7, ha='center', va='center', color='black', weight='bold')

    ax.axis('off')
    plt.savefig(output_file, bbox_inches='tight', dpi=300)
    plt.show()

# Main logic
def main():
    print("Select your CSV data file...")
    csv_path = filedialog.askopenfilename(
        title="Select CSV file",
        filetypes=[("CSV Files", "*.csv")]
    )
    if not csv_path:
        print("No CSV selected")
        return

    data = load_network_data(csv_path)
    print(f"Loaded {len(data)} points from CSV")
    if len(data) == 0:
        print("No valid data in CSV. Exiting.")
        return

    print("Select your site map image...")
    img_path = filedialog.askopenfilename(
        title="Select Site Map",
        filetypes=[
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg"),
            ("JPEG files", "*.jpeg"),
            ("All Image files", "*.png *.jpg *.jpeg")
        ]
    )
    if not img_path:
        print("No image selected")
        return

    coords, img = get_coords_for_points(img_path, data)
    print(f"Got {len(coords)} coords")

    if len(coords) != len(data):
        print("Coords and data mismatch!")
        return

    names, up_speeds, down_speeds = zip(*data)
    plot_network_map(img, coords, up_speeds, down_speeds, "network_map_output.png")

if __name__ == "__main__":
    main()
