from PIL import Image

# Open an image
img = Image.open('D:\Documents\code\python\yolo\datasets\defect\images\\train\\1.jpg')

# Get image size
width, height = img.size
print(f"Image size: {width} x {height}")
