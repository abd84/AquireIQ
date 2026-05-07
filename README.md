# AcquireIQ

> **AI-Powered M&A Lead Generation Platform**

AcquireIQ is a full-stack application that automates the discovery, enrichment, scoring, and outreach pipeline for identifying high-quality acquisition targets. Powered by Google Places API, Hunter.io, and Gemini 2.5 Flash AI.

---

## 🚀 Features

- **Lead Discovery**: Google Places API integration for location-based company discovery
- **AI Scoring**: Gemini 2.5 Flash for acquisition readiness analysis
- **Email Enrichment**: Hunter.io API for executive contact discovery
- **Premium UI**: Glassmorphism design with Framer Motion animations
- **Real-time Updates**: Live company status tracking and score updates
- **Outreach Queue**: Automated email generation for qualified leads

---

## 🏗️ Architecture

### Frontend
- **Framework**: Next.js 16.2.4 with App Router & TypeScript 5
- **Styling**: Tailwind CSS 4 with Framer Motion 12.38.0
- **UI Components**: Lucide React icons, glassmorphism patterns
- **Ports**: Local 3005 | Production 3005

### Backend
- **Framework**: FastAPI (Python 3.12)
- **Server**: Uvicorn 0.30.6 ASGI
- **Database**: SQLite with SQLAlchemy 2.0 async ORM
- **AI Model**: Google Gemini 2.5 Flash
- **Ports**: Local 8080 | Production 8080

### External Services
- Google Places API (location data)
- Hunter.io API (email discovery)
- Google Generative AI / Gemini 2.5 Flash (scoring & analysis)

---

## 📋 Requirements

**Development:**
- Node.js >= 20.9.0
- Python >= 3.12
- npm >= 10.8.2

**Production:**
- DigitalOcean Ubuntu 24.04.2 LTS droplet
- 563+ system packages (see deployment)

**API Keys (Required):**
- `GOOGLE_PLACES_API_KEY` - Google Cloud
- `GEMINI_API_KEY` - Google AI Studio
- `HUNTER_API_KEY` - Hunter.io

---

## 🛠️ Local Development

### 1. Clone & Setup

```bash
git clone https://github.com/abd84/AcquireIQ.git
cd AcquireIQ
```

### 2. Environment Setup

Create `.env` file in the project root:

```env
DATABASE_URL=sqlite+aiosqlite:///./acquireiq.db
GOOGLE_PLACES_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here
HUNTER_API_KEY=your_key_here
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your@gmail.com
SMTP_PASSWORD=your_app_password
```

### 3. Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8080
```

Backend runs on: **http://localhost:8080**

### 4. Frontend Setup

```bash
cd frontend
npm install
npm start -- -p 3005
```

Frontend runs on: **http://localhost:3005**

---

## 📦 Project Structure

```
AcquireIQ/
├── backend/
│   ├── app/
│   │   ├── api/routes/          # API endpoints (search, companies, outreach)
│   │   ├── services/
│   │   │   ├── ai/              # Gemini client & prompts
│   │   │   ├── discovery/       # Google Places integration
│   │   │   ├── enrichment/      # Hunter.io, web scraping
│   │   │   └── scoring/         # Acquisition scoring engine
│   │   ├── models/              # SQLAlchemy ORM models
│   │   ├── config.py            # Settings & environment config
│   │   └── main.py              # FastAPI app entry point
│   ├── requirements.txt         # Python dependencies
│   └── acquireiq.db             # SQLite database
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx         # Dashboard landing
│   │   │   ├── companies/       # Companies list & detail
│   │   │   ├── search/          # Lead search interface
│   │   │   ├── outreach/        # Email outreach queue
│   │   │   └── layout.tsx       # Root layout with animations
│   │   ├── components/
│   │   │   └── Layout.tsx       # Sidebar with glassmorphism
│   │   └── lib/utils.ts         # API client & utilities
│   ├── package.json             # Node dependencies
│   └── next.config.ts           # Next.js configuration
│
└── .gitignore
```

---

## 🚀 Deployment (DigitalOcean)

### Prerequisites
- DigitalOcean account with Ubuntu 24.04.2 LTS droplet
- SSH access with password: `Abdullah@123Naeem`

### Deploy Steps

```bash
# 1. SSH into droplet
ssh root@147.182.173.184

# 2. Archive and transfer code
tar --exclude='.git' --exclude='node_modules' --exclude='.next' \
    --exclude='venv' --exclude='__pycache__' -czf acquireiq.tar.gz acquireiq/
scp acquireiq.tar.gz root@147.182.173.184:/tmp/

# 3. Extract and setup
ssh root@147.182.173.184 'cd /tmp && tar -xzf acquireiq.tar.gz && mv acquireiq /opt/'

# 4. Setup backend
ssh root@147.182.173.184 'cd /opt/acquireiq/backend && \
  python3 -m venv venv && source venv/bin/activate && \
  pip install -r requirements.txt'

# 5. Setup frontend
ssh root@147.182.173.184 'cd /opt/acquireiq/frontend && npm install && npm run build'

# 6. Start services
ssh root@147.182.173.184 'cd /opt/acquireiq/backend && \
  source venv/bin/activate && \
  uvicorn app.main:app --host 0.0.0.0 --port 8080 &'

ssh root@147.182.173.184 'cd /opt/acquireiq/frontend && npm start -- -p 3005 &'
```

### Access Production
- **Frontend**: http://147.182.173.184:3005
- **Backend API**: http://147.182.173.184:8080

---

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/api/search` | POST | Search companies by location/industry |
| `/api/companies` | GET | List enriched companies |
| `/api/companies/{id}` | GET | Company detail with scoring |
| `/api/outreach` | GET | Outreach queue & email drafts |

---

## 🔧 Key Technologies

### Frontend Stack
- Next.js 16.2.4 + React 19.2.4
- Tailwind CSS 4
- Framer Motion 12.38.0 (animations)
- TypeScript 5
- Lucide React (icons)

### Backend Stack
- FastAPI 0.115.0
- SQLAlchemy 2.0.35 async
- Pydantic 2.9.2
- Google Generative AI SDK
- Uvicorn 0.30.6

---

## 🤖 AI Model

**Current Model**: Gemini 2.5 Flash
- Used for: Acquisition readiness scoring, email subject/body generation
- Prompts: Located in `backend/app/services/ai/prompts.py`
- Configuration: `backend/app/services/ai/gemini_client.py`

---

## 📝 Environment Variables

```env
# Database
DATABASE_URL=sqlite+aiosqlite:///./acquireiq.db

# Google APIs
GOOGLE_PLACES_API_KEY=AIzaSy...
GEMINI_API_KEY=AIzaSy...

# Hunter.io
HUNTER_API_KEY=469f4c...

# Email (SMTP)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_FROM_NAME=AcquireIQ
```

---

## 🔐 Security Notes

- Store `.env` files locally; never commit to git
- Use app-specific passwords for Gmail SMTP
- Rotate API keys periodically
- Keep dependencies updated: `npm audit fix`, `pip install --upgrade`

---

## 📄 License

MIT License - See LICENSE file for details

---

## 👤 Author

**Abdullah Naeem**  
[GitHub](https://github.com/abd84) | [Email](mailto:your@email.com)

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

**Last Updated**: May 7, 2026  
**Status**: ✅ Production Ready
