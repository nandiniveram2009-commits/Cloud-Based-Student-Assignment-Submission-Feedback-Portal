
# Cloud-Based Student Assignment Submission & Feedback Portal



## Overview 

The Cloud-Based Student Assignment Submission & Feedback Portal is an enterprise-grade, cloud-native web application designed to digitize, streamline, and secure the academic workflow of student homework submissions and instructor evaluations. By moving away from fragmented local files, chaotic email threads, and physical paperwork, this portal establishes a reliable single source of truth for educational institutions, online learning platforms, and corporate training programs.

## Problem statement 

Traditional academic assignment management suffers from severe operational inefficiencies:


-Paper & Email Chaos: Physical papers get lost or damaged, while email submissions cause version confusion, missing attachments, and cluttered instructor inboxes.

-Opacity & Delayed Feedback: Students lack real-time visibility into whether their assignments were received successfully or when grades will be posted.

-Scattered Evaluation Trails: Verbal or margin-written comments are easily lost, preventing long-term tracking of student academic progress.

-This portal solves these friction points by providing a centralized, secure, cloud-hosted platform that automates submission timestamps, version control, and real-time feedback.
##  Objectives 

-Centralized Repository: Archive all course assignments, student submissions, and grading metadata in a secure cloud database.

-Seamless Object Storage: Decouple binary attachments (PDF, DOCX, ZIP) from database storage by utilizing scalable cloud object storage buckets.

-Automated Workflow Processing: Automatically calculate version history, flag late submissions via server-side time comparison, and aggregate daily analytics.

-Role-Based Security: Enforce strict perimeter defense, ensuring students, teachers, and administrators access only authorized resources.

-AI-Powered Evaluation: Provide instructors with baseline auto-grading suggestions and plagiarism similarity detection.
## Features

-Secure User Authentication (Email/Password with JWT / Firebase Auth)

-Role-Based Access Control (Student, Teacher, Admin dashboards)

-Dynamic Assignment Creation & Deadline Enforcement

-Multi-format File Uploads (PDF, DOCX, PNG, JPEG up to 20MB)

-Automated Version Numbering & Late Submission Flagging

-Real-time Grading & Written Feedback Threads

-AI-Driven Plagiarism Similarity Score & Auto-Grade Suggestions

-Scheduled Daily Course Analytics
## User Roles 

          
Permissions & Capabilities
STUDENT	  

• Register and login securely<br>• View assigned coursework and strict deadlines<br>• Upload and resubmit assignment files<br>• Track submission statuses (SUBMITTED, LATE, GRADED)<br>• View numerical marks and instructor feedback

TEACHER

	• Create, update, and delete coursework assignments<br>• Set deadlines and maximum marks<br>• View, filter, and download student submissions<br>• Assign numerical scores and written critiques<br>• Monitor course submission statistics

ADMIN	

• Manage user accounts and role assignments<br>• Provision courses and assign faculty<br>• Monitor system-wide logs and database integrity

## Cloud computing concepts 

-Cloud Computing: Delivering compute, storage, and networking over the internet on-demand.

-SaaS (Software as a Service): Providing the portal entirely through web browsers without local software installation.

-PaaS (Platform as a Service): Deploying containerized FastAPI and Flask services to managed cloud runtimes.

-Cloud Database: Storing relational user profiles, course definitions, and submission metadata in managed PostgreSQL/Firestore.

-Object Storage: Storing unstructured binary documents in scalable S3-compatible buckets.

-Authentication & Authorization: Verifying identity via tokens and enforcing Role-Based Access Control (RBAC).
Serverless Computing: Executing background logic (versioning, late flagging, analytics) via Cloud Functions.

-Scalability & Elasticity: Dynamic scaling of database pools and storage buckets to absorb submission traffic spikes.

-CDN (Content Delivery Network): Serving static frontend assets globally with low latency.

-CI/CD & Deployment: Automated build and deployment pipelines connecting GitHub to cloud hosting

## Architecture 

[Students / Teachers]
         │ (HTTPS / TLS 1.3)
         ▼
[CDN / Frontend Hosting (React SPA)]
         │
         ▼
[API Gateway / Backend Router (FastAPI / Flask)]
    ┌────┴────────────────────────┬────────────────────────┐
    ▼                             ▼                        ▼
[Cloud Database]        [Cloud Object Storage]    [AI/ML Microservice]
(PostgreSQL / Firestore)  (S3 / Firebase Storage)   (Flask + Sentence-BERT)
## Technology stack

-Frontend: React, Vite, Tailwind CSS, React Router DOM, Axios

-Backend: Python FastAPI / Flask, Uvicorn, Pydantic

-Cloud Infrastructure: Firebase (Auth, Firestore, Storage, Cloud Functions) / Supabase / AWS S3

-AI / ML Microservice: Python, Flask, Hugging Face sentence-transformers, scikit-learn, joblib

-Testing & DevOps: Jest, Cypress, Docker, Gunicorn, Git / GitHub Actions

## Database Design 

-Users Table: user_id (PK), name, email, password_hash, role, created_at

-Courses Table: course_id (PK), course_name, teacher_id (FK), created_at

-Assignments Table: assignment_id (PK), course_id (FK), title, description, deadline, max_marks, created_by (FK), created_at

-Submissions Table: submission_id (PK), assignment_id (FK), student_id (FK), file_name, file_url, storage_path, submitted_at, submission_status, marks, feedback, graded_at
## Cloud storage 

-Database vs. Object Storage: Relational databases store structured metadata and timestamps, whereas cloud object storage buckets store unstructured binary assets (.pdf, .docx, .zip).

-File Path Convention:
assignments/{course_id}/{assignment_id}/{student_id}-{timestamp}-{filename} prevents naming collisions.

-Security: Private bucket rules require authenticated tokens and generate time-limited pre-signed URLs for downloads.


## Authentication & Authorization 

-Authentication: Validates user credentials and issues cryptographically signed JSON Web Tokens (JWT).

-Authorization: Intercepts API requests to inspect the role payload claim, preventing students from accessing teacher grading endpoints or peer submissions.

## Assignment workflow 

-Teacher authenticates and submits assignment parameters (title, description, course, deadline, max marks).

-Backend validates input via Pydantic schemas and saves record to the cloud database.

-Assignments instantly become visible on all enrolled student dashboards.
## Submission workflow 

-Student selects an active assignment and attaches a valid document (< 20MB).

-Frontend validates file mime type and size.

-File streams into Cloud Object Storage, returning a unique file reference URL.

-Submission metadata is saved to the cloud database, triggering server-side Cloud Functions to verify version numbers and late submission statuses.

## Feedback & Grading

-Teacher reviews submitted files via secure download links.
-Teacher enters numerical marks (validated against max allowed) and textual feedback.
-Database record updates status to GRADED and timestamps the evaluation.
-Student dashboard reflects grades and instructor comments immediately.
## Rest APIs

 -POST /api/register – Register new user account
-POST /api/login – Authenticate user and issue JWT
-POST /api/assignments – Create new assignment (Teacher only)
-GET /api/assignments – Retrieve all course assignments
-POST /api/assignments/{id}/submit – Upload student submission file
-GET /api/submissions/me – Retrieve authenticated student's submissions
-GET /api/assignments/{id}/submissions – View assignment submissions (Teacher only)
-POST /api/submissions/{id}/grade – Grade submission and provide feedback (Teacher only)
-GET /api/submissions/{id}/download – Download secure submission file asset
## Folder structure 

Cloud-Hobby-Skills-Tracker/
├── backend/
│   ├── requirements.txt
│   ├── app.py
│   ├── cloud_db.py
│   ├── database_models.py
│   ├── auth_service.py
│   ├── auth_routs.py
│   └── assignment_routs.py
│   └── submission_routs.py
│   
├── Frontend/   
│   ├── package.json
│   ├── src/app.jsx
│   ├── src/services/api.js
│   ├── scr/pages/login.jsx
│   ├──src/pages/Register.jsx
│   ├── src/pages/studentDashboad.jsx
│   └── src/pages/TeacherDashboard.jsx
│   
├── .env.example
├── .gitignore
└── README.md
## Installation 

Ensure Python (3.10+), Node.js (18+), and Git are installed on your machine.

## Environment variable 


## Local setup

## Running the application 
## Testing 

Run Unit Tests: npm test or pytest
Run End-to-End Tests: npx cypress open

## Cloud development 

-Frontend: Deployed globally via Vercel / Netlify edge networks.
-Backend: Containerized and deployed to Render, Railway, or Google Cloud Run.
-Database & Storage: Managed PostgreSQL and S3 Object Storage buckets via Supabase or AWS.

## Security 

-TLS 1.3 encryption in transit and AES-256 encryption at rest.
-Strict Role-Based Access Control (RBAC) preventing unauthorized endpoint access.
-File-type whitelisting and size restrictions preventing malicious uploads.
-Secure environment secret management preventing hardcoded credentials.



## Scalability 

-Designed for horizontal scaling using load balancers and container orchestration (ECS / Kubernetes).
-Cloud object storage and managed database connection pooling effortlessly handle massive traffic spikes near submission deadlines.
## Failure handeling 

-Exponential backoff retry logic for network drops during multipart file uploads.
-Circuit breaker patterns and graceful 503 error responses during temporary cloud storage outages.
-Idempotent API designs preventing duplicate submission records.

## Results

Successfully implemented a fully functional cloud education portal demonstrating secure authentication, role isolation, real-time cloud database synchronization, and scalable object storage file management.

## Limitations 

-Free-tier cloud database connection limits under high concurrent loads.
-Local storage simulation fallback requires external cloud bucket configuration for multi-region production scale.
## Future improvement 

-Integration of automated plagiarism scanning against an institutional document corpus.
-Real-time WebSockets for instant push notifications when grades are published.
-Mobile application client built with Flutter or React Native.

## Learning outcomes 

-Mastery of full-stack cloud architecture and decoupled client-server communication.
-Practical experience with cloud authentication, database design, and object storage lifecycles.
-Proficiency in containerization, deployment pipelines, and cloud security best practices.


## Author

* **GitHub:** [nandiniveram2009](https://github.com)
* **LinkedIn:** [Nandini Verma](https://linkedin.com)



## Scalability 

-Designed for horizontal scaling using load balancers and container orchestration (ECS / Kubernetes).
-Cloud object storage and managed database connection pooling effortlessly handle massive traffic spikes near submission deadlines.
## Rest APIs

 -POST /api/register – Register new user account
-POST /api/login – Authenticate user and issue JWT
-POST /api/assignments – Create new assignment (Teacher only)
-GET /api/assignments – Retrieve all course assignments
-POST /api/assignments/{id}/submit – Upload student submission file
-GET /api/submissions/me – Retrieve authenticated student's submissions
-GET /api/assignments/{id}/submissions – View assignment submissions (Teacher only)
-POST /api/submissions/{id}/grade – Grade submission and provide feedback (Teacher only)
-GET /api/submissions/{id}/download – Download secure submission file asset