import tensorflow as tf
import streamlit as st
from tensorflow.keras.losses import MeanSquaredError

@st.cache_resource
def load_model():
    """Loads and caches the deep learning model."""
    custom_objects = {"mse": MeanSquaredError()}
    model_path = "model_deep.h5"  # Ensure this path is correct
    return tf.keras.models.load_model(model_path, custom_objects=custom_objects)

model = load_model()

@st.cache_data
def predict_egt(input_data):
    """
    Predicts EGT Hot Day Margin using the trained deep learning model.

    Parameters:
    input_data (DataFrame): Scaled input data for prediction.

    Returns:
    float: Predicted EGT Hot Day Margin value.
    """
    prediction = model.predict(input_data)
    return prediction


#@st.cache_resource for model loading: Ensures the model is loaded once and reused, improving performance.
#@st.cache_data for prediction: Caches predictions to avoid redundant computations on the same input.