import streamlit as st
import boto3
import io
from PIL import Image, ImageEnhance  # Add the ImageEnhance import

# Set up AWS S3
s3 = boto3.client(
    's3',
    aws_access_key_id = 'AKIAQTY4EPQRLPPZXTNJ',
    aws_secret_access_key = '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',
    config = boto3.session.Config(signature_version='s3v4'),
    region_name='ap-south-1'
)
bucket_name = 's3-files-sync'

def main():
    st.title("S3 Image Upload and Edit")
    page = st.sidebar.selectbox("Select a page", ["Upload", "View"])
    
    if page == "Upload":
        upload_page()
    elif page == "View":
        view_page()

def upload_page():
    st.header("Upload Images")
    
    # Image upload
    uploaded_files = st.file_uploader("Choose multiple images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            image = Image.open(uploaded_file)
            st.image(image, caption=f"Uploaded Image: {uploaded_file.name}", use_column_width=True)
            st.write("---")

            # Image editing options
            brightness = st.slider(f"Brightness ({uploaded_file.name})", -100, 100, 0)
            contrast = st.slider(f"Contrast ({uploaded_file.name})", -100, 100, 0)
            saturation = st.slider(f"Saturation ({uploaded_file.name})", -100, 100, 0)

            edited_image = edit_image(image, brightness, contrast, saturation)
            st.image(edited_image, caption=f"Edited Image: {uploaded_file.name}", use_column_width=True)

            # Upload the edited image to S3
            if st.button(f"Save ({uploaded_file.name})"):
                save_image_to_s3(edited_image, f"edited_{uploaded_file.name}")
                st.success("Image saved successfully!")

            st.write("---")
def view_page():
    st.header("View Images")
    
    # Fetch images from S3
    image_urls = fetch_images_from_s3()

    if image_urls:
        for image_url in image_urls:
            st.image(image_url, use_column_width=True)

def edit_image(image, brightness, contrast, saturation):
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(1 + brightness / 100.0)

    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1 + contrast / 100.0)

    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(1 + saturation / 100.0)

    return image

def save_image_to_s3(image, filename):
    edited_image_stream = io.BytesIO()
    image.save(edited_image_stream, format='JPEG')
    edited_image_stream.seek(0)

    s3.upload_fileobj(edited_image_stream, bucket_name, filename, ExtraArgs={'ContentType': 'image/jpeg'})

def fetch_images_from_s3():
    response = s3.list_objects_v2(Bucket=bucket_name)
    images = []

    if 'Contents' in response:
        for obj in response['Contents']:
            image_url = s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket_name, 'Key': obj['Key']},
                ExpiresIn=36000  # Set the expiration time as per your requirement
            )
            images.append(image_url)

    return images   

if __name__ == '__main__':
    main()
           