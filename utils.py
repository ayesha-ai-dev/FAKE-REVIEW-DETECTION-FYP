import joblib
import requests
import re ,string
# Load the model and vectorizer once
model_imdb = joblib.load('model.pkl')
vectorizer_imdb = joblib.load('vectorizer.pkl')
amazon_model = joblib.load("AmazoneModel.pkl")
amazon_vectorizer = joblib.load("AmazoneVectorizer.pkl")
trip_model = joblib.load('Tripadvisormodel.pkl')
trip_vectorizer = joblib.load('Tripadvisorvectorizer.pkl')

API_KEY = "8e316c99c4c82d2f381cb46677444084" 

def clean_text(text):
  text = text.lower()
  text = text.translate(str.maketrans("" , "" , string.punctuation))
  text = re.sub(r'\s+', ' ', text).strip()
  return text

def predict_review(review_text , source = 'imdb'):
 if not review_text.strip():
   return "Invalid", "Empty review text provided."
 if source == "amazon":
  vectorizer = amazon_vectorizer
  model = amazon_model
 elif source == "tripadvisor":
  vectorizer = trip_vectorizer 
  model = trip_model
 else: # default = imdb
  vectorizer = vectorizer_imdb
 
 model = model_imdb
 vectorized_input = vectorizer.transform([review_text])
 prediction = model.predict(vectorized_input)[0]
 if prediction == 1:
   return "Real", "This review seems genuine based on language and structure."
 else:
  return "Fake", "This review appears to be fake or suspicious."
def scrape_reviews(movie_id):
 """
 Scrape reviews using TMDB API by movie ID (e.g., 27205 for Inception).
 """
 url = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews?api_key={API_KEY}&language=en-US&page=1"
 try:
        response = requests.get(url)
        if response.status_code != 200:
            return [f"Error: TMDB API returned status {response.status_code}"]
        
        data = response.json()
        reviews = [review["content"].strip() for review in data.get("results", [])]
        return reviews[:5] if reviews else ["No reviews found."]
    
 except Exception as e:
      return [f"Error during scraping: {e}"]