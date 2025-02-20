from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

# Constants
BASE_URL = "https://api.socialverseapp.com/posts"
HEADERS = {"Authorization": "Bearer YOUR_API_KEY_HERE"}  # Add necessary headers if required

@app.get("/feed")
def get_personalized_feed():
    """Fetches a personalized feed."""
    response = requests.get(f"{BASE_URL}/feed", headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail=response.text)

@app.get("/posts/all")
def get_all_posts():
    """Fetches all posts."""
    response = requests.get(f"{BASE_URL}/summary/get?page=1&page_size=1000", headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail=response.text)

@app.get("/users/all")
def get_all_users():
    """Fetches all users."""
    response = requests.get("https://api.socialverseapp.com/users/get_all?page=1&page_size=1000", headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail=response.text)

@app.get("/posts/view")
def get_viewed_posts():
    """Fetches all viewed posts."""
    response = requests.get(f"{BASE_URL}/view?page=1&page_size=1000&resonance_algorithm=resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if", headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail=response.text)

@app.get("/posts/like")
def get_liked_posts():
    """Fetches all liked posts."""
    response = requests.get(f"{BASE_URL}/like?page=1&page_size=1000&resonance_algorithm=resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if", headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail=response.text)

@app.get("/posts/inspire")
def get_inspired_posts():
    """Fetches all inspired posts."""
    response = requests.get(f"{BASE_URL}/inspire?page=1&page_size=1000&resonance_algorithm=resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if", headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail=response.text)

@app.get("/posts/rating")
def get_rated_posts():
    """Fetches all rated posts."""
    response = requests.get(f"{BASE_URL}/rating?page=1&page_size=1000&resonance_algorithm=resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if", headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail=response.text)

# Data Preprocessing Functions
def normalize_data(data):
    """Applies normalization techniques to numerical data."""
    return (data - min(data)) / (max(data) - min(data)) if max(data) != min(data) else data

def encode_categorical_data(data):
    """Encodes categorical data using one-hot encoding or label encoding."""
    return {category: idx for idx, category in enumerate(set(data))}

def handle_missing_values(data):
    """Handles missing values by filling with mean/median/mode."""
    return [x if x is not None else 0 for x in data]  # Example: filling missing values with zero

# Model Architecture (Conceptual Example)
def build_model():
    """Defines a simple recommendation model with embeddings."""
    import tensorflow as tf
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Embedding, Dense, Dropout, Flatten
    
    model = Sequential([
        Embedding(input_dim=1000, output_dim=64, input_length=10),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(64, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

# Cold Start Handling
def cold_start_recommendation(user_id):
    """Handles recommendations for new users."""
    if user_id not in known_users:
        return {"recommendations": ["Trending", "Mood-Based", "Popular Posts"]}
    return {"recommendations": ["Content-Based Filtering"]}
