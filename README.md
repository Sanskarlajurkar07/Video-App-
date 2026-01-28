# API-First Video App

A React Native mobile app with Flask backend demonstrating API-first architecture, JWT authentication, and secure YouTube video abstraction.

## 🏗️ Architecture

```
React Native App  →  Flask API  →  MongoDB
                         ↓
                    YouTube (hidden behind backend logic)
```

**Key Principle**: The mobile app acts as a thin client with NO business logic. All data processing happens on the backend.

## 📁 Project Structure

```
video-app/
├── backend/                 # Flask API
│   ├── app.py              # Main Flask app
│   ├── config.py           # Configuration
│   ├── requirements.txt    # Python dependencies
│   ├── models/             # MongoDB models
│   ├── routes/             # API endpoints
│   ├── middleware/         # JWT authentication
│   └── utils/              # Token utilities
│
└── mobile/                  # React Native App
    ├── App.js              # Entry point
    ├── package.json        # Dependencies
    └── src/
        ├── screens/        # App screens
        ├── components/     # UI components
        ├── services/       # API client
        ├── context/        # Auth state
        └── navigation/     # Navigation config
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- MongoDB (running locally or MongoDB Atlas)
- Android Studio / Xcode (for mobile development)

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
# Edit .env with your MongoDB URI and secrets

# Run the server
python app.py
```

The API will be available at `http://localhost:5000`

### Mobile Setup

```bash
# Navigate to mobile
cd mobile

# Install dependencies
npm install

# For Android
npm run android

# For iOS (macOS only)
cd ios && pod install && cd ..
npm run ios
```

## 🔐 API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/signup` | Register new user |
| POST | `/auth/login` | Login, returns JWT |
| GET | `/auth/me` | Get current user profile |
| POST | `/auth/logout` | Logout user |

### Videos

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/dashboard` | Get 2 featured videos |
| GET | `/video/<id>/stream?token=...` | Get video stream URL |

## 🎥 YouTube Abstraction

The app **never exposes raw YouTube URLs**. Instead:

1. Dashboard returns video metadata + `playback_token`
2. App requests `/video/<id>/stream?token=...`
3. Backend verifies token and returns embed-safe URL
4. WebView plays the embedded video

This ensures:
- YouTube IDs are never exposed to the client
- Playback tokens expire after 1 hour
- Token verification prevents unauthorized access

## 🔑 JWT Flow

1. User logs in with email/password
2. Backend validates credentials and returns JWT
3. App stores JWT securely with AsyncStorage
4. All subsequent requests include JWT in Authorization header
5. Backend validates JWT on protected routes

## 📱 App Screens

1. **Login** - Email/password authentication
2. **Signup** - User registration
3. **Dashboard** - Displays 2 video tiles
4. **Video Player** - Plays embedded YouTube videos
5. **Settings** - User profile and logout

## 🛠️ Tech Stack

### Backend
- Flask 3.0
- PyMongo (MongoDB)
- PyJWT (authentication)
- bcrypt (password hashing)
- Flask-CORS

### Mobile
- React Native 0.77
- React Navigation 7
- AsyncStorage
- WebView (for YouTube embed)

## 📋 Environment Variables

### Backend (.env)
```
MONGODB_URI=mongodb://localhost:27017/video_app
JWT_SECRET_KEY=your-jwt-secret
JWT_EXPIRY_HOURS=24
PLAYBACK_SECRET_KEY=your-playback-secret
```

### Mobile (.env.example)
```
API_BASE_URL=http://10.0.2.2:5000  # Android emulator
# Use localhost for iOS or your IP for physical device
```

## ✅ Features Implemented

- [x] JWT Authentication (signup, login, logout)
- [x] Password hashing with bcrypt
- [x] Protected API routes
- [x] Video dashboard (2 videos)
- [x] Playback token system
- [x] YouTube embed abstraction
- [x] Video player with controls
- [x] User profile/settings

## 📄 License

MIT
