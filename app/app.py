from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

app = Flask(__name__)

#https://github.com/McGill-MMA-EnterpriseAnalytics/Anime-Rating-Prediction-and-Recommendation/blob/main/Data_Preprocess_And_Prediction.ipynb
#https://www.kaggle.com/code/tugbabz/anime-rating-prediction-with-matrix-factorization/notebook


df = pd.read_csv('../Anime_data.csv')
df = df.dropna(subset=["Title", "Genre", "Synopsis", "Type", "Producer", "Studio", "Rating"])

features = ["Title", "Genre", "Synopsis", "Type", "Producer", "Studio"]


X = df[features]
y = df['Rating']
y = y.apply(lambda x : str(x))

X_train, X_test, y_train, y_test = train_test_split(X['Synopsis'], y, test_size=0.2, random_state=42)

wordToVector = TfidfVectorizer(stop_words='english')


X_train_matrix = wordToVector.fit_transform(X_train)

X_test_matrix = wordToVector.transform(X_test)

model = GradientBoostingRegressor()

model.fit(X_train_matrix, y_train)

def model_pred(Title, Genre, Synopsis, Type, Producer, Studio):
    new_data = pd.DataFrame({
        'Title': [Title],
        'Genre': [Genre],
        'Synopsis': [Synopsis],
        'Type': [Type],
        'Producer': [Producer],
        'Studio': [Studio]
    })

    new_matrix = wordToVector.transform(new_data['Synopsis'])
    rat_pred = model.predict(new_matrix)
    return rat_pred[0]



@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Récupérer les données saisies par l'utilisateur
    
    Title = request.form['Title']
    Genre = request.form['Genre']
    Synopsis = request.form['Synopsis']
    Type = request.form['Type']
    Producer = request.form['Producer']
    Studio = request.form['Studio']

    rating = model_pred(Title, Genre, Synopsis, Type, Producer, Studio)

    # Afficher le résultat de la prédiction à l'utilisateur
    return render_template('resultat.html', rating= rating)
    #return render_template('resultat.html', rating=jsonify({'rating':  Title + "404"}))


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

