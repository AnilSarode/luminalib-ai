
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

### 4️⃣ Setup PostgreSQL

Create database and tables (see SQL schema in project).

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
