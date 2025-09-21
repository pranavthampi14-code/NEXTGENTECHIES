from flask import Flask, request, jsonify, send_from_directory
import os
from preprocessing import pdf_to_images, preprocess_image
from ocr_engine import ocr_image
from extractor import extract_text_block

# Gemini SDK
try:
    from google import genai
except Exception:
    genai = None

app = Flask(__name__, static_folder='../frontend', static_url_path='/')
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'no file uploaded'}), 400
    f = request.files['file']
    filepath = os.path.join(UPLOAD_FOLDER, f.filename)
    f.save(filepath)

    images = pdf_to_images(filepath)
    full_text = []
    pages_res = []
    for i, img in enumerate(images):
        proc = preprocess_image(img)
        ocr_res = ocr_image(proc)
        text = ocr_res.get('text','')
        pages_res.append({'page': i+1, 'text': text})
        full_text.append(text)

    joined = "\n\n".join(full_text)
    # Basic extraction (returns full OCR text for now)
    extracted = extract_text_block(joined)

    return jsonify({'file': f.filename, 'pages': len(images), 'pages_text': pages_res, 'extracted_text': extracted})

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json() or {}
    text = data.get('text','').strip()
    if not text:
        return jsonify({'error':'no text provided'}), 400

    # Initialize Gemini client
    if genai is None:
        return jsonify({'error':'google-genai library not installed on server'}), 500

    api_key = os.environ.get('GEMINI_API_KEY')
    client = genai.Client(api_key=api_key) if api_key else genai.Client()

    prompt = (
        "You are a helpful assistant that explains legal documents in plain English for a non-expert. "
        "Given the following legal text, produce:\n1) a concise summary (3-5 short bullets),\n2) a plain-language explanation of the obligations and risks,\n3) a short list of questions the signer should ask a lawyer.\n\nLegal text:\n" + text
    )

    try:
        response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
        # many SDK responses expose .text
        summary = getattr(response, 'text', None) or str(response)
    except Exception as e:
        return jsonify({'error':'gemini API error', 'detail': str(e)}), 500

    return jsonify({'summary': summary})

# Serve frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
