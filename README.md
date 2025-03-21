# TODO List Application - Backend

This is the **backend** of a simple **TODO List Application**, built using **FastAPI**. It serves RESTful APIs for task management, including task creation, listing, updating, and deletion.

---

## ✨ Features

- 📄 **Task CRUD Operations** — Create, Read, Update, and Delete tasks
- ⚙️ **In-Memory Storage** — Uses simple in-memory storage (can be replaced with a database)
- 🗂️ **Modular Codebase** — Clear separation of concerns:
  - `models.py` — Data models (Pydantic schemas)
  - `routes.py` — API route definitions
  - `storage.py` — In-memory data storage logic
  - `utils.py` — Helper functions
  - `main.py` — Application entry point

---

## 🛠️ Tech Stack

- **Backend Framework:** FastAPI
- **Language:** Python 3.x
- **Dependencies:** Listed in `requirements.txt`

---



## 📂 Folder Structure
```
TODO-BACKEND/
├── app/
│   ├── __pycache__/           # Python cache files (auto-generated)
│   ├── main.py                # FastAPI app initialization and server entry point
│   ├── models.py              # Pydantic models (request/response schemas)
│   ├── routes.py              # API route definitions (CRUD endpoints)
│   ├── storage.py             # In-memory storage logic for tasks
│   ├── utils.py               # Utility/helper functions
├── .gitignore                 # Files and folders to ignore in git
├── README.md                  # Project documentation
├── requirements.txt           # Python dependencies list
```

## 🚀 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/CloudEvaTech/todo-backend.git
cd todo-backend
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```


### 4️⃣ Run the FastAPI Server
```bash
uvicorn app.main:app --reload
```

By default, the server runs at:

http://localhost:8000

You can explore and test the API at:

http://localhost:8000/docs — Swagger UI

