# Realtime Events Management App - README
### Project Overview
This is a real-time events management application where users can create events, join or leave events, and see updates in real time. The project consists of a React frontend and a FastAPI backend, with both services set up to run together using Docker Compose.

### Features
- Users can create events with details such as title, organizer, date, and location.
- Users can join or leave events, and the joiners list is updated in real-time for all users.
 - WebSocket-based real-time updates.
FastAPI for the backend and React for the frontend.
- Running the Project with Docker Compose
To simplify the process of running both the backend (FastAPI) and the frontend (React), the project is set up to use Docker Compose. This allows you to spin up both services simultaneously with a single command.

### Prerequisites
Make sure you have the following installed:

```bash 
Docker: Install Docker
Docker Compose: Install Docker Compose
```
#### Step-by-Step Instructions
- First, clone the project repository to your local machine:

```bash
Copy code
git clone <repository-url>
cd <repository-folder>
Build and Run the Services:
```

- Once you are inside the project folder, run the following command to build and run both the frontend and backend services:

```bash
docker-compose up --build
```
This command will:

- Build the Docker images for the React frontend and FastAPI backend.
Start both services in separate containers.
Access the Application:

### Frontend (React): Open your browser and navigate to:

```bash
http://localhost:3000
Backend (FastAPI): Access the backend API at:
http://localhost:8000
```
- API Documentation: FastAPI automatically generates documentation for its API. You can view the API documentation by visiting:

```bash 
Copy code
http://localhost:8000/docs
```
- Stopping the Application
To stop both the frontend and backend services, press CTRL + C in the terminal where Docker Compose is running, or use the following command in a new terminal window:

```bash

docker-compose down
This will stop and remove the containers but will leave the built images intact.
```

### Project Structure
Here’s an overview of the key directories and files in the project:

```bash 
.
├── backend/                  # FastAPI backend
│   ├── Dockerfile            # Dockerfile for backend
│   ├── main.py               # Main FastAPI application
│   ├── requirements.txt      # Backend dependencies
├── frontend/                 # React frontend
│   ├── Dockerfile            # Dockerfile for frontend
│   ├── src/                  # React application source files
├── docker-compose.yml        # Docker Compose configuration
```
### Key Files:
docker-compose.yml: This file defines how Docker Compose should set up and link the frontend and backend containers.
```bash 
version: '3'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    networks:
      - app-network

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

- backend/Dockerfile: The backend Dockerfile installs the necessary dependencies and runs the FastAPI server using uvicorn.

Dockerfile
```bash
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
frontend/Dockerfile: The frontend Dockerfile builds the React application and serves it.

# Dockerfile
```bash
# Use an official Node.js image as a parent image
FROM node:14

# Set the working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY package.json /app
RUN npm install

# Copy the current directory contents into the container
COPY . /app

# Expose port 3000
```bash
EXPOSE 3000
```

# Start the frontend application
```bash 
CMD ["npm", "start"]
Development Setup (Without Docker)
```
If you prefer running the project without Docker, follow these steps:


# Backend:

Navigate to the backend folder:
```bash
cd backend
Install dependencies:
bash
Copy code
pip install -r requirements.txt
Run the FastAPI server:
bash
Copy code
uvicorn main:app --reload
```

# Frontend:

Navigate to the frontend folder:
```bash
Copy code
cd frontend
Install dependencies:
npm install
Start the React development server:
bash
Copy code
npm start
```
# Next Steps
 - Database Integration: Future updates will include migrating from the in-memory database to a persistent database (e.g., SQLite or PostgreSQL).
- User Authentication: User authentication will be added to the app to enhance security and user experience.
