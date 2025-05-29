from flask import Flask, request, jsonify
import requests
import mammoth
from io import BytesIO
from pdfminer.high_level import extract_text

app = Flask(__name__)

@app.route('/parse-document', methods=['POST'])
def parse_document():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'Missing URL'}), 400

    try:
        file_response = requests.get(url)
        buffer = BytesIO(file_response.content)

        if url.endswith('.pdf'):
            text = extract_text(buffer)
        elif url.endswith('.docx'):
            result = mammoth.extract_raw_text(buffer)
            text = result.value
        else:
            return jsonify({'error': 'Unsupported file type'}), 400

        return jsonify({'text': text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
