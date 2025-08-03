# app.py

from flask import Flask, render_template, request
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

class Summarizer:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))

    def _calculate_sentence_scores(self, text):
        sentences = sent_tokenize(text)
        if not sentences:
            return {}
            
        word_freq = {}
        for word in word_tokenize(text.lower()):
            if word.isalnum() and word not in self.stop_words:
                word_freq[word] = word_freq.get(word, 0) + 1

        sentence_scores = {}
        for sentence in sentences:
            score = 0
            for word in word_tokenize(sentence.lower()):
                if word in word_freq:
                    score += word_freq[word]
            sentence_scores[sentence] = score
        return sentence_scores

    def summarize(self, text, num_sentences=3):
        if not text.strip():
            return "Please enter some text to summarize."
        
        sentence_scores = self._calculate_sentence_scores(text)
        summarized_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)
        return ' '.join(summarized_sentences[:num_sentences])

# --- Flask App Setup ---
# Tell Flask to look for HTML files in the current folder ('.')
app = Flask(__name__, template_folder='.') 
summarizer = Summarizer()

@app.route('/', methods=['GET', 'POST'])
def index():
    summary_text = ""
    original_text = ""
    if request.method == 'POST':
        original_text = request.form['raw_text']
        num_sentences = int(request.form.get('num_sentences', 3))
        summary_text = summarizer.summarize(original_text, num_sentences)

    return render_template('index.html', summary=summary_text, original_text=original_text)

if __name__ == '__main__':
    app.run(debug=True)