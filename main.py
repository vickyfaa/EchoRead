# main.py

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize


class Summarizer:

    def __init__(self):
        self.stop_words = set(stopwords.words('english'))

    def _calculate_sentence_scores(self, text):
        
        sentences = sent_tokenize(text)
        word_freq = {}
        
        # Calculate word frequencies for the entire text
        for word in word_tokenize(text.lower()):
            if word.isalnum() and word not in self.stop_words:
                word_freq[word] = word_freq.get(word, 0) + 1

        # Score each sentence based on the words it contains
        sentence_scores = {}
        for sentence in sentences:
            score = 0
            for word in word_tokenize(sentence.lower()):
                if word in word_freq:
                    score += word_freq[word]
            sentence_scores[sentence] = score
            
        return sentence_scores

    def summarize(self, text, num_sentences=3):
        """
        The main public method to generate the summary.
        This is the method users will call.
        """
        if not text.strip():
            return "Error: Input text is empty."

        sentence_scores = self._calculate_sentence_scores(text)

        # Get the top N sentences with the highest scores
        summarized_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)
        
        # Return the joined summary
        return ' '.join(summarized_sentences[:num_sentences])


# --- How to use the Summarizer class ---
if __name__ == "__main__":
    # 1. Create an instance of the class
    my_summarizer = Summarizer()

    # 2. Define the text you want to summarize
    long_article = """
    Technology is the application of conceptual knowledge for achieving practical goals, especially in a reproducible way. 
    The word technology can also mean the products resulting from such efforts, including both tangible tools such as utensils or machines, 
    and intangible ones such as software. Technology plays a critical role in science, engineering, and everyday life. 
    Engineers apply scientific principles to create new technologies.
    """

    # 3. Call the summarize method
    summary = my_summarizer.summarize(long_article, 2)

    # 4. Print the result
    print("--- SUMMARY ---")
    print(summary)