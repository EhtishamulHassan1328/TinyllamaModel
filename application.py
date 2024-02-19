from os import pipe
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_ngrok import run_with_ngrok
from transformers import pipeline

# Initialize the Flask application
application = Flask(__name__)

# Run the Flask application with ngrok
run_with_ngrok(application)

# Enabling CORS for all routes
CORS(application)

# Random API key
API_KEY = 'ehtisham'

# Load the text generation pipeline
pipe = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")

# Home Page Route
@application.route('/', methods=['GET'])
def home():
    return "Home route"

# Generate Response Route
@application.route('/generate_response', methods=['POST'])
def generate_response():
    try:
        if 'api_key' not in request.json:
            return jsonify({'error': 'API key not passed by the user.'}), 401

        if request.json['api_key'] != API_KEY:
            return jsonify({'error':'API key not matched.'}), 401

        # Get the input history from the request
        history = request.json.get('history')

        # Check if history is None or empty
        if history is None or len(history) == 0:
            return jsonify({'error': 'Please provide a valid history'}), 400

        # Check if the last message in history has the role of the user
        if history[-1]['role'] != 'user':
            return jsonify({'error': 'The last message in history should be from the user.'}), 400

        try:
            # Concatenate the history messages into a single string
            history_text = " ".join([msg['message'] for msg in history])

            # Generate response using the text generation pipeline
            response = pipe(history_text, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)

            # Extract the generated text from the response
            generated_text = response[0]["generated_text"]

            # Append the generated text to the history with assistant role
            history.append({
                'role': 'assistant',
                'message': generated_text
            })

            # Construct the JSON response manually
            response_data = {'history': history}
            return jsonify(response_data), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run the Flask application
if __name__ == '__main__':
    application.run()
