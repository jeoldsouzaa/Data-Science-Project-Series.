from flask import Flask, request, render_template
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')

app = Flask(__name__)

# Load your trained TfidfVectorizer
with open('tfidf_model.pkl', 'rb') as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)

# Load your trained Logistic Regression model
with open('model.pkl', 'rb') as model_file:
    loaded_model = pickle.load(model_file)

@app.route('/')
def my_form():
    return render_template('form.html')

@app.route('/', methods=['POST'])
def my_form_post():
    stop_words = set(stopwords.words('english'))
    
    text1 = request.form['text1'].lower()
    text_final = ''.join(c for c in text1 if not c.isdigit())
    processed_doc1 = ' '.join([word for word in text_final.split() if word not in stop_words])

    # Transform the input text using the pre-fitted vectorizer
    text_vectorized = vectorizer.transform([processed_doc1])

    # Make predictions using the loaded model
    prediction = loaded_model.predict(text_vectorized)
    # Get probability scores for each class
    prediction_probs = loaded_model.predict_proba(text_vectorized)[0]
    # Probability of the predicted class
    prediction_prob = max(prediction_probs)

    return render_template('form.html', prediction="Positive" if prediction[0] == 1 else "Negative", 
                           prediction_prob=round(prediction_prob*100,2), text1=text_final)

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5002, threaded=True)
