import joblib
import os

# Assuming the model is saved in the root directory of the project
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'pretrained_model.pkl')

def load_model():
    model = joblib.load(MODEL_PATH)
    return model
