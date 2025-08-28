# 🚀 Setup Instructions

## Step-by-Step Setup Guide

### 1. Extract the Project
Extract the `ecommerce-chatbot.zip` file to your desired location.

### 2. Backend Setup

```bash
# Navigate to backend directory
cd ecommerce-chatbot/backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# IMPORTANT: Edit the .env file and add your OpenAI API key
# Replace 'your-openai-api-key-here' with your actual OpenAI API key
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory (in a new terminal)
cd ecommerce-chatbot/frontend

# Install dependencies
npm install
```

### 4. Run the Application

#### Terminal 1 - Backend:
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```

### 5. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🔑 Important Notes

1. **OpenAI API Key**: You must add your OpenAI API key to `backend/.env`
2. **Both services must be running**: Backend on port 8000, Frontend on port 3000
3. **Test the connection**: Try sending a message in the chat interface

## 🎯 What You Get

- Working AI chat interface
- GPT-4o-mini integration
- Session management
- Professional UI/UX
- Cost-efficient setup (~$5/month)

## 🆘 Need Help?

- Check that both backend and frontend are running
- Verify your OpenAI API key is set correctly
- Make sure you have Python 3.8+ and Node.js 18+
- Check the browser console for any errors

Happy coding! 🚀