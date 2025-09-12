# Task Manager API 🚀

A simple Task Manager API built with **FastAPI**, **PostgreSQL**, and **Docker**.  
Supports user authentication (JWT) and task CRUD operations.  

## 📦 Setup & Installation

### Prerequisites
- Python 3.10+  
- SQLite (for quick local testing)  
- PostgreSQL (for production / Docker setup)  
- Docker & Docker Compose ( for containerized setup)  
- pip / virtualenv  
- Git  
- Postman (for API testing)  
- Visual Studio Code (recommended code editor)

### Local Setup
```bash
# Clone repository
git clone https://github.com/reshmabandi1028-rgb/task-manager-api
cd task-manager-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  

# Install dependencies
pip install -r requirements.txt

# Run locally with SQLite (tables auto-created on first run)
uvicorn app.main:app --reload

# Build and run with Docker
docker-compose up --build

# Check running containers
docker ps

🔗 API Endpoints
Auth
POST /signup → Register new user


POST /login → Login and receive JWT


Users
GET /me → Get current logged-in user


Tasks
POST /tasks → Create a new task


GET /tasks → List all tasks


GET /tasks/{id} → Get a single task


PUT /tasks/{id} → Update a task


DELETE /tasks/{id} → Delete a task


👉 Full interactive API docs available at:
Swagger UI → http://127.0.0.1:8000/docs


ReDoc → http://127.0.0.1:8000/redoc



 📸 Screenshots / Demo
Swagger UI running locally
[Swagger Screenshot](./Screenshots/SwaggerUI.png)
📬 Postman Collection
You can quickly test all APIs by importing the Postman collection:
Postman Request/Response:
  [Postman Collection](./postman/Task_Manager_API.postman_collection.json)


Download for quick import in Postman:
 [Download Postman Collection](./postman/Task_Manager_API.postman_collection.json)


📂 Project Structure
task-manager-api/
├── app
│   ├── __init__.py
│   ├── auth.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── routes.py
│   ├── schemas.py
│   └── tasks.py
├── Dockerfile
├── postman
│   └── Task_Manager_API.postman_collection.json
├── README.md
├── requirements.txt
├── Screenshots
├── start.sh
├── tests
│   ├── __init__.py
│   ├── test_auth.py
│   └── test_tasks.py

🌍 Deployment
Deployed on Render
🚀 Future Improvements
Add task categories/labels


Role-based access (admin/user)


Unit + integration tests coverage


CI/CD pipeline setup


Add Alembic migrations for database versioning
📝 License
MIT License – feel free to use this project for learning or building your own ideas.





  
