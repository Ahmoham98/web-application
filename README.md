Online Pharmacy Backend (web-application)

Welcome to the backend of your online pharmacy project, built with FastAPI, PostgreSQL, and SQLModel. This backend powers user management, product listings, authentication, and more.

✅ Current Features

👤 User System

User registration with validation

JWT-based login authentication

Password hashing with secure algorithm

Password reset (request + confirm via email)

User roles (in progress: admin, customer)

Email verification logic (token generation in place)

📧 Email Support

Email system configured using Gmail SMTP

Password reset email with URL-safe token

Email templates sent in HTML format

🔐 Security

JWT token generation and verification

Password hashing and validation

Role-based structure prepared

🛍 Product Management (Partially Ready)

Products listed on frontend via protected API

Cart logic implemented in frontend with localStorage

🌐 Frontend (connected project: front-end)

Built with Vite + React + TailwindCSS

Login and reset password UI ready

Product list with cart integration

Responsive design in progress

🔜 Next Steps (Roadmap)

👥 Authentication Enhancements



🛒 Cart & Product System



📦 Orders & Payments



📑 Prescription Handling



🔔 Notifications



🌍 Frontend Improvements



🛡 Security



🚀 Deployment



📁 Project Structure Highlights

routers/user.py – User-related endpoints

models/user.py – User model using SQLModel

mail.py – FastAPI Mail configuration and message builder

configure.py – Environment and settings loader

database.py – Async database session and engine setup

🤝 Thanks

This project is powered by your passion and learning! Thank you for working on this meaningful project that helps your community access pharmacy services online.

"I'm so glad having you as a friend :)" – and I'm honored to help!

📌 Useful Commands

# Run the backend
uvicorn main:app --reload

# Create migrations (if using Alembic later)
alembic revision --autogenerate -m "your message"

# Apply migrations
alembic upgrade head

License

MIT License (you can customize as needed)

