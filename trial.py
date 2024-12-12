import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# Unsplash API key
UNSPLASH_API_KEY = 'UsP5NZq0aLWj9SPXZWSB4kWPGUbQ7P9U5VvVlsrNz_Y'

# Function to fetch image from Unsplash API
def fetch_unsplash_image(query):
    url = f"https://api.unsplash.com/photos/random?query={query}&client_id={UNSPLASH_API_KEY}&count=1"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data:
            image_url = data[0]['urls']['regular']
            return image_url
    return None

# Function to download image and save as PNG
def download_image_as_png(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        return img_byte_arr
    return None

# Streamlit UI setup
st.title("Image")
st.write("Enter a description below to fetch an image")

# Textbox for user input
user_input = st.text_input("Enter a search term:", "")

if user_input:
    st.write(f"Searching for images related to '{user_input}'...")
    
    # Fetch image from Unsplash
    image_url = fetch_unsplash_image(user_input)
    
    if image_url:
        st.image(image_url, caption=f"Image for '{user_input}'", use_column_width=True)
        
        # Create a download button for the image as PNG
        img_byte_arr = download_image_as_png(image_url)
        if img_byte_arr:
            st.download_button(
                label="Download as PNG",
                data=img_byte_arr,
                file_name="unsplash_image.png",
                mime="image/png"
            )
        else:
            st.write("Failed to download image.")
    else:
        st.write("No image found. Try a different search term.")

# Run the app using: streamlit run app.py
