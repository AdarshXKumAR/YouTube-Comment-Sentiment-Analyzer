import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import googleapiclient.discovery
from textblob import TextBlob
from dotenv import load_dotenv
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import re

load_dotenv('.env.local')

# Initialize FastAPI app
app = FastAPI(
    title="YouTube Comment Sentiment Analysis API",
    description="API to analyze sentiment of YouTube comments",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for demo purposes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request models
class CommentRequest(BaseModel):
    video_id: str
    comment_count: int = 100

class CommentResponse(BaseModel):
    comment_id: str
    text: str
    author: str
    publish_date: str
    likes: int
    sentiment: str
    polarity: float

class VideoInfoResponse(BaseModel):
    video_id: str
    title: str
    channel_title: str
    thumbnail_url: str
    published_at: str
    view_count: Optional[int] = None
    like_count: Optional[int] = None
    comment_count: Optional[int] = None

class AnalysisResponse(BaseModel):
    video_id: str
    comments: List[CommentResponse]
    sentiment_counts: dict
    common_words: List[dict]

# YouTube API setup
def get_youtube_client():
    api_service_name = "youtube"
    api_version = "v3"
    # You should set the YouTube API key as an environment variable
    api_key = os.environ.get("YOUTUBE_API_KEY")
    
    if not api_key:
        raise HTTPException(status_code=500, detail="YouTube API key not found")
    
    return googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=api_key
    )

# Function to clean text
def clean_text(text):
    # Remove special characters and URLs
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^A-Za-z0-9\s]', '', text)
    text = text.lower()
    return text

# Function to get sentiment
def get_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    
    if polarity > 0.1:
        return "Positive", polarity
    elif polarity < -0.1:
        return "Negative", polarity
    else:
        return "Neutral", polarity

# Function to get common words
def get_common_words(comments, n=10):
    # Combine all comments
    combined_text = ' '.join([clean_text(comment.text) for comment in comments])
    
    # Create a count vectorizer with stopwords
    vectorizer = CountVectorizer(stop_words='english')
    word_count = vectorizer.fit_transform([combined_text])
    
    # Get the most common words
    words = vectorizer.get_feature_names_out()
    counts = word_count.toarray()[0]
    
    # Sort by count
    word_counts = sorted(zip(words, counts), key=lambda x: x[1], reverse=True)
    return [{"word": word, "count": int(count)} for word, count in word_counts[:n]]

# Function to fetch video info
def fetch_video_info(video_id):
    youtube = get_youtube_client()
    
    request = youtube.videos().list(
        part="snippet,statistics",
        id=video_id
    )
    
    response = request.execute()
    
    if not response.get("items"):
        raise HTTPException(status_code=404, detail="Video not found")
    
    video_data = response["items"][0]
    snippet = video_data.get("snippet", {})
    statistics = video_data.get("statistics", {})
    
    return VideoInfoResponse(
        video_id=video_id,
        title=snippet.get("title", ""),
        channel_title=snippet.get("channelTitle", ""),
        thumbnail_url=snippet.get("thumbnails", {}).get("high", {}).get("url", ""),
        published_at=snippet.get("publishedAt", ""),
        view_count=int(statistics.get("viewCount", 0)) if "viewCount" in statistics else None,
        like_count=int(statistics.get("likeCount", 0)) if "likeCount" in statistics else None,
        comment_count=int(statistics.get("commentCount", 0)) if "commentCount" in statistics else None
    )

# Function to fetch comments
def fetch_youtube_comments(video_id, max_comments=100):
    youtube = get_youtube_client()
    
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=min(max_comments, 100),  # YouTube API limits to 100 per request
        textFormat="plainText"
    )
    
    try:
        response = request.execute()
    except Exception as e:
        if "commentsDisabled" in str(e):
            raise HTTPException(status_code=400, detail="Comments are disabled for this video")
        raise HTTPException(status_code=500, detail=f"YouTube API error: {str(e)}")
    
    comment_items = response.get("items", [])
    
    # For large comment counts, we might need to use pagination (nextPageToken)
    next_page_token = response.get("nextPageToken")
    comments_fetched = len(comment_items)
    
    while next_page_token and comments_fetched < max_comments:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=min(max_comments - comments_fetched, 100),
            pageToken=next_page_token,
            textFormat="plainText"
        )
        response = request.execute()
        comment_items.extend(response.get("items", []))
        next_page_token = response.get("nextPageToken")
        comments_fetched = len(comment_items)
    
    # Extract comments data
    comments = []
    for item in comment_items:
        snippet = item.get("snippet", {}).get("topLevelComment", {}).get("snippet", {})
        comment_id = item.get("id", "")
        text = snippet.get("textDisplay", "")
        author = snippet.get("authorDisplayName", "")
        publish_date = snippet.get("publishedAt", "")
        likes = snippet.get("likeCount", 0)
        
        # Get sentiment
        sentiment, polarity = get_sentiment(text)
        
        comments.append(CommentResponse(
            comment_id=comment_id,
            text=text,
            author=author,
            publish_date=publish_date,
            likes=likes,
            sentiment=sentiment,
            polarity=polarity
        ))
    
    return comments

# Serve static files
# app.mount("/static", StaticFiles(directory="static"), name="static")

# Root endpoint
@app.get("/")
def serve_frontend():
    return FileResponse("templates/index.html")

# Video info endpoint
@app.get("/video_info/{video_id}", response_model=VideoInfoResponse)
def get_video_info(video_id: str):
    try:
        return fetch_video_info(video_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Fetch comments endpoint
@app.post("/analyze_comments/", response_model=AnalysisResponse)
def analyze_comments(request: CommentRequest):
    try:
        # Check if video exists and comments are enabled
        video_info = fetch_video_info(request.video_id)
        
        # Fetch comments
        comments = fetch_youtube_comments(request.video_id, request.comment_count)
        
        # Count sentiments
        sentiment_counts = {
            "Positive": len([c for c in comments if c.sentiment == "Positive"]),
            "Negative": len([c for c in comments if c.sentiment == "Negative"]),
            "Neutral": len([c for c in comments if c.sentiment == "Neutral"])
        }
        
        # Get common words
        common_words = get_common_words(comments)
        
        return AnalysisResponse(
            video_id=request.video_id,
            comments=comments,
            sentiment_counts=sentiment_counts,
            common_words=common_words
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)