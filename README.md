# Image Prep Tool

Image Prep Tool is a Python application designed to simplify the process of preparing images for LoRA and fine-tune training. It provides a user-friendly interface for various image processing tasks.

## Features

- **Duplicate Finding**: Automatically detect and remove duplicate images, with user verification.
- **Image Resizing**: Resize images to specific dimensions while maintaining aspect ratio if desired.
- **Caption Writing**: Easily write and save captions for your dataset images.
- **Caption Templates**: Use mustache templates for captions and quickly fill in templated areas.
- **Watermark and Text Removal**: Remove watermarks or text from images using inpainting.

## Requirements

- Python 3.x
- PyQt5
- Pillow
- NumPy
- OpenCV
- ImageHash

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/image-prep-tool.git
   cd image-prep-tool
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the main script to start the application:

```
python main.py
```

The application window will open with two main tabs:

1. **Duplicate Finder**: Find and manage duplicate images in a selected directory.
2. **Image Viewer**: View, edit, and process individual images.

### Duplicate Finder

1. Click "Select Directory" to choose the folder containing your images.
2. Click "Start Duplicate Search" to begin the process.
3. Review the results and delete unwanted duplicates.

### Image Viewer

1. Click "Select Directory" to choose the folder containing your images.
2. Use the navigation buttons to browse through images.
3. Resize images, add captions, or remove watermarks as needed.
4. Save your changes or delete unwanted images.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.