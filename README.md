🚀 DreamProject Platform

An AI-Powered Career, Simulation & Guidance Ecosystem

📌 Overview

DreamProject Platform is a full-stack, modular web application designed to help users explore careers, build projects, simulate real-world experiences, and connect with expert guides — all in one place.

The platform is built with strict feature isolation, ensuring scalability, maintainability, and future mobile app integration without backend rewrites.

🎯 Core Objectives

Help users discover suitable careers

Enable AI-assisted project planning

Provide real-world simulation experiences

Connect learners with verified professional guides

Maintain clean separation of concerns between features

🧩 Key Features
👤 User Roles

Learner / Career Explorer

Professional Guide

Admin (Future Scope)

🧭 Career Module

Designed for users confused about their career path.

Features:

Career onboarding (New Learner / Professional)

AI-based career suggestion via question flow

Career roadmap generation

Guide discovery by domain

Guide messaging & feedback

Career-specific dashboard

⚠️ Simulation is intentionally excluded from this module for clarity and modularity.

🧠 MyDreamProject (AI-Powered Project Builder)

A unique feature where users describe their dream project and get a structured execution plan.

Capabilities:

Project idea description input

Optional image upload

AI-generated step-by-step project breakdown

Required tools & tech stack suggestions

Learning resources & guides mapping

Built-in discussion & comments

Direct “Contact Guide” option

🎮 Simulation Module (Dedicated & Isolated)

A standalone feature for immersive, real-world role simulations.

Highlights:

Real-life role simulation (e.g., CEO, Engineer, Analyst)

Time-compressed experience (24 hours → 10–12 hours)

AI-controlled environment & decision paths

Safe sandbox execution

Error-handled backend execution

Independent routing & UI access

✔ Completely isolated from Career module
✔ No shared dependency conflicts

🧑‍🏫 Guide System

A professional verification and mentorship layer.

Guide Features:

Separate guide signup flow

Field/domain selection

Document upload for experience verification

Guide dashboard

User chat & problem-solving

Feedback & rating system

🔐 Authentication & Authorization

Secure login & signup

Role-based access control

Separate schemas for learners and guides

Protected routes

🖥️ Frontend Architecture

Modular UI components

Feature-level routing

Conditional rendering

Clean navigation separation

Responsive & scalable design

⚙️ Backend Architecture

REST-based API design

Isolated feature endpoints

Robust error handling

Logging for debugging

CORS-safe frontend/backend communication

🏗️ Tech Stack

Frontend

HTML / CSS / JavaScript

React (planned / integrated)

Tailwind CSS (UI enhancement)

Backend

FastAPI / Node.js (depending on implementation)

REST APIs

Modular routers

AI / ML

Ollama (Free & local AI inference)

Prompt-driven intelligence

No paid APIs dependency

Database

SQL-based (schema-separated)

User & guide isolation

🧪 Reliability & Safety

Feature-level isolation

No shared mutation across modules

Regression-safe updates

Graceful error handling

Backward compatibility maintained

📂 Project Structure (High Level)
/frontend
  ├── career/
  ├── simulation/
  ├── myDreamProject/
  ├── auth/
  └── shared/

/backend
  ├── auth/
  ├── career/
  ├── simulation/
  ├── guides/
  └── core/

🚀 Future Enhancements

Mobile App (Android / iOS) using same APIs

Admin analytics dashboard

AR-based simulation

Resume & portfolio auto-generation

Blockchain-based credential verification

🤝 Contribution Guidelines

Do not modify unrelated features

Follow feature isolation rules

Add proper error handling

Maintain backward compatibility

📄 License

This project is licensed for educational and demonstration purposes.

✨ Final Note

This project is designed with real-world scalability, clean architecture, and AI-first thinking.
Every feature is modular, future-proof, and safe for expansion.
