from os import pipe
from flask import Flask, jsonify, request
from flask_cors import CORS



application = Flask(__name__)

#Enabling CORS for all routes
CORS(application)

# Random API key
API_KEY = 'ehtisham'

# Home Page Route
@application.route('/', methods=['GET'])
def home():
    return "Home route"


@application.route('/generate_response', methods=['POST'])
def generate_response():

    try:
        if 'api_key' not in request.form:
            return jsonify({'error': 'API key not passed by the user.'}),401
        
        if request.form['api_key']!=API_KEY:
            return jsonify({'error':'API key not matched.'}),401
        

        # Get the input query from the request
        user_query = request.json.get('query')

        # Check if user_query is None or empty
        if user_query is None or user_query == '':
            return jsonify({'error': 'Please provide a valid query'}), 400

        try:
            # Generate response using the text generation pipeline
            response = pipe(user_query, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)

            # Extract the generated text from the response
            generated_text = response[0]["generated_text"]

            return jsonify({'response': generated_text}), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Main
if __name__ == "__main__":
    application.run(debug=True)