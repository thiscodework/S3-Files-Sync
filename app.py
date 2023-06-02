import streamlit as st
import boto3
import io
from PIL import Image, ImageEnhance  # Add the ImageEnhance import

# Set up AWS S3
s3 = boto3.client(
    's3',
    aws_access_key_id='AKIAQTY4EPQRLPPZXTNJ',
    aws_secret_access_key='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'
)
bucket_name = 's3-files-sync'

def main():
    st.title("S3 Image Upload and Edit")
    
    # Image upload
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)

        # Image editing options
        st.subheader("Image Editing")
        brightness = st.slider("Brightness", -100, 100, 0, 10)
        contrast = st.slider("Contrast", -100, 100, 0, 10)
        saturation = st.slider("Saturation", -100, 100, 0, 10)

        edited_image = edit_image(image, brightness, contrast, saturation)
        st.image(edited_image, caption='Edited Image', use_column_width=True)

        # Upload the edited image to S3
        if st.button("Save"):
            save_image_to_s3(edited_image, 'edited_image.jpg')
            st.success("Image saved successfully!")

def edit_image(image, brightness, contrast, saturation):
    # Add your image editing code here
    # Example: Applying brightness, contrast, and saturation adjustments using PIL
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(brightness / 10.0)

    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(contrast / 10.0)

    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(saturation / 10.0)

    return image

def save_image_to_s3(image, filename):
    # Convert image to RGB mode
    image = image.convert('RGB')

    # Create a byte stream for the edited image
    edited_image_stream = io.BytesIO()
    image.save(edited_image_stream, format='JPEG')
    edited_image_stream.seek(0)

    # Upload the image to S3
    s3.upload_fileobj(edited_image_stream, bucket_name, filename)

if __name__ == '__main__':
    main()