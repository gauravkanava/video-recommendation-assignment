from fastapi import FastAPI, Query
from typing import List, Dict
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Embedding, Dense, Flatten

app = FastAPI(title="Video Recommendation Engine")

# Mock Video Dataset
video_data = [
    {"id": 101, "title": "Motivational Talk", "category_id": 1, "views": 5000, "likes": 120},
    {"id": 102, "title": "Life Lessons", "category_id": 2, "views": 3000, "likes": 80},
    {"id": 103, "title": "Tech Innovations", "category_id": 3, "views": 4000, "likes": 100},
    {"id": 104, "title": "Fitness Guide", "category_id": 1, "views": 7000, "likes": 200},
    {"id": 105, "title": "Self-Improvement", "category_id": 2, "views": 2500, "likes": 90}
]

# Mock user engagement data (user_id, video_id, engagement_score) 
user_engagement = [
    {"user_id": 1, "video_id": 101, "engagement_score": 4.5},
    {"user_id": 1, "video_id": 102, "engagement_score": 4.0},
    {"user_id": 2, "video_id": 103, "engagement_score": 3.5},
    {"user_id": 2, "video_id": 104, "engagement_score": 5.0},
    {"user_id": 3, "video_id": 105, "engagement_score": 4.8}
]

# Prepare Training Data (User-Video Interaction Matrix)
num_users = 10  # Simulated 10 users
num_videos = len(video_data)
user_video_matrix = np.random.randint(0, 2, size=(num_users, num_videos))  # Simulated engagement data

# Define Deep Learning Model for Recommendations
class VideoRecommendationModel(keras.Model):
    def __init__(self, num_videos):
        super().__init__()
        self.embedding = Embedding(input_dim=num_videos, output_dim=16)
        self.dense1 = Dense(32, activation="relu")
        self.dense2 = Dense(16, activation="relu")
        self.output_layer = Dense(1, activation="sigmoid")

    def call(self, inputs):
        x = self.embedding(inputs)
        x = Flatten()(x)
        x = self.dense1(x)
        x = self.dense2(x)
        return self.output_layer(x)

# Initialize & Train the Model
model = VideoRecommendationModel(num_videos)
model.compile(optimizer="adam", loss="binary_crossentropy")

# Correcting the Shape of Target Labels
y_train = np.random.randint(0, 2, size=(num_users, 1))

# Train the model 
model.fit(user_video_matrix, y_train, epochs=10, verbose=1)

# DNN-Based Video Recommendation Function
def recommend_videos(user_id: int) -> List[Dict]:
    video_ids = np.array([video["id"] for video in video_data])
    predicted_scores = model.predict(video_ids)

    # Sort videos by predicted scores
    recommended_videos = sorted(zip(video_data, predicted_scores.flatten()), key=lambda x: x[1], reverse=True)
    return [{"id": v[0]["id"], "title": v[0]["title"], "predicted_score": round(v[1], 2)} for v in recommended_videos[:3]]

# Cold Start Handling (If User Has No Engagement Data)
def cold_start_recommendations() -> List[Dict]:
    return sorted(video_data, key=lambda x: x["likes"], reverse=True)[:3]  # Top 3 most liked videos

# API: Get DNN-Based Personalized Recommendations
@app.get("/feed", summary="Get personalized recommendations")
def get_feed(username: str = Query(..., description="Username for recommendations")):
    user_id = hash(username) % num_users  # Generate a fake user ID for testing
    
    if user_id in [eng["user_id"] for eng in user_engagement]:
        recommendations = recommend_videos(user_id)
    else:
        recommendations = cold_start_recommendations()

    return {"username": username, "recommendations": recommendations}

# API: Get All Videos (Mocked Data)
@app.get("/posts/all", summary="Get all videos")
def get_all_posts():
    return {"status": "success", "message": "Mocked post data", "posts": video_data}
