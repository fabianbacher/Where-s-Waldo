
import streamlit as st
from PIL import Image
import requests
from io import BytesIO

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
    waldo_image_url = "https://github.com/fabianbacher/wheres-waldo/raw/main/Waldo%20Selfie.jpg"
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

elif page == "Try it out":
    st.header("Try It Out")
    uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        with st.spinner('Finding Waldo...'):
            # Read the image with PIL
            image = Image.open(uploaded_image)
            st.image(image, caption="Uploaded Image", use_column_width=True)

            # Your image processing code
            # Replace with actual processing code

            # Mockup: Replace this with condition checking if Waldo was found
            waldo_found = True  # replace with actual detection result
            if waldo_found:
                # Mockup: Replace with the actual result image after processing
                result_image = image  # replace with actual result image
                result_image_available = True  # replace with actual check

                st.image(result_image, caption="Waldo Found!", use_column_width=True)
                st.success('Done!')

                # Allow users to download the result image
                st.download_button('Download Result', data=BytesIO(result_image.tobytes()), file_name='waldo_found.png')
            else:
                st.error("Waldo could not be found in this image.")

elif page == "About":
    st.header("About")
    st.write("""
        Developed with meticulous dedication by Team Waldo at Le Wagon Amsterdam, this app is the collective brainchild of Fabian Bacher, Albert Paul, Victor van Leeuwen, and Megan Ho.
        It embodies a cutting-edge fusion of deep learning and machine learning technologies, harnessing the advanced functionalities of TensorFlow's Keras coupled with the analytical prowess of Convolutional Neural Networks (CNN).
        Together, they form the dynamic core that drives this app's powerful image recognition models.
    """)
 # Raw GitHub URL to the team's image
    team_image_url = "https://raw.githubusercontent.com/fabianbacher/wheres-waldo/main/Team%20Waldo.JPG"

    # Download the image from the web
    response = requests.get(team_image_url)
    team_image = Image.open(BytesIO(response.content))

    # Display the team image, using the full width of the column
    st.image(team_image, caption='Team Waldo', use_column_width=True)
# Note: Ensure that the logic and variables like `result_image_available` and `result_image` are properly defined in your actual code
