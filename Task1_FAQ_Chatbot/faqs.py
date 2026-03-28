import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# डाउनलोड (runs only first time)
nltk.download('punkt')
nltk.download('stopwords')

# ================= FAQ DATA =================
faqs = [
    ("What is AI?", "AI stands for Artificial Intelligence."),
    ("What is Python?", "Python is a programming language."),
    ("What is machine learning?", "Machine learning is a subset of AI."),
    ("What is NLP?", "NLP stands for Natural Language Processing."),
    ("What is ChatGPT?", "ChatGPT is an AI chatbot developed by OpenAI."),
]

# ================= PREPROCESS FUNCTION =================
def preprocess(text):
    tokens = word_tokenize(text.lower())
    tokens = [w for w in tokens if w not in stopwords.words('english')]
    tokens = [w for w in tokens if w not in string.punctuation]
    return " ".join(tokens)

# ================= PREPARE DATA =================
questions = [q for q, a in faqs]
processed_questions = [preprocess(q) for q in questions]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(processed_questions)

# ================= CHATBOT FUNCTION =================
def get_answer(user_input):
    user_processed = preprocess(user_input)
    user_vector = vectorizer.transform([user_processed])

    similarity = cosine_similarity(user_vector, X)
    index = similarity.argmax()

    # Confidence check (important!)
    if similarity[0][index] < 0.2:
        return "Sorry, I don't understand your question."

    return faqs[index][1]

# ================= CHAT LOOP =================
print("FAQ Chatbot 🤖 (type 'exit' to stop)")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Bot: Goodbye!")
        break

    answer = get_answer(user_input)
    print("Bot:", answer)