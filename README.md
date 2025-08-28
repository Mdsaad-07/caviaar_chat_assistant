# 🛍️ AI-Powered E-commerce Shopping Assistant

A complete AI shopping assistant solution similar to Amazon Rufus, built with **FastAPI**, **Next.js**, and **GPT-4o-mini**. This system includes intelligent chat capabilities and a modern user interface.

## 🌟 Features

### Frontend (Next.js + Tailwind)
- ✅ Modern chat UI with Amazon Rufus-style design
- ✅ Product suggestions with images and links
- ✅ Responsive design for all devices
- ✅ Real-time conversation with AI assistant
- ✅ Product recommendations and styling advice

### Backend (FastAPI + Python)
- ✅ RESTful API with FastAPI
- ✅ GPT-4o-mini integration for cost-efficient responses
- ✅ SQLite database with chat session management
- ✅ Intelligent conversation handling

### AI Capabilities
- 🤖 **Product Discovery**: Find items based on descriptions
- 💡 **Styling Advice**: Get fashion recommendations
- 🔍 **Product Comparison**: Compare different options
- 💰 **Budget-Friendly**: Uses GPT-4o-mini ($4.65/month for 3M input + 7M output tokens)

## 🚀 Quick Start

### Prerequisites
- **Node.js** 18.17.0+
- **Python** 3.8+
- **OpenAI API Key**

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set your OpenAI API key in .env file
# Edit backend/.env and replace 'your-openai-api-key-here' with your actual key

# Start FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 3. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📊 Cost Analysis (GPT-4o-mini)

For **3M input + 7M output tokens/month**:
- Input cost: 3M × $0.15/1M = $0.45
- Output cost: 7M × $0.60/1M = $4.20
- **Total monthly cost: $4.65**

## 🔧 Configuration

### Backend Environment Variables

Edit `backend/.env`:

```bash
# Required
OPENAI_API_KEY=your-openai-api-key-here

# Optional (with defaults)
OPENAI_MODEL=gpt-4o-mini
OPENAI_MAX_TOKENS=1000
OPENAI_TEMPERATURE=0.7
DATABASE_URL=sqlite:///./products.db
WEBSITE_URL=https://caviaarmode.com
```

### Frontend Environment Variables

Edit `frontend/.env.local`:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

## 🚀 Deployment

### Backend Deployment (Render)

1. **Create Render Account**: Sign up at [render.com](https://render.com)

2. **Deploy Web Service**:
   ```bash
   # Build Command
   pip install -r requirements.txt

   # Start Command
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

3. **Environment Variables** on Render:
   ```
   OPENAI_API_KEY=your-api-key
   WEBSITE_URL=https://caviaarmode.com
   DATABASE_URL=sqlite:///./products.db
   ```

### Frontend Deployment (Vercel)

1. **Connect Repository**: Link your GitHub repo to Vercel

2. **Build Settings**:
   ```bash
   # Build Command
   npm run build

   # Output Directory
   .next
   ```

3. **Environment Variables** on Vercel:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend-url.onrender.com/api
   ```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm run test
```

## ✅ What's Included

This package contains a working AI shopping assistant with:

- **Complete Backend API** with FastAPI and GPT-4o-mini integration
- **Modern Frontend** with Next.js and Tailwind CSS
- **Database Integration** with SQLite for session management
- **Professional UI/UX** inspired by Amazon Rufus
- **Cost-Efficient Setup** with GPT-4o-mini (~$5/month)
- **Production-Ready Code** that you can deploy immediately

## 🔍 Troubleshooting

### Common Issues

1. **OpenAI API Errors**
   - Verify your API key is correct in `backend/.env`
   - Check you have sufficient credits
   - Ensure rate limits aren't exceeded

2. **Database Issues**
   - Delete `products.db` and restart to reset
   - Check file permissions for SQLite

3. **CORS Errors**
   - Update `allow_origins` in `backend/app/main.py`
   - Ensure frontend URL is whitelisted

## 📈 Scaling Considerations

### Production Optimizations
- **Database**: Migrate to PostgreSQL for production
- **Caching**: Add Redis for session caching
- **CDN**: Use Cloudflare for static assets
- **Monitoring**: Implement logging and error tracking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Check the troubleshooting section
- Review the API documentation at `/docs`
- Open an issue on GitHub

---

**Built with ❤️ using FastAPI, Next.js, and GPT-4o-mini**