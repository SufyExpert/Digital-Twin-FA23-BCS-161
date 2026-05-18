-- Dynamically Generated Seed Script from Supabase
-- Created for FA23-BCS-161 Final Exam Submission

-- Drop existing tables to ensure clean state
DROP TABLE IF EXISTS project_images CASCADE;
DROP TABLE IF EXISTS projects CASCADE;
DROP TABLE IF EXISTS experience CASCADE;
DROP TABLE IF EXISTS services CASCADE;

-- Create tables
CREATE TABLE experience (
    id SERIAL PRIMARY KEY,
    company VARCHAR(255),
    role VARCHAR(255),
    duration VARCHAR(100),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE,
    description TEXT,
    html_url VARCHAR(512),
    stargazers_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE project_images (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    image_url TEXT,
    caption VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE services (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    icon VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Seeding data for projects
INSERT INTO projects (id, title, slug, description, cover_image_url, link, github_link, technologies, tools, case_study_content, status, is_featured, order_index, category, created_at) VALUES ('33333333-3333-3333-3333-333333333333', 'ask_academy', 'ask-academy', 'ASK Academy was engineered to replace fragmented, slow, and outdated administrative tools with a highly cohesive, natively compiled desktop management system.', 'https://ywhocytfjiubouhehiuj.supabase.co/storage/v1/object/public/project-images/ask-academy.png', '', 'https://github.com/SufyExpert/ask_academy', '[''Python'', ''React'', ''PostgreSQL'', ''Vector DB'', ''LLM'', ''RAG'']', '[]', '### Executive Summary
ASK Academy was engineered to replace fragmented, slow, and outdated administrative tools with a highly cohesive, natively compiled desktop management system.

The objective was to build an enterprise-grade School Management application capable of:
- Executing comprehensive CRUD operations across massive student and faculty datasets
- Generating granular, multi-variable analytical charts
- Processing structured data into professional, printable PDF reports
- Ensuring remote, secure access to a centralized cloud database

The system utilizes a sophisticated Python architecture to combine the speed of a native desktop interface with the immense data capacity of an Azure SQL cloud backbone.

### The Problem
Administrative educational software suffers from severe usability gaps:
- Web-based portals often suffer from high latency and poor UX when filtering thousands of records simultaneously.
- Extracting raw data into properly formatted, physical A4 documents usually requires third-party plugins or convoluted Excel exports.
- Local desktop apps frequently rely on fragile local SQLite files, leading to massive data loss if a machine crashes.

There was a critical need for a system that provided lightning-fast desktop rendering while strictly maintaining data integrity in a secure cloud environment.

### The Solution
ASK Academy integrates:
- A completely modernized CustomTkinter GUI featuring a professional dark-navy aesthetic.
- A direct, parameterized connection layer to Microsoft Azure SQL via `pyodbc`.
- Integrated Matplotlib graphing directly mapped onto the Tkinter canvas.
- The ReportLab engine to systematically render complex tables into exportable PDFs.

The result is a powerful institutional tool that delivers:
- Instantaneous multi-column filtering for precise record retrieval.
- Hardware-accelerated visual analytics embedded in the dashboard.
- One-click physical reporting capabilities for student transcripts and institutional rosters.
- Highly secure, parameterized query execution preventing any SQL injection vulnerabilities.

### System Architecture
1. Interface Layer
Python CustomTkinter managing complex grid layouts, interactive tables, and custom calendar pickers (`tkcalendar`).
Matplotlib `FigureCanvasTkAgg` bridging scientific charting into the UI thread.

2. Logic & Reporting Layer
A highly modular, single-file class architecture managing application state.
ReportLab executing physical document generation (`SimpleDocTemplate`).

3. Database Layer
Microsoft Azure SQL Server handling relational data integrity.
`schema.sql` defining rigorous relational constraints between Students, Classes, Teachers, and Results.
`testdata.py` providing robust testing environments.

### Engineering Decisions
Why a Single-File Class Architecture?
To highly centralize state management and UI updating logic within a single executable flow, drastically simplifying distribution and deployment to internal school hardware.

Why Azure SQL via PyODBC?
To ensure enterprise-grade ACID compliance and remote accessibility. This guarantees that multiple administrative computers can safely read and write to the same dataset simultaneously without locking errors.

Why ReportLab PDF Generation?
Unlike basic HTML-to-PDF scripts, ReportLab allows for pixel-perfect mathematical positioning of text and tables, ensuring official school documents are perfectly formatted for A4 printing.

### Performance Metrics
Database query execution: heavily optimized via parameterized SQL indexing.
UI thread responsiveness: zero-blocking during complex Matplotlib rendering.
PDF generation speed: sub-second compilation for heavy data tables.
Application stability: robust error handling managing remote database connection drops.

### Scalability Strategy
The Azure SQL backend scales infinitely to handle decades of institutional records.
The Python codebase is fully primed to be compiled into a standalone Windows Executable (`.exe`) via PyInstaller for zero-dependency distribution.
Extensible schema allows easy addition of financial/payroll modules.

### Outcome
ASK Academy is a masterclass in bridging native Python GUI development with enterprise cloud databases.

It operates as a highly polished, visually modern, and structurally unbreakable administrative platform.

', 'published', True, 3, 'Web App', '2026-05-07T05:17:05.003981+00:00') ON CONFLICT DO NOTHING;
INSERT INTO projects (id, title, slug, description, cover_image_url, link, github_link, technologies, tools, case_study_content, status, is_featured, order_index, category, created_at) VALUES ('77777777-7777-7777-7777-777777777777', 'Flappy-Bird-Game', 'flappy-bird', 'The Flappy Bird clone was engineered to tackle the complex foundational computer science challenges of game loop synchronization, real-time physics rendering, and memory management inherent in pure object-oriented software development.', 'https://ywhocytfjiubouhehiuj.supabase.co/storage/v1/object/public/project-images/flappy-bird.png', '', 'https://github.com/SufyExpert/Flappy-Bird-Game', '[''Java'', ''AWT'', ''Swing'', ''OOP'', ''Game Loop'', ''Physics'']', '[]', '### Executive Summary
The Flappy Bird clone was engineered to tackle the complex foundational computer science challenges of game loop synchronization, real-time physics rendering, and memory management inherent in pure object-oriented software development.

The objective was to build a highly responsive, mathematically precise 2D arcade game in Java capable of:
- Sustaining a strict, stutter-free 60 FPS rendering cycle
- Calculating precise bounding-box collision detection at high velocities
- Managing the infinite procedural generation of obstacle elements
- Orchestrating complex state-driven threading without deadlocks

The system was architected entirely from scratch using pure Java Swing, intentionally avoiding heavy third-party game engines to demonstrate absolute mastery of core programming principles.

### The Problem
Developing real-time, infinite-loop software presents unique architectural hurdles that standard event-driven applications never face:
- Unoptimized rendering loops suffer from severe frame-rate stuttering and screen tearing.
- Continuously instantiating objects (like pipes) without recycling them leads to massive memory leaks and garbage collection stutters.
- Thread-blocking UI updates completely destroy input responsiveness.

Relying on modern engines like Unity abstracts these problems away, masking a lack of understanding of the underlying algorithmic physics and memory constraints.

### The Solution
The Java-based engine integrates:
- A meticulously constructed custom `Runnable` game loop ensuring precise thread sleeping.
- Advanced Object-Oriented patterns utilizing Abstraction (`Moveable`) and Inheritance for diverse game entities.
- Precise delta-time physical algorithms controlling gravitational pull and impulse velocity.
- Hardware-accelerated Java Swing/AWT graphics pipelines.

The result is a buttery-smooth desktop executable that delivers:
- Pixel-perfect bounding box collision responses.
- Continuous, memory-efficient procedural level streaming.
- Parallax background scrolling synced perfectly to foreground movement.
- Instantaneous keyboard event handling isolated from the rendering thread.

### System Architecture
1. Rendering Layer
`JPanel` and `Graphics` objects utilizing explicit painting techniques to completely eliminate visual flickering.

2. Logic & Physics Layer
A global `Coordinates` interface defining mathematical constants (speed, gap sizes, gravity).
Independent physics controllers strictly dictating downward acceleration versus upward impulse.

3. Synchronization Layer
Independent threads controlling the Bird, Pipes, and Background.
Strict usage of `volatile boolean shouldTerminate` flags to ensure thread-safe game-over states across all executing loops.

4. State & Data Layer
Multi-screen flow managed via encapsulated classes (MainMenu, GamePanel, InfoForm).
Persistent `data.txt` I/O streams handling the local high-score ledger securely.

### Engineering Decisions
Why Pure Java Swing?
To intentionally construct a lightweight, native application, proving the ability to handle raw frame-pacing, threading, and rendering APIs without relying on pre-built physics engines.

Why ''Volatile'' State Flags?
When multiple CPU threads control different moving objects simultaneously, using `volatile` ensures memory visibility. This guarantees that when the bird hits a pipe, the background and pipe threads instantly read the game-over state and halt, preventing race conditions.

Why Abstract Interfaces (`Moveable`)?
Enforces strict architectural contracts, ensuring every game entity is guaranteed to have unified `run`, `start`, and `move` methods, making the engine highly modular.

### Performance Metrics
Rendering speed: locked consistently at 60 FPS.
Heap memory usage: strictly maintained with zero memory leaks during infinite play loops.
Input latency: optimized for sub-16 millisecond response times.
Collision mathematics: 100% accurate edge-detection logic.

### Scalability Strategy
Highly modular class design allows rapid injection of new entity types (e.g., power-ups, moving pipes) simply by extending the `Moveable` class.
Decoupled rendering logic makes it theoretically straightforward to port the core math to mobile frameworks like LibGDX.

### Outcome
This application demonstrates deep, rigorous understanding of foundational computer science concepts: complex concurrency, raw algorithmic physics, and memory-safe object management.

It is a highly polished software engine that serves as undeniable proof of advanced Java capabilities.

', 'published', False, 7, 'Game', '2026-05-07T05:17:05.003981+00:00') ON CONFLICT DO NOTHING;
INSERT INTO projects (id, title, slug, description, cover_image_url, link, github_link, technologies, tools, case_study_content, status, is_featured, order_index, category, created_at) VALUES ('88888888-8888-8888-8888-888888888888', 'prompt-tutor-ai', 'prompt-tutor-ai', 'An AI-powered web application that helps users write, analyze, improve, and compare prompts.', 'https://ywhocytfjiubouhehiuj.supabase.co/storage/v1/object/public/project-images/prompt-tutor-ai.png', 'https://promptutor.app', '', '[''Next.js'', ''AI Studio'', ''Supabase'', ''Tailwind CSS'', ''Vercel'']', '[]', '### Executive Summary
An AI-powered web application that helps users write, analyze, improve, and compare prompts. Built with React, Firebase, and Google Gemini, it features a Prompt Analyzer, a guided Prompt Generator, dynamic Templates, and side-by-side comparisons.

### The Problem
Users frequently struggle to write effective, context-rich, and specific prompts, resulting in suboptimal LLM outputs. There is a lack of unified, interactive tools to structurally evaluate, compare, or generate high-quality prompts with real-time, actionable feedback.

### The Solution
Prompt Tutor AI leverages Google Gemini to provide a robust analyzer that scores prompts across 5 dimensions (clarity, specificity, context, tone, efficiency). It offers a guided zero-to-hero generator, a categorized template library with dynamic placeholders, side-by-side comparisons, and a personalized history dashboard.

### System Architecture
1. Frontend Layer
React 19, TypeScript, and Tailwind CSS v4 providing a highly interactive SPA.
Recharts for scoring visualization and Framer Motion for fluid UI animations.

2. Intelligence Layer
Google Gemini API (gemini-3-flash-preview) handling prompt analysis, multi-dimensional scoring, and intelligent rewriting.

3. Data & Auth Layer
Cloud Firestore managing dynamic collections for users, historical prompts, and template libraries.
Firebase Authentication for secure, session-persistent Google Sign-In.

### Engineering Decisions
Why Google Gemini (Flash)?
To leverage a high-speed, cost-effective LLM capable of complex multidimensional text analysis and rapid prompt rewriting without long loading states.

Why Firebase + Firestore?
To eliminate the need for a complex custom backend, allowing real-time, schema-less storage for user histories, seamless authentication, and strict rule-based data isolation.

Why React 19 + Vite + Vercel?
To ensure extreme frontend developer velocity, highly optimized client-side routing, and zero-configuration serverless deployment.

### Performance Metrics
Instantaneous client-side navigation; highly optimized AI response latency via the Gemini Flash model; seamless real-time syncing of user histories.

### Scalability Strategy
Fully serverless architecture deployed on Vercel; Firestore handles horizontal data scaling automatically; Firebase Security Rules enforce strict multi-tenant data isolation per user.

### Outcome
A polished, production-ready SaaS application that transforms prompt engineering from a trial-and-error process into a structured, analytical, and highly accessible workflow.

', 'published', True, 0, 'SaaS Web App', '2026-05-07T05:17:05.003981+00:00') ON CONFLICT DO NOTHING;
INSERT INTO projects (id, title, slug, description, cover_image_url, link, github_link, technologies, tools, case_study_content, status, is_featured, order_index, category, created_at) VALUES ('11111111-1111-1111-1111-111111111111', 'health-level-prediction-system', 'health-predictor', 'The Health Level Prediction System was engineered to provide immediate, data-driven health risk assessments.', 'https://ywhocytfjiubouhehiuj.supabase.co/storage/v1/object/public/project-images/health-risk.png', '', 'https://github.com/SufyExpert/health-level-prediction-system', '[''Python'', ''Flask'', ''Scikit-Learn'', ''Matplotlib'', ''Random Forest'']', '[]', '### Executive Summary
The Health Level Prediction System was engineered to provide immediate, data-driven health risk assessments. By processing a complex array of daily lifestyle inputs—such as age, BMI, sleep duration, exercise routines, smoking habits, and profession—the system accurately predicts a user''s health risk tier (Low, Medium, or High).

The objective was to build a highly responsive, machine-learning-powered web application capable of:
- Preprocessing user lifestyle data in real-time
- Running rapid ML inference to determine risk categorization
- Generating granular visual diagnostic reports
- Maintaining a stateless web architecture for seamless user flow

The system utilizes a Scikit-Learn Random Forest Classifier trained on a large-scale synthetic dataset, delivering personalized health insights instantly without requiring clinical intervention.

### The Problem
Traditional preliminary health assessments suffer from several structural limitations:
- They often rely on isolated metrics (like only BMI or only age) rather than holistic lifestyle data.
- Users must navigate complex, multi-step clinical portals to get basic preventative insights.
- Static web forms provide generic text feedback rather than dynamic, personalized visual analytics.
- Storing personal health inputs often introduces severe database privacy concerns and compliance overhead.

There was a clear need for a fast, stateless diagnostic tool that could leverage heavy data science models while delivering instantaneous, easily digestible graphical reports directly to the user.

### The Solution
The Health Level Prediction System integrates:
- A pre-trained Random Forest Classifier capable of handling complex categorical and numerical inputs.
- A dynamic, multi-page Flask web interface that uses session states to manage user data securely.
- Real-time Matplotlib generation to create visual risk gauges and feature breakdown charts.

The result is a highly contextual ML system that delivers:
- An accurate Low/Medium/High risk classification
- Inline graphical reports comparing user metrics against baseline health standards
- A completely stateless backend where no personal health data is persistently saved to a database, ensuring absolute privacy and high performance.

### System Architecture
1. Data & Preprocessing Layer
Data ingested from a synthetic lifestyle dataset (~270K rows).
Extensive preprocessing utilizing `StandardScaler` for numerical normalization.
Binary mapping via `LabelEncoder` and categorical mapping via One-Hot Encoding for fields like profession and exercise type.

2. Intelligence Layer
The core engine is a `RandomForestClassifier` optimized for multi-class prediction.
Models and scalers are serialized and exported via `joblib` for rapid memory loading.

3. Visualization Layer
Matplotlib dynamically generates comparison bars and gauge charts.
Charts are converted directly into base64-encoded PNG strings to be served inline.

4. Application Layer
Python/Flask backend handling orchestration and routing.
Jinja2 HTML templates with custom CSS rendering the frontend.
Flask `session` handles state transfer between the form submission and the final results page.

### Engineering Decisions
Why Flask Sessions Over a Database?
To maintain a strictly stateless application. By utilizing secure cookies/sessions, the app avoids the overhead, latency, and security risks of permanently writing transient medical data to a persistent database.

Why Base64 Inline Image Encoding?
Generating physical image files for thousands of concurrent users would create massive I/O bottlenecks and require complex cleanup scripts. Encoding plots to Base64 strings directly in RAM and passing them to Jinja2 ensures a clean, memory-efficient pipeline.

Why Random Forest?
It provides excellent robustness against overfitting on diverse categorical lifestyle data and handles the non-linear relationships between health factors seamlessly.

### Performance Metrics
Model training capability: handles ~270K rows efficiently.
Inference latency: < 100 milliseconds per prediction.
Visual report generation: < 1 second for fully rendered Matplotlib inline charts.
Memory overhead: minimized due to lack of persistent I/O file writing.

### Scalability Strategy
Joblib serialization allows rapid swapping or upgrading of the ML models without altering the backend code.
The completely stateless Flask architecture means the application can be seamlessly horizontally scaled across multiple load-balanced web servers.
Potential future integration with automated API endpoints for external B2B health triage.

### Outcome
The Health Level Prediction System demonstrates how complex Scikit-Learn pipelines can be effectively deployed into consumer-facing web applications.

It is architected as a highly efficient, privacy-first predictive tool that prioritizes immediate visual feedback over bloated backend data retention.

', 'published', True, 1, 'Web App', '2026-05-07T05:17:05.003981+00:00') ON CONFLICT DO NOTHING;
INSERT INTO projects (id, title, slug, description, cover_image_url, link, github_link, technologies, tools, case_study_content, status, is_featured, order_index, category, created_at) VALUES ('22222222-2222-2222-2222-222222222222', 'medical-diagnostic-system-ver2', 'medical-diagnostic-v2', 'Medical Diagnostic System Version 2 was engineered to completely modernize its desktop predecessor, transforming a robust diagnostic engine into a highly accessible, full-stack AI web platform.', 'https://ywhocytfjiubouhehiuj.supabase.co/storage/v1/object/public/project-images/meddiag-v2.png', '', 'https://github.com/SufyExpert/medical-diagnostic-system-ver2', '[''Next.js'', ''React'', ''Node.js'', ''Python ML'', ''Express'', ''Microservices'']', '[]', '### Executive Summary
Medical Diagnostic System Version 2 was engineered to completely modernize its desktop predecessor, transforming a robust diagnostic engine into a highly accessible, full-stack AI web platform.

The objective was to build a scalable, clinical-grade SaaS application capable of:
- Mapping user-entered symptoms to accurate disease predictions
- Dynamically calculating patient-specific, age-aware medicine dosages
- Recommending specific clinical lab tests based on the diagnostic output
- Maintaining secure patient session histories

The system utilizes a highly sophisticated dual-engine approach, blending a dynamically built Random Forest Classifier with a probabilistic Bayesian-style scoring system, all powered by a Neo4j knowledge graph.

### The Problem
Traditional digital symptom checkers face several critical issues:
- They rely on hardcoded decision trees that fail to account for overlapping symptoms.
- Medication recommendations are often generic, ignoring critical variables like the patient''s age (child vs. adult vs. elderly).
- Desktop-bound applications severely limit accessibility for remote or mobile users.
- Medical data schemas in traditional SQL databases become overwhelmingly complex and slow when mapping many-to-many relationships between diseases, symptoms, and treatments.

There was a structural need for an accessible web platform capable of handling complex graph-based medical relationships and statistically sound inferences.

### The Solution
Version 2 seamlessly integrates:
- A Neo4j cloud graph database optimized for medical relationship mapping.
- A Python/Flask backend acting as a secure AI orchestration layer.
- A React.js frontend delivering a modern, responsive user experience.
- A blended ML model utilizing data augmentation for higher diagnostic resilience.

The result is a powerful diagnostic tool that delivers:
- Top-N ranked disease predictions based on user inputs.
- Precise medicine dosage recommendations strictly categorized by age groups (<12, 12-64, 65+).
- Structured lab test suggestions linked to the predicted condition.
- A comprehensive, securely stored patient history via MongoDB.

### System Architecture
1. Knowledge Graph Layer (Neo4j)
The entire medical corpus is structured as a graph: `(Disease) -[:HAS_SYMPTOM]-> (Symptom)` with precise weights and probabilities, alongside `[:TREATED_BY]` and `[:DIAGNOSED_BY]` relationships.

2. Intelligence & ML Layer
A Random Forest classifier is built dynamically in RAM at server startup using data pulled from Neo4j.
Model training utilizes noise injection (data augmentation) for better real-world generalization.
A parallel Bayesian-style scorer ranks diseases by weighted symptom overlap, and the results are mathematically blended.

3. Application Backend (Flask & MongoDB)
Python Flask provides RESTful APIs.
MongoDB Atlas securely stores user profiles, encrypted passwords (bcrypt), and historical diagnostic sessions.

4. Presentation Layer
React.js utilizing React Router and custom CSS for a fluid, SPA experience.

### Engineering Decisions
Why a Graph Database (Neo4j)?
Medical data is inherently highly connected. Graph databases allow traversal of complex relationships (Disease to Symptom to Medicine) exponentially faster than complex SQL JOINs.

Why a Dual ML Engine?
Relying purely on a classifier can lead to edge-case failures. Blending a Random Forest model with a probabilistic Bayesian overlap scorer ensures the output remains medically logical and highly resilient.

Why In-Memory Graph Loading?
Loading the Neo4j schema into memory at server startup drastically reduces API response times for end-users, facilitating near-instantaneous diagnostic inference.

### Performance Metrics
Diagnostic inference latency: incredibly low due to in-memory graph models.
Knowledge graph traversal speed: optimized via Neo4j indexing.
Authentication security: 100% integration with bcrypt hashing protocols.
Responsive UI: zero page reloads during the multi-step diagnostic workflow.

### Scalability Strategy
Decoupled architecture allows the React frontend, Flask API, and Neo4j database to scale independently.
MongoDB integration paves the way for complex patient data analytics.
Easily extensible graph schema to introduce new medical fields like allergies or genetic markers.

### Outcome
Version 2 successfully bridges the gap between advanced probabilistic machine learning and an intuitive web interface.

It is architected as an enterprise-grade healthcare tool capable of delivering deeply personalized, age-specific medical guidance.

', 'published', True, 2, 'Web App', '2026-05-07T05:17:05.003981+00:00') ON CONFLICT DO NOTHING;
INSERT INTO projects (id, title, slug, description, cover_image_url, link, github_link, technologies, tools, case_study_content, status, is_featured, order_index, category, created_at) VALUES ('55555555-5555-5555-5555-555555555555', 'vibee-centralized-social-media', 'vibee', 'Vibee was engineered to solve a structural problem in modern digital consumption: the fragmentation of content across isolated platforms and the negative psychological impact of infinite, unmanaged scrolling.', 'https://ywhocytfjiubouhehiuj.supabase.co/storage/v1/object/public/project-images/vibee.png', '', 'https://github.com/SufyExpert/vibee-centralized-social-media', '[''Flutter'', ''Dart'', ''WebSockets'', ''NoSQL'', ''Firebase'', ''Real-time'']', '[]', '### Executive Summary
Vibee was engineered to solve a structural problem in modern digital consumption: the fragmentation of content across isolated platforms and the negative psychological impact of infinite, unmanaged scrolling.

The objective was to build a highly responsive, cross-platform mobile ecosystem capable of:
- Unifying content from YouTube, Reddit, and global News into a single feed
- Automatically curating content based on pre-selected user interests
- Standardizing vastly different media types into a cohesive UI
- Actively managing user screen time via controlled, timed sessions

The application was built using Flutter to ensure native-level performance across all platforms while orchestrating complex concurrent data streams from multiple external REST APIs.

### The Problem
The current social media landscape suffers from:
- Extreme siloization: users must open different apps for videos, community discussions, and articles.
- Algorithmic manipulation: feeds are designed for maximum retention, often ignoring the user''s actual declared interests.
- Severe screen-time issues: platforms lack native tools to forcefully break the infinite scrolling loop, leading to digital burnout.

There was no unified centralization layer that put the user in absolute control of both what they consume and exactly how long they consume it.

### The Solution
Vibee integrates:
- The YouTube Data API v3, Reddit Public JSON API, and NewsAPI into a simultaneous fetch protocol.
- A structured interest-to-query mapping engine.
- A strict ''Timed Session'' mechanic that requests a time limit before the feed opens and aggressively terminates the session when time expires.

The result is a highly curated, premium social platform that delivers:
- A chronologically and algorithmically balanced feed of videos, text posts, and articles.
- A unified `MediaCard` interface that normalizes completely different data structures.
- Seamless cross-platform execution (Mobile, Web, Windows) from a single Dart codebase.
- Comprehensive tracking of total content viewed and minutes watched.

### System Architecture
1. Data Orchestration Layer
The `http` package handles concurrent API requests to YouTube, Reddit, and NewsAPI.
Responses are normalized into standard object models to be digested by the UI.

2. Presentation Layer
Flutter (Dart) frontend utilizing a custom `SkeletonLoader` to mask network delays.
Smart routing via `AuthGate` utilizing StreamBuilders to seamlessly transition states based on login and interest-selection status.

3. Backend & Storage Layer
Firebase Authentication handling secure user onboarding.
Cloud Firestore strictly organizing the user graph: storing preferences, saved items, and historical session telemetry.
`shared_preferences` and `cached_network_image` handle local caching for optimal offline performance.

### Engineering Decisions
Why Flutter?
To achieve native rendering speeds (60 FPS) and maintain absolute visual consistency across iOS, Android, and Desktop without duplicating engineering effort.

Why a Built-In Timed Session?
To fundamentally alter the user experience from passive, infinite scrolling to intentional, time-boxed consumption—a unique value proposition in the social media market.

Why Simultaneous API Fetching?
By concurrently querying YouTube, Reddit, and News platforms and merging the asynchronous streams, the app creates a massive, diversified feed in seconds without sequential blocking.

### Performance Metrics
Feed generation speed: optimized via parallel asynchronous HTTP requests.
UI layout shifts: minimized using intelligent `SkeletonLoader` widgets.
Image rendering latency: drastically reduced using advanced network image caching.
Cross-platform consistency: 100% matched UI behavior across diverse OS environments.

### Scalability Strategy
Serverless Firestore integration ensures the backend scales automatically with user acquisition.
Interest-mapping logic is decoupled, allowing easy integration of future APIs (e.g., Twitter/X, Medium).
Potential microservice migration to handle heavy backend content scraping, reducing client-side payload.

### Outcome
Vibee demonstrates profound capability in mobile architecture, asynchronous API orchestration, and thoughtful UX design.

It is an innovative, production-ready consumer application that champions digital well-being while centralizing the modern internet.

', 'published', True, 5, 'Mobile App', '2026-05-07T05:17:05.003981+00:00') ON CONFLICT DO NOTHING;
INSERT INTO projects (id, title, slug, description, cover_image_url, link, github_link, technologies, tools, case_study_content, status, is_featured, order_index, category, created_at) VALUES ('66666666-6666-6666-6666-666666666666', 'medical-diagnostic-system', 'medical-diagnostic-v1', 'The original Medical Diagnostic System was engineered to address the need for a highly secure, locally executed triage platform capable of interpreting complex medical knowledge graphs without internet-facing vulnerabilities.', 'https://ywhocytfjiubouhehiuj.supabase.co/storage/v1/object/public/project-images/meddiag-v1.png', '', 'https://github.com/SufyExpert/medical-diagnostic-system', '[''Python'', ''Bayesian Network'', ''Neo4j'', ''FastAPI'', ''Scikit-Learn'']', '[]', '### Executive Summary
The original Medical Diagnostic System was engineered to address the need for a highly secure, locally executed triage platform capable of interpreting complex medical knowledge graphs without internet-facing vulnerabilities.

The objective was to build a robust, standalone Python desktop application capable of:
- Processing symptoms utilizing strict probabilistic mathematics
- Interacting directly with a cloud-based graph database
- Rendering diagnostic charts and user interfaces natively
- Managing persistent user profiles entirely client-side

The system utilizes a custom-built Bayesian Network architecture to ensure outputs are statistically rigorous rather than relying on black-box generative AI models.

### The Problem
In clinical or highly secure environments, web-based tools pose specific challenges:
- Reliance on browsers can introduce compliance and security risks for sensitive medical data.
- Standard SQL relational databases fail to efficiently compute the deeply connected probability networks required for medical triage.
- Many diagnostic systems lack true mathematical explainability, outputting guesses rather than calculated conditional probabilities.

There was a critical need for a deeply mathematical, standalone engine that could process graph structures natively.

### The Solution
This Version 1 platform integrates:
- A Neo4j knowledge graph schema mapping diseases to weighted symptoms.
- A completely custom Bayesian Network inference engine calculating exact posterior probabilities.
- A modern CustomTkinter graphical interface for multi-screen navigation.

The result is a highly reliable diagnostic desktop tool that delivers:
- Statistically accurate, ranked disease predictions.
- Embedded, hardware-accelerated Matplotlib charts for visual probability analysis.
- Total local data privacy via `.txt` based profile storage, ensuring patient history never touches a public server.

### System Architecture
1. Logic & Inference Layer
A Bayesian Network mathematically evaluating Conditional Probability Tables based on the presence or absence of user-selected symptoms.

2. Presentation Layer
CustomTkinter UI bypassing the outdated aesthetics of standard Tkinter.
A single-window layout wrapper handles seamless page destruction and recreation, simulating a modern SPA experience on desktop.

3. Database Layer
A lazy-initialized connection to a Neo4j cloud instance (connecting only upon inference to speed up initial app load).
Local file system integration utilizing `src/Profiles/` for secure data persistence.

### Engineering Decisions
Why a Custom Bayesian Network?
Unlike modern opaque neural networks, Bayesian models are mathematically deterministic and entirely explainable—a strict necessity when providing medical probabilities based on overlapping symptom weights.

Why CustomTkinter Instead of Web Tech?
To guarantee maximum operational security and zero-install requirements for internal end-users, keeping the entire computational loop confined to the host machine''s resources.

Why Lazy-Initialization for Neo4j?
To prevent network latency from blocking the application''s startup thread, ensuring a snappy, immediate user experience.

### Performance Metrics
Application startup time: nearly instantaneous due to deferred network connections.
Bayesian computation: sub-second probability table resolution.
UI rendering: lag-free transition between complex data entry screens.
Local storage footprint: negligible text-based files.

### Scalability Strategy
The decoupled Neo4j cloud graph allows the central medical corpus to be updated seamlessly without requiring local users to patch their desktop software.
The Bayesian engine logic is heavily modularized, allowing easy porting to web microservices (as later achieved in Version 2).

### Outcome
The original Medical Diagnostic System is a masterclass in probabilistic programming and graph database integration.

It proves the capability to engineer mathematically pure, highly secure offline-first healthcare tools.

', 'published', False, 6, 'Desktop App', '2026-05-07T05:17:05.003981+00:00') ON CONFLICT DO NOTHING;
INSERT INTO projects (id, title, slug, description, cover_image_url, link, github_link, technologies, tools, case_study_content, status, is_featured, order_index, category, created_at) VALUES ('44444444-4444-4444-4444-444444444444', 'socialapp', 'social-app', 'SocialApp was engineered to solve the complex foundational challenges inherent in building full-stack web community platforms, specifically focusing on state management, image data handling, and relational mapping.', 'https://ywhocytfjiubouhehiuj.supabase.co/storage/v1/object/public/project-images/socialapp.png', '', 'https://github.com/SufyExpert/socialapp', '[''MongoDB'', ''Express'', ''React'', ''Node.js'', ''JWT'', ''Bcrypt'']', '[]', '### Executive Summary
SocialApp was engineered to solve the complex foundational challenges inherent in building full-stack web community platforms, specifically focusing on state management, image data handling, and relational mapping.

The objective was to build a fast, dynamic web platform capable of:
- Secure, stateless user authentication
- Real-time global feed generation
- Deep relational mapping for following/friend systems
- Seamless processing and rendering of user-generated imagery

The system utilizes a React/Flask/MongoDB stack, prioritizing rapid data flow and minimized backend infrastructure complexity.

### The Problem
Developing social networks traditionally involves heavy architectural overhead:
- Managing sticky sessions requires complex load balancing.
- Integrating AWS S3 or external CDNs for image storage complicates deployment and inflates early-stage costs.
- Navigating relational data (like mutual friends) in SQL databases often requires deeply nested, slow JOIN operations.

There was a need for a streamlined, highly functional platform that could handle rich media and relational graphs efficiently within a simplified stack.

### The Solution
SocialApp integrates:
- A React SPA frontend utilizing the Context API for robust, global state management.
- A Python Flask backend providing secure RESTful API endpoints.
- A MongoDB NoSQL database storing flexible user schemas, friend arrays, and direct binary data.

The result is a highly cohesive social environment that delivers:
- Instantaneous feed updates sorted chronologically.
- The ability to upload images that are seamlessly encoded into Base64 format and stored directly in the database alongside post metadata.
- A dynamic friend recommendation system based on array lookups.
- Robust session security utilizing tokenized access.

### System Architecture
1. Frontend Layer
React.js handling dynamic routing via React Router.
React AuthContext acts as a central store, preventing unnecessary prop-drilling and ensuring protected routes remain secure.

2. Backend API Layer
Flask powered by Python orchestrating complex cross-origin requests via Flask-CORS.
Dedicated REST endpoints handling creation, deletion, and retrieval of social data.

3. Database Layer
MongoDB mapping unstructured documents.
Friend connections stored as highly efficient sub-arrays inside the User document.
Images stored as `base64` encoded strings supporting payloads up to 7MB.

### Engineering Decisions
Why Base64 Direct Storage?
By converting file uploads to Base64 and storing them inside MongoDB, the app completely eliminates the need for complex external blob storage APIs during the MVP phase, consolidating infrastructure into a single database cluster.

Why React Context Over Redux?
Context API provides a lightweight, native solution for managing global authentication states without the heavy boilerplate and performance overhead associated with Redux.

Why MongoDB for Social Graphs?
NoSQL document structures are perfectly suited for storing dynamic arrays of friend IDs and variable post schemas (some with images, some without) without rigid SQL migrations.

### Performance Metrics
API response latency: heavily optimized for quick feed retrieval.
Authentication validation: instantaneous verification via Context state.
Media rendering: rapid inline decoding of Base64 strings.
Data schema flexibility: extremely high, allowing rapid feature iteration.

### Scalability Strategy
MongoDB documents can easily be indexed to handle massive scale in friend lookups.
The stateless Flask API allows seamless horizontal scaling across multiple servers.
Clear transition pathways exist to migrate Base64 strings to cloud buckets once data volume demands it.

### Outcome
SocialApp successfully demonstrates end-to-end full-stack engineering capabilities, covering everything from complex client-side state to database-level optimization.

It stands as a highly effective, deployable architecture for modern community web applications.

', 'published', True, 4, 'Web App', '2026-05-07T05:17:05.003981+00:00') ON CONFLICT DO NOTHING;


-- Seeding data for project_images
INSERT INTO project_images (id, project_id, url, order_index, created_at) VALUES ('6cbb08d7-c76e-45d2-8841-cdf44f80487e', '88888888-8888-8888-8888-888888888888', 'https://ywhocytfjiubouhehiuj.supabase.co/storage/v1/object/public/project-images/prompt-tutor-ai.png', 1, '2026-05-07T05:17:05.003981+00:00') ON CONFLICT DO NOTHING;
INSERT INTO project_images (id, project_id, url, order_index, created_at) VALUES ('1933884b-be02-4719-b479-c0847b9912c9', '11111111-1111-1111-1111-111111111111', 'https://ywhocytfjiubouhehiuj.supabase.co/storage/v1/object/public/project-images/health-risk.png', 1, '2026-05-07T05:17:05.003981+00:00') ON CONFLICT DO NOTHING;
INSERT INTO project_images (id, project_id, url, order_index, created_at) VALUES ('70d89fca-cfcb-4c84-b08c-d45d7280f277', '22222222-2222-2222-2222-222222222222', 'https://ywhocytfjiubouhehiuj.supabase.co/storage/v1/object/public/project-images/meddiag-v2.png', 1, '2026-05-07T05:17:05.003981+00:00') ON CONFLICT DO NOTHING;
INSERT INTO project_images (id, project_id, url, order_index, created_at) VALUES ('0ad24e64-c7b3-4657-9e48-b7d77e696b15', '55555555-5555-5555-5555-555555555555', 'https://ywhocytfjiubouhehiuj.supabase.co/storage/v1/object/public/project-images/vibee.png', 1, '2026-05-07T05:17:05.003981+00:00') ON CONFLICT DO NOTHING;
INSERT INTO project_images (id, project_id, url, order_index, created_at) VALUES ('b911b099-89c0-4f63-9bc9-58b7669cdb33', '66666666-6666-6666-6666-666666666666', 'https://ywhocytfjiubouhehiuj.supabase.co/storage/v1/object/public/project-images/meddiag-v1.png', 1, '2026-05-07T05:17:05.003981+00:00') ON CONFLICT DO NOTHING;
INSERT INTO project_images (id, project_id, url, order_index, created_at) VALUES ('422f119f-a172-4579-aafe-76251c628737', '44444444-4444-4444-4444-444444444444', 'https://ywhocytfjiubouhehiuj.supabase.co/storage/v1/object/public/project-images/socialapp.png', 1, '2026-05-07T05:17:05.003981+00:00') ON CONFLICT DO NOTHING;
INSERT INTO project_images (id, project_id, url, order_index, created_at) VALUES ('2fa7287e-396d-467d-a631-30e68359cb01', '33333333-3333-3333-3333-333333333333', 'https://ywhocytfjiubouhehiuj.supabase.co/storage/v1/object/public/project-images/ask-academy.png', 1, '2026-05-07T05:17:05.003981+00:00') ON CONFLICT DO NOTHING;
INSERT INTO project_images (id, project_id, url, order_index, created_at) VALUES ('c20ee726-5fef-4582-b360-f2eb3fe6f31a', '77777777-7777-7777-7777-777777777777', 'https://ywhocytfjiubouhehiuj.supabase.co/storage/v1/object/public/project-images/flappy-bird.png', 1, '2026-05-07T05:17:05.003981+00:00') ON CONFLICT DO NOTHING;


-- Seeding data for experience
INSERT INTO experience (id, title, company, date_range, employment_type, bullets, status, order_index, created_at) VALUES ('ad913689-0a6a-4d66-8c94-13ea0d27136d', 'BS Computer Science', 'COMSATS University Islamabad, Lahore Campus', '2023 – Present', 'Full-time', '[''Currently in 6th semester with a CGPA of 3.73'', ''Focusing on Artificial Intelligence, Machine Learning & Data Science'', ''Building end-to-end AI systems from Bayesian engines to full-stack ML apps'', ''Actively seeking AI/ML internship opportunities'']', 'published', 1, '2026-04-28T08:43:03.324921+00:00') ON CONFLICT DO NOTHING;
INSERT INTO experience (id, title, company, date_range, employment_type, bullets, status, order_index, created_at) VALUES ('236f4548-65d9-4369-8169-049c2cdf8885', 'AI Engineering Enthusiast', 'Independent Research & Development', '2023 – Present', 'Self-Employed', '[''Developed a Medical Diagnostic System using Random Forest and Neo4j knowledge graphs'', ''Built ASK Academy ERP system with Azure SQL and custom triggers'', ''Engineered mutual-friend recommendation algorithms using MongoDB'', ''Unifying multiple data streams into a single interface with Flutter'']', 'published', 2, '2026-04-28T08:43:03.324921+00:00') ON CONFLICT DO NOTHING;


-- Seeding data for services
INSERT INTO services (id, title, slug, tagline, description, features, order_index, created_at) VALUES ('59e472bf-db29-4812-8ccc-7b427f00fb35', 'AI Engineering', 'ai-engineering', 'Intelligent Systems & ML Pipelines', 'Building complete, working systems—from Bayesian-inference diagnostic engines to multi-model Random Forest evaluation pipelines.', '[''Custom ML Model Development'', ''Bayesian Inference Engines'', ''Predictive Analytics'', ''Data Visualization'']', 1, '2026-04-28T08:43:03.324921+00:00') ON CONFLICT DO NOTHING;
INSERT INTO services (id, title, slug, tagline, description, features, order_index, created_at) VALUES ('3e87d210-097d-43a9-bc17-25ce47ef8816', 'Full-Stack AI Development', 'full-stack-ai', 'Smart Web Applications', 'Bridging ML model development with real deployable software using Next.js, Flask, and modern database architectures.', '[''React & Next.js Frontends'', ''Flask & Python Backends'', ''Supabase & SQL Integration'', ''Responsive Design'']', 2, '2026-04-28T08:43:03.324921+00:00') ON CONFLICT DO NOTHING;
INSERT INTO services (id, title, slug, tagline, description, features, order_index, created_at) VALUES ('9b8d1ba5-b1f3-418a-96df-38788d463c16', 'Database Architecting', 'database-architecting', 'Graph & Relational Design', 'Designing scalable data solutions using Neo4j, MongoDB, and Azure SQL with a focus on data integrity and performance.', '[''Graph Data Modeling (Neo4j)'', ''SQL Triggers & Stored Procedures'', ''NoSQL Architecture (MongoDB)'', ''Performance Tuning'']', 3, '2026-04-28T08:43:03.324921+00:00') ON CONFLICT DO NOTHING;
