from flask import Flask, request, jsonify
from flask_bootstrap import Bootstrap
from flask_cors import CORS
import spacy
from collections import Counter
import random
from PyPDF2 import PdfReader

app = Flask(__name__)
Bootstrap(app)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins

# Load English tokenizer, tagger, parser, NER, and word vectors
nlp = spacy.load("en_core_web_sm")

def generate_mcqs(text, num_questions=5):
    if not text.strip():
        return []

    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    num_questions = min(num_questions, len(sentences))
    selected_sentences = random.sample(sentences, num_questions)
    mcqs = []

    for sentence in selected_sentences:
        sent_doc = nlp(sentence)
        nouns = [token.text for token in sent_doc if token.pos_ == "NOUN"]

        if len(nouns) < 2:
            continue

        noun_counts = Counter(nouns)
        subject = noun_counts.most_common(1)[0][0]
        question_stem = sentence.replace(subject, "______")
        answer_choices = [subject]

        distractors = list(set(nouns) - {subject})
        while len(distractors) < 3:
            distractors.append("[Distractor]")

        distractors = distractors[:3]
        answer_choices.extend(distractors)
        random.shuffle(answer_choices)
        correct_answer_index = answer_choices.index(subject)
        mcqs.append([question_stem, answer_choices, correct_answer_index])

    return mcqs

@app.route('/', methods=['POST'])
def index():
    text = ""

    if 'files[]' in request.files:
        files = request.files.getlist('files[]')
        for file in files:
            if file.filename.endswith('.pdf'):
                text += process_pdf(file)
            elif file.filename.endswith('.txt'):
                text += file.read().decode('utf-8')
    else:
        text = request.form.get('text', '')

    if not text.strip():
        return jsonify({'error': 'No text provided for MCQ generation'}), 400

    num_questions = int(request.form.get('num_questions', 5))
    mcqs = generate_mcqs(text, num_questions=num_questions)
    return jsonify(mcqs)

def process_pdf(file):
    text = ""
    pdf_reader = PdfReader(file)
    for page_num in range(len(pdf_reader.pages)):
        page_text = pdf_reader.pages[page_num].extract_text()
        if page_text:
            text += page_text
    return text

if __name__ == '__main__':
    app.run(debug=True)
