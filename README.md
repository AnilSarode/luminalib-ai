
# LuminaLib AI

AI-powered library backend system with:

* 📚 Book upload (PDF)
* 🤖 LLM-based summarization (Ollama)
* 🧠 Embedding generation
* 😊 Sentiment analysis
* 🎯 Embedding-based recommendation engine
* 🏗 Clean Architecture design

---

## 🚀 Tech Stack

* Python 3.10+
* Flask
* PostgreSQL
* Ollama (local LLM)
* NumPy (cosine similarity)

---

## 🏗 Project Structure

```
luminalib/
│
├── api/
│   ├── books.py
│   ├── borrowings.py
│   ├── reviews.py
│
├── application/
│   └── usecases/
│       ├── add_book.py
│       ├── borrow_book.py
│       ├── add_review.py
│       ├── recommend_books.py
│       ├── summarize_book.py
│
├── domain/
│   └── services/
│       ├── recommendation_engine.py
│
├── infrastructure/
│   ├── db/
│   │   ├── connection.py
│   │   └── repositories/
│   │       ├── book_repo.py
│   │       ├── borrowing_repo.py
│   │       ├── review_repo.py
│   │
│   ├── ai/
│   │   ├── llm_base.py
│   │   ├── summary_service.py
│   │   ├── sentiment_service.py
│   │   ├── embedding_service.py
│   │   ├── pdf_reader.py
│
├── uploaded_books/
├── main.py
├── requirements.txt
```

---

## 🧠 How Recommendation Works

1. Generate summary from PDF using Ollama
2. Generate embedding from summary
3. Store embedding in PostgreSQL (JSONB)
4. Build user profile embedding (average of liked books)
5. Compute cosine similarity
6. Return top recommended books

---

## ⚙️ Setup Instructions

### 1️⃣ Clone

```
git clone <repo-url>
cd luminalib
```

---

### 2️⃣ Create Virtual Environment

```
python3 -m venv luminalib_venv
source luminalib_venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

---

### 4️⃣ Setup PostgreSQL Using Docker

This project uses PostgreSQL as the database.

The easiest way to run PostgreSQL is using Docker.

Your Flask app will run locally (outside Docker).
Only PostgreSQL will run inside a container.

4.1 Create docker-compose.yml

Create a file named:

docker-compose.yml

at the project root (luminalib/) and add the following content:

version: "3.9"

services:
  postgres:
    image: postgres:15
    container_name: luminalib_postgres
    restart: always
    environment:
      POSTGRES_USER: luminalib
      POSTGRES_PASSWORD: luminalib
      POSTGRES_DB: luminalib_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
4.2 Start PostgreSQL

From your project root:

docker-compose up -d

You should see something like:

Creating luminalib_postgres ... done
4.3 Verify PostgreSQL Is Running
4.3.1 Check Running Containers
docker ps

You should see:

luminalib_postgres
4.3.2 Connect to PostgreSQL (Recommended)
docker exec -it luminalib_postgres psql -U luminalib -d luminalib_db

If successful, you should see:

luminalib_db=#

To exit:

\q
4.4 Create Required Tables

After connecting to the database, run the following SQL:

CREATE TABLE books (
    id UUID PRIMARY KEY,
    title TEXT,
    author TEXT,
    category TEXT,
    description TEXT,
    file_path TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    summary TEXT,
    embedding JSONB
);

CREATE TABLE borrowings (
    id SERIAL PRIMARY KEY,
    book_id UUID REFERENCES books(id),
    user_id INT,
    borrowed_at TIMESTAMP,
    returned_at TIMESTAMP
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    book_id UUID REFERENCES books(id),
    user_id INT,
    text TEXT,
    sentiment TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

4.5 Stop PostgreSQL

To stop the container:

docker-compose down

To stop and remove all database data:

docker-compose down -v
---

### 5️⃣ Install Ollama

```
ollama pull mistral
```

---

### 6️⃣ Run Server

```
python main.py
```

Server runs at:

```
http://127.0.0.1:5000
```

---

## 🧪 Example API Calls

### Upload Book

```
curl -X POST http://127.0.0.1:5000/books \
  -F "title=Deep Learning" \
  -F "author=Author" \
  -F "category=ML" \
  -F "description=Guide" \
  -F 'file=@/path/to/book.pdf'
```

---

### Borrow Book

```
curl -X POST http://127.0.0.1:5000/books/<BOOK_ID>/borrow
```

---

### Add Review

```
curl -X POST http://127.0.0.1:5000/books/<BOOK_ID>/reviews \
  -H "Content-Type: application/json" \
  -d '{"text":"Excellent book."}'
```

---

### Get Recommendations

```
curl http://127.0.0.1:5000/users/1/recommendations
```

---

## 📌 Highlights

* Local LLM integration
* Semantic recommendation engine
* Clean architecture separation
* No external API dependency
* Fully self-hosted AI pipeline

---
