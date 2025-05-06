# YouTube Comment Sentiment Analyzer

A powerful web application that analyzes the sentiment of YouTube video comments using Python, FastAPI, and natural language processing techniques. Visualize sentiment distribution, polarity trends, and common words to gain insights from user feedback.

![YouTube Comment Sentiment Analysis Dashboard](https://github.com/AdarshXKumAR/YouTube-Comment-Sentiment-Analyzer/blob/main/Screenshot%20(832).png)

## 🌟 Features

- **Sentiment Analysis**: Categorizes comments as positive, negative, or neutral
- **Polarity Distribution**: Visualizes the strength of sentiment across comments
- **Common Words**: Identifies the most frequently used words in comments
- **Responsive UI**: Clean and modern interface that works on all devices
- **Comment Filtering**: Filter comments by sentiment type
- **YouTube Data Integration**: Fetches video details and comments through YouTube API

## 🛠️ Technologies Used

- **Backend**:
  - Python 3.8+
  - FastAPI framework
  - TextBlob for sentiment analysis
  - Google API Client for YouTube integration
  - scikit-learn for text processing
  - Pandas for data manipulation

- **Frontend**:
  - HTML5, CSS3, JavaScript
  - Chart.js for data visualization
  - Font Awesome for icons
  - Responsive design with CSS Grid and Flexbox

## 📋 Prerequisites

To run this project, you need:

- Python 3.8 or higher
- A YouTube Data API key (get one from the [Google Developer Console](https://console.developers.google.com/))
- pip (Python package installer)

## ⚙️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/AdarshXKumAR/YouTube-Comment-Sentiment-Analyzer.git
   cd YouTube-Comment-Sentiment-Analyzer
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env.local` file in the project root with your YouTube API key**:
   ```
   YOUTUBE_API_KEY=your_youtube_api_key_here
   ```

5. **Run the application**:
   ```bash
   uvicorn app:app --reload
   ```

6. **Access the web interface**:
   Open your browser and go to `http://127.0.0.1:8000`

## 📊 How It Works

1. Enter a YouTube video URL or ID in the input field
2. Specify the number of comments to analyze
3. Click "Analyze Comments" to start the analysis
4. View the results through interactive charts and comment listing
5. Filter comments by sentiment type using the dropdown menu

![Comment Analysis Process](https://github.com/AdarshXKumAR/YouTube-Comment-Sentiment-Analyzer/blob/main/Screenshot%20(833).png)

## 🔍 Sentiment Analysis Method

The application uses TextBlob's sentiment analysis capabilities to determine the sentiment of each comment:

- **Positive**: Polarity score > 0.1
- **Negative**: Polarity score < -0.1
- **Neutral**: Polarity score between -0.1 and 0.1

The common words feature removes stopwords (common words like "the", "and", etc.) to focus on meaningful content.

![Sentiment Distribution](https://github.com/AdarshXKumAR/YouTube-Comment-Sentiment-Analyzer/blob/main/Screenshot%20(834).png)

## 🔒 Rate Limiting & Quotas

Be aware that the YouTube Data API has quotas and rate limits. The default quota is 10,000 units per day, and each API call costs a certain number of units. For more information, visit [YouTube API Quota Documentation](https://developers.google.com/youtube/v3/getting-started#quota).

## 💬 Comments Section 

![Mobile Interface](https://github.com/AdarshXKumAR/YouTube-Comment-Sentiment-Analyzer/blob/main/Screenshot%20(835).png)

## 🚀 Future Improvements

- Add user authentication to save analysis results
- Implement more advanced NLP techniques for better sentiment accuracy
- Add support for analyzing comments from multiple videos for comparison
- Create a time-based analysis to track sentiment changes over time
- Add export functionality for reports (PDF, CSV)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- [TextBlob](https://textblob.readthedocs.io/) for the sentiment analysis functionality
- [FastAPI](https://fastapi.tiangolo.com/) for the efficient API framework
- [Chart.js](https://www.chartjs.org/) for beautiful data visualizations
- [YouTube Data API](https://developers.google.com/youtube/v3) for accessing YouTube data

---

Made with ❤️ by [Your Name]
