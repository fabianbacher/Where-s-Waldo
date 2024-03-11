import streamlit as st
from PIL import Image
import requests
from io import BytesIO

# Set the API endpoint URL
# API_ENDPOINT = "https://wheres-waldo.streamlit.app/"
API_ENDPOINT = "http://localhost:8000/detect_waldo"

# Set up the title and intro of the app on the main page
st.title('Find Waldo with AI!')
st.write("Welcome to the AI-powered Waldo finder. Upload your image and let the AI do the searching.")

# Enhance the sidebar with additional options
with st.sidebar:
    st.write("## App Navigation")
    page = st.radio("Go to", ["Home", "How it works", "Try it out", "About"])

# Displaying different content based on navigation choice
if page == "Home":
    st.header("Home")
    st.write("This is your starting point. Use the navigation in the sidebar to learn more or to start using the app.")

    # Waldo image URL
    waldo_image_url = "https://raw.githubusercontent.com/fabianbacher/wheres-waldo/main/images/Waldo%20Selfie.jpg"

    # Download the image from the web
    response = requests.get(waldo_image_url)
    waldo_image = Image.open(BytesIO(response.content))

    # Display the Waldo image on the home page
    st.image(waldo_image, caption='Waldo is Here!', use_column_width=True)

elif page == "How it works":
    st.header("How it Works")
    st.write("""
        This app uses advanced deep learning algorithms to identify and locate Waldo in any image.
        Simply upload your image, and the AI will highlight Waldo for you.
    """)

    # The correct raw GitHub URL to the CNN model image
    cnn_model_image_url = "https://raw.githubusercontent.com/fabianbacher/wheres-waldo/main/models/CNN%20Model.png"

    # Download the image from the web
    response = requests.get(cnn_model_image_url)
    cnn_model_image = Image.open(BytesIO(response.content))

    # Display the CNN model image on the 'How it works' page, fitting the size of the blue box placeholder
    st.image(cnn_model_image, use_column_width=True)

elif page == "Try it out":
    st.header("Try It Out")
    uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        with st.spinner('Finding Waldo...'):
            # Read the image with PIL
            image = Image.open(uploaded_image)
            st.image(image, caption="Uploaded Image", use_column_width=True)

            # Send the image to the API
            files = {"file": uploaded_image.getvalue()}
            response = requests.post(API_ENDPOINT, files=files)

            if response.status_code == 200:
                data = response.json()
                message = data["message"]
                st.write(message)

                if "output_image" in data:
                    output_image_path = data["output_image"]

                    # Read the output image
                    with open(output_image_path, "rb") as f:
                        image_bytes = f.read()

                    # Display the output image
                    st.image(image_bytes, caption="Image with Waldo detected", use_column_width=True)

                    # Allow users to download the result image
                    st.download_button('Download Result', data=BytesIO(image_bytes), file_name='waldo_found.png')

            else:
                st.error(f"Error: {response.status_code}")

elif page == "About":
    st.header("About")
    st.write("""
    Developed with meticulous dedication by Team Waldo at Le Wagon Amsterdam, this app is the collective brainchild of Fabian Bacher, Albert Paul, Victor van Leeuwen, and Megan Ho.
    It embodies a cutting-edge fusion of deep learning and machine learning technologies, harnessing the advanced functionalities of TensorFlow's Keras coupled with the analytical prowess of Convolutional Neural Networks (CNN).
    Together, they form the dynamic core that drives this app's powerful image recognition models.
    """)

    # Raw GitHub URL to the team's image
    team_image_url = "https://raw.githubusercontent.com/fabianbacher/wheres-waldo/main/images/Team%20Waldo.JPG"

    # Download the image from the web
    response = requests.get(team_image_url)
    team_image = Image.open(BytesIO(response.content))

    # Display the team image, using the full width of the column
    st.image(team_image, caption='Team Waldo', use_column_width=True)
