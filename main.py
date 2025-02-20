from fastapi import FastAPI, HTTPException
import requests
import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Flatten, Dense, Dropout, concatenate

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Environment variables
FLIC_TOKEN = os.getenv("FLIC_TOKEN")
API_BASE_URL = os.getenv("API_BASE_URL")

# Authorization header
headers = {
    "Flic-Token": FLIC_TOKEN
}

# Data Preprocessing
data = pd.read_csv('your_data.csv')
categorical_cols = ['category', 'mood']
numerical_cols = ['view_count', 'like_count', 'rating']

numerical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_cols),
        ('cat', categorical_transformer, categorical_cols)
    ])

X = preprocessor.fit_transform(data)

# Model Architecture
num_numerical_features = X.shape[1] - len(categorical_cols)
embedding_input_dims = [data[col].nunique() for col in categorical_cols]
embedding_output_dims = [5 for _ in categorical_cols]

numerical_input = Input(shape=(num_numerical_features,), name='numerical_input')
categorical_inputs = []
categorical_embeddings = []
for i, col in enumerate(categorical_cols):
    categorical_input = Input(shape=(1,), name=f'{col}_input')
    embedding = Embedding(input_dim=embedding_input_dims[i], output_dim=embedding_output_dims[i], input_length=1)(categorical_input)
    embedding = Flatten()(embedding)
    categorical_inputs.append(categorical_input)
    categorical_embeddings.append(embedding)

all_features = concatenate([numerical_input] + categorical_embeddings)
x = Dense(128, activation='relu')(all_features)
x = Dropout(0.5)(x)
x = Dense(64, activation='relu')(x)
x = Dropout(0.5)(x)
output = Dense(1, activation='sigmoid', name='output')(x)

model = Model(inputs=[numerical_input] + categorical_inputs, outputs=output)
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Cold Start Handling
def cold_start_recommendations(user_mood):
    mood_based_recommendations = data[data['mood'] == user_mood].head(10)
    if mood_based_recommendations.empty:
        content_based_recommendations = data[data['category'] == 'default_category'].head(10)
    else:
        content_based_recommendations = mood_based_recommendations
    if content_based_recommendations.empty:
        popularity_based_recommendations = data.sort_values(by='view_count', ascending=False).head(10)
    else:
        popularity_based_recommendations = content_based_recommendations
    return popularity_based_recommendations

# Main endpoints
@app.get("/feed")
async def get_personalized_feed(username: str):
    try:
        response = requests.get(f"{API_BASE_URL}/posts/summary/get", headers=headers, params={"username": username})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/feed/category")
async def get_category_based_feed(username: str, category_id: int):
    try:
        response = requests.get(f"{API_BASE_URL}/posts/summary/get", headers=headers, params={"username": username, "category_id": category_id})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/posts/all")
async def get_all_videos():
    try:
        response = requests.get(f"{API_BASE_URL}/posts/summary/get", headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/cold_start")
async def get_cold_start_recommendations(user_mood: str):
    recommendations