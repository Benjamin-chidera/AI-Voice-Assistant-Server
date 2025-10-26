# 🗣️ Echo Voice Assistant API

<!-- ![Python Version](https://img.shields.io/badge/python-3.9%2B-blue) -->

![FastAPI](https://img.shields.io/badge/FastAPI-005571?logo=fastapi)
![Last Commit](https://img.shields.io/github/last-commit/Benjamin-chidera/AI-Voice-Assistant-Server)
![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)
![PRs](https://img.shields.io/badge/PRs-welcome-blue.svg)

A **FastAPI-based backend** for the **Echo Voice Assistant**, providing **user authentication**, **AI-powered chat**, and **customization** features — including voice and audio transcription support.

---

## 🚀 Features

- 🔐 **User Authentication** — Secure registration, login, and profile management with JWT.
- 💬 **AI Chat** — Communicate naturally with an AI assistant using text or voice.
- 🎨 **Customization** — Personalize your assistant’s voice, language, and settings.
- 🎧 **Audio Transcription** — Upload and transcribe audio files for AI interaction.
- ☁️ **Cloud Integration** — Store assets with Cloudinary and vector data with Pinecone.

---

## 🧱 Project Structure

```text
.
├──                          # Entry point of the application
├──                      # Database configuration and connection
├──                        # SQLAlchemy models for the database
├── router/                         # API route modules
│   ├── auth.py                     # User authentication routes
│   ├── chat.py                     # Chat-related routes
│   └── customization.py            # Customization-related routes
├──                        # Pydantic models for request/response validation
├── utils/                          # Utility modules
│   ├── access_token.py             # JWT token generation and validation
│   ├── get_current_user.py         # User authentication helpers
│   └── llm_communication.py        # AI communication logic
├──                  # Python dependencies
├──                        # Project documentation
└── .env                            # Environment variables (not included in version control)

## ⚙️ Prerequisites

Before running the project, make sure you have:

- 🐍 **Python 3.9+**
- 🛢️ **MySQL database**
- 🧠 **Pinecone** account for vector storage → [https://www.pinecone.io/](https://www.pinecone.io/)
- ☁️ **Cloudinary** account for media uploads → [https://cloudinary.com/](https://cloudinary.com/)

---

## 🧩 Installation Guide

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Benjamin-chidera/AI-Voice-Assistant-Server.git
cd AI-Voice-Assistant-Server

python -m venv venv
source venv/bin/activate      # On macOS/Linux
# OR
venv\Scripts\activate         # On Windows

pip install -r requirement.txt

SECRET_KEY=your_secret_key

# Pinecone configuration
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=your_pinecone_index_name

# Cloudinary configuration
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://username:password@localhost/echo_db"

uvicorn main:app --host 0.0.0.0 --port 8000 --reload

| Method  | Endpoint          | Description             |
| ------- | ----------------- | ----------------------- |
| `POST`  | `/auth/register`  | Register a new user     |
| `POST`  | `/auth/login`     | Log in an existing user |
| `GET`   | `/auth/user/{id}` | Retrieve user details   |
| `PATCH` | `/auth/user/{id}` | Update user information |


| Method | Endpoint             | Description                               |
| ------ | -------------------- | ----------------------------------------- |
| `POST` | `/chat/communicate`  | Transcribe audio and interact with the AI |
| `POST` | `/chat/chat_with_ai` | Send a text message to the AI             |

| Category           | Technology                |
| ------------------ | ------------------------- |
| **Framework**      | FastAPI                   |
| **Database**       | MySQL + SQLAlchemy ORM    |
| **Authentication** | JWT (JSON Web Token)      |
| **AI Integration** | LangChain, OpenAI, Ollama |
| **Cloud Storage**  | Cloudinary                |
| **Vector Storage** | Pinecone                  |

.env

📬 Contact
For questions, issues, or contributions:
Email: benjaminchidera72@gmail.com
GitHub: @Benjamin-chidera
```
