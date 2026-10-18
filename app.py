from flask import Flask , render_template, request
from utils import predict_review, scrape_reviews, clean_text

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', source="imdb")

@app.route('/predict', methods=['POST'])
def predict():
    review_text = request.form.get('review', '').strip()
    source = request.form.get('source', 'imdb') # dropdown: imdb or amazon

    if not review_text:
        return render_template('index.html', source=source)

    review_text = clean_text(review_text)
    prediction, reason = predict_review(review_text, source)

    return render_template('result.html', prediction=prediction, reason=reason, source=source)

@app.route('/scrape', methods=['POST'])
def scrape():
    scrape_source = request.form.get('scrape_source', 'tmdb')
    movie_id = request.form.get('movie_id', '').strip()

    if scrape_source == 'tmdb':
        if not movie_id:
            return render_template('result.html', prediction="Error", reason="TMD B Movie ID is missing.")
        reviews = scrape_reviews(movie_id)
    elif scrape_source == 'amazon':
        # NOTE: Amazon scraping logic is complex and placeholder data is shown in original documents.
        # This part of the code needs external scraping logic or direct data to function.
        # Assuming the final code uses scrape_reviews(scrape_source) if implemented.
        # Using a dummy value for now since the full scrape logic isn't provided.
        reviews = [] # Replace with actual scraping function call if implemented

    batch_results = []
    for review in reviews:
        clean_review = clean_text(review)
        prediction, reason = predict_review(clean_review, source='amazon') # Assuming scraped reviews are checked against Amazon model
        batch_results.append((review, prediction, reason))

    return render_template('result.html', batch_results=batch_results)

if __name__ == '__main__':
    # Yeh line debug mode mein chalti hai
    app.run(debug=True)