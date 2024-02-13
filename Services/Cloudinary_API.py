import cloudinary
import cloudinary.api
import cloudinary.uploader
from dotenv import load_dotenv
import os

def Upload_Photo_CloudinaryAPI(Path_Photo):
    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET"),
        secure=True,
    )

    result = cloudinary.uploader.upload(
        Path_Photo,
        folder="AgendaPy",
        resource_type="image")
    
    return result["url"]