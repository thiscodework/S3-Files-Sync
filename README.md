# S3 Image Upload and Edit Web App

This web app allows users to upload images to an AWS S3 bucket and perform various editing operations on the uploaded images.

## Prerequisites

Before running the web app, ensure that you have the following:

- Python 3.6 or higher installed on your system.
- AWS account credentials (Access Key ID and Secret Access Key) with sufficient permissions to interact with S3.
- Python packages listed in the `requirements.txt` file. You can install them using the command:
pip install -r requirements.txt

## Instructions

1. Clone the repository or download the source code files.

2. Install the required Python packages mentioned in the `requirements.txt` file. You can use the following command:
3. Open the `app.py` file and replace the placeholder values for `YOUR_ACCESS_KEY`, `YOUR_SECRET_KEY`, and `YOUR_BUCKET_NAME` with your own AWS credentials and S3 bucket details.

4. Run the following command in your terminal to start the web app:
streamlit run app.py

5. The web app will start running locally, and you can access it by opening the provided URL in your web browser.

6. Use the file upload functionality to select and upload multiple images (JPG, JPEG, PNG) to the web app.

7. For each uploaded image, adjust the sliders for brightness, contrast, and saturation to apply desired edits.

8. The edited image will be displayed, and you can save it by clicking the "Save" button. It will be uploaded to the configured S3 bucket with a modified filename.

9. Follow the on-screen instructions and enjoy using the S3 Image Upload and Edit web app!

## License

This project is licensed under the [MIT License](LICENSE).
