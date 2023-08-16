from flask import Flask, render_template, request, jsonify
from bot import generate_empathetic_response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('frontend.html')

@app.route('/get_chatbot_response', methods=['POST'])
def get_chatbot_response_route():
    data = request.json
    user_input = data['user_input']

    chatbot_response = generate_empathetic_response(user_input)

    return jsonify({"response": chatbot_response})

if __name__ == '__main__':
    app.run(debug=True)
