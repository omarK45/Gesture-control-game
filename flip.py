import os
import cv2

# Paths
input_folder = "/Users/maryamhabeb/Desktop/H"  # Replace with the path to your input folder
output_folder = "/Users/maryamhabeb/Desktop/flipped"  # Replace with the path to your output folder

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Flip direction: 0 for vertical, 1 for horizontal, -1 for both
flip_code = 1  # Change to your desired flip direction

# Loop through each file in the input folder
for filename in os.listdir(input_folder):
    # Construct full file path
    input_path = os.path.join(input_folder, filename)
    
    # Check if the file is an image
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff')):
        # Read the image
        image = cv2.imread(input_path)
        
        # Check if the image was read successfully
        if image is None:
            print(f"Skipping {filename}: Unable to read file.")
            continue
        
        # Flip the image
        flipped_image = cv2.flip(image, flip_code)
        
        # Construct output file path
        output_path = os.path.join(output_folder, filename)
        
        # Save the flipped image
        cv2.imwrite(output_path, flipped_image)
        print(f"Processed and saved: {filename}")
    else:
        print(f"Skipping {filename}: Not an image file.")

print("Processing complete!")
