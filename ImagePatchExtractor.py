import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import argparse

# Function to extract and save patches
def extract_patches(image_path, num_patches, patch_size, output_name, output_dir):
    # Load the image
    img = Image.open(image_path)
    fig, ax = plt.subplots()
    ax.imshow(img)

    # Make figure full screen
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()

    # Store clicks
    clicks = []

    # Rectangle to show patch area
    rect = plt.Rectangle((0,0), patch_size, patch_size, linewidth=1, edgecolor='r', facecolor='none')
    ax.add_patch(rect)
    rect.set_visible(False)

    # Function to handle click events
    def onclick(event):
        if event.xdata is not None and event.ydata is not None:
            # Append click position, adjusting for patch size
            clicks.append((int(event.ydata), int(event.xdata)))
            if len(clicks) == num_patches:
                plt.close()

    # Function to handle motion events
    def onmove(event):
        if event.xdata is not None and event.ydata is not None:
            x, y = event.xdata - patch_size / 2, event.ydata - patch_size / 2
            rect.set_xy((x, y))
            rect.set_visible(True)
            fig.canvas.draw_idle()

    # Connect the events to the handlers
    fig.canvas.mpl_connect('button_press_event', onclick)
    fig.canvas.mpl_connect('motion_notify_event', onmove)

    # Display the image and wait for clicks
    plt.show()

    # After collecting clicks, extract and save patches
    for i, (y, x) in enumerate(clicks):
        left = x - patch_size // 2
        upper = y - patch_size // 2
        right = left + patch_size
        lower = upper + patch_size

        # Extract patch
        patch = img.crop((left, upper, right, lower))

        # Save patch
        patch_filename = f"{output_dir}/{output_name}_{patch_size}x{patch_size}_{i+1}.jpg"
        patch.save(patch_filename)
        print(f"Patch saved: {patch_filename}")

if __name__ == "__main__":
    # Initialize parser
    parser = argparse.ArgumentParser(description='Extract image patches by clicking.')
    
    # Adding arguments
    parser.add_argument('-i', '--image_path', type=str, required=True, help='Path to the original image')
    parser.add_argument('-n', '--num_patches', type=int, required=True, help='Number of patches to be collected')
    parser.add_argument('-s', '--patch_size', type=int, required=True, help='Size of each patch (e.g., 8 for 8x8)')
    parser.add_argument('-o', '--output_name', type=str, required=True, help='Base name for output files')
    parser.add_argument('-d', '--output_dir', type=str, required=True, help='Directory to save image patches')
    
    # Parse arguments
    args = parser.parse_args()

    # Extract and save patches
    extract_patches(args.image_path, args.num_patches, args.patch_size, args.output_name, args.output_dir)

