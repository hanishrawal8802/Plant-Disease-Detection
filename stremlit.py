import streamlit as st
from PIL import Image
import numpy as np
import tensorflow as tf 
import tensorflow.keras as keras
import matplotlib.pyplot as plt
import tensorflow_hub as hub

hide_streamlit_style = """
            
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            
            """
st.markdown(hide_streamlit_style, unsafe_allow_html = True)

st.title('Potato Leaf Disease Prediction')
def main() :
    file_uploaded = st.file_uploader('Choose an image...', type = 'jpg')
    if file_uploaded is not None :
        image = Image.open(file_uploaded)
        st.write("Uploaded Image.")
        figure = plt.figure()
        plt.imshow(image)
        plt.axis('off')
        st.pyplot(figure)
        result, confidence = predict_class(image)
        st.write('Prediction : {}'.format(result))
        st.write('Confidence : {}%'.format(confidence))
def predict_class(image) :
    with st.spinner('Loading Model...'):
        classifier_model = keras.models.load_model(r'potato.h5', compile = False)

    shape = ((256,256,3))
    model = keras.Sequential([hub.KerasLayer(classifier_model, input_shape = shape)])   
    test_image = image.resize((256, 256))
    test_image = keras.preprocessing.image.img_to_array(test_image)
    test_image /= 255.0
    test_image = np.expand_dims(test_image, axis = 0)
    class_name = ['Potato__Early_blight', 'Potato__Late_blight', 'Potato__healthy']

    prediction = model.predict(test_image)
    confidence = round(100 * (np.max(prediction[0])), 2)
    final_pred = class_name[np.argmax(prediction)]
    return final_pred, confidence
footer = """
a:link , a:visited{
    color: blue;
    background-color: transparent;
    text-decoration: None;
}

a:hover,  a:active {
    color: grey;
    background-color: transparent;
    text-decoration: None;
}
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: transparent;
    color: black;
    text-align: center;
}
</style>
<div class="footer">
<p align="center"> <a href="https://www.linkedin.com/in/hanish-raval-a55125218//">Developed by hanish rawal</a></p>
</div>
        """

st.markdown(footer, unsafe_allow_html = True)

if __name__ == '__main__' :
    main()