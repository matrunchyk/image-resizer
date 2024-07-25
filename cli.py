import os
from PIL import Image

def process_images(source_folder, output_folder):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through all files in the source folder
    for filename in os.listdir(source_folder):
        file_path = os.path.join(source_folder, filename)
        if os.path.isfile(file_path):
            # Open an image file
            with Image.open(file_path) as img:
                # Get the size of the image
                img_width, img_height = img.size

                # Define the size of the new canvas
                canvas_width, canvas_height = 1035, 1440

                # Calculate the scaling factor to fit the image inside the canvas
                scale_factor = min((canvas_width - 130) / img_width, (canvas_height - 130) / img_height)
                new_width = int(img_width * scale_factor)
                new_height = int(img_height * scale_factor)

                # Resize the image with the calculated scale factor
                img_resized = img.resize((new_width, new_height), Image.LANCZOS)

                # Create a new image with white background
                new_image = Image.new('RGB', (canvas_width, canvas_height), (255, 255, 255))

                # Calculate position to paste the resized image on the new canvas
                paste_x = (canvas_width - new_width) // 2
                paste_y = (canvas_height - new_height) // 2

                # Paste the resized image onto the new canvas
                new_image.paste(img_resized, (paste_x, paste_y))

                # Save the new image
                new_image.save(os.path.join(output_folder, filename))

if __name__ == "__main__":
    # Get the current directory of the script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Define source and output folders relative to the current directory
    source_folder = os.path.join(current_dir, 'source')
    output_folder = os.path.join(current_dir, 'output')

    # Process the images
    process_images(source_folder, output_folder)

