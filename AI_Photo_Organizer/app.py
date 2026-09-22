from flask import Flask, request, jsonify
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image
import io
import base64

app = Flask(__name__)

# Assuming `train_data` and its `classes` attribute are available from previous cells
# If not, you might need to re-initialize `train_data` or load the classes from a file

# Define the CNN model architecture (must be identical to the one used for training)
class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()

        self.conv = nn.Sequential(
            nn.Conv2d(3, 16, 3),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(16, 32, 3),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )

        # This needs to be correctly initialized with the number of classes
        # For demonstration, I'll use a placeholder. You should ensure train_data.classes is available
        # or load class names from a saved list.
        num_classes = 131 # Replace with actual number of classes or load from train_data.classes
        # The actual number of classes will be determined by `len(train_data.classes)`
        # Let's try to get it from the kernel state if possible, or assume 131 as per previous output.
        # If train_data.classes is not available, you would need to load it.
        
        # Placeholder if train_data.classes is not directly accessible here.
        # In a real deployment, you'd load the classes from a persisted list.
        global train_data # Access the global train_data from the notebook state
        if 'train_data' in globals() and hasattr(train_data, 'classes'):
            num_classes = len(train_data.classes)
            class_names = train_data.classes
        else:
            # Fallback or load from a saved file if train_data is not available
            print("Warning: train_data not found or classes attribute missing. Using hardcoded num_classes=131 and placeholder class_names.")
            num_classes = 131
            class_names = [f'class_{i}' for i in range(num_classes)] # Placeholder


        self.fc = nn.Sequential(
            nn.Linear(32*30*30, 128),
            nn.ReLU(),
            nn.Linear(128, num_classes)
        )

    def forward(self, x):
        x = self.conv(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x

app = Flask(__name__)

# Load the trained model
model = CNN()
model.load_state_dict(torch.load("cnn_model.pth"))
model.eval()

# Image transformations (must be identical to training/evaluation transformations)
transform = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor(),
])

# Get class names (assuming train_data.classes is available in the global scope)
# If not, you would need to load these from a saved file
global train_data # Access the global train_data from the notebook state
if 'train_data' in globals() and hasattr(train_data, 'classes'):
    class_names = train_data.classes
else:
    # Fallback if train_data is not available (should ideally be loaded from a file)
    print("Warning: train_data not found in global scope. Using placeholder class names. Predictions might be incorrect.")
    class_names = [f"Actor_{i}" for i in range(131)] # Adjust 131 if your actual class count is different


@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        try:
            img_bytes = file.read()
            img = Image.open(io.BytesIO(img_bytes)).convert('RGB')
            img_tensor = transform(img).unsqueeze(0) # Add batch dimension

            with torch.no_grad():
                outputs = model(img_tensor)
                _, predicted_idx = torch.max(outputs, 1)
                predicted_class_name = class_names[predicted_idx.item()]

            return jsonify({'predicted_actor': predicted_class_name})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return "<h1>Actor Recognition API</h1><p>Send a POST request to /predict with an image file.</p>"


# To run this Flask app in Colab, you'd typically use ngrok or a similar tool
# For local testing within Colab, you can run it directly, but it won't be publicly accessible.

# This part is for running within Colab for demonstration purposes.
# In a production environment, you'd use a WSGI server like Gunicorn.
# You might need to install 'nest_asyncio' and 'pyngrok' if you want to expose it publicly.

# from google.colab.output import eval_js
# print(eval_js("google.colab.kernel.proxyPort(5000)"))

if __name__ == '__main__':
    # For running locally within Colab. Not accessible from outside by default.
    app.run(host='0.0.0.0', port=5000, debug=True)
