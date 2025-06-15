# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Running the Application
```bash
python run.py
```
- Starts the Flask application on port 8000 (or PORT environment variable)
- Automatically detects Railway vs local environment
- Application accessible at http://localhost:8000
- Health check endpoint: http://localhost:8000/api/test

### Testing
```bash
# Test data layer functionality
python test_data_layer.py

# Test customization features  
python test_customize.py
```

### Dependencies
```bash
pip install -r requirements.txt
```

## Architecture Overview

This is a TimefoldAI-powered timetable optimization application with a Flask backend and vanilla JavaScript frontend.

### Core Components

**Backend Structure:**
- `run.py` - Application entry point with Railway deployment configuration
- `backend/app.py` - Flask application factory with Blueprint registration
- `backend/api/routes.py` - Main API endpoints for optimization and data retrieval
- `backend/api/customize_routes.py` - Customization API endpoints
- `backend/services/optimization_service.py` - TimefoldAI solver integration
- `backend/models/timefold_models.py` - TimefoldAI domain model definitions
- `backend/models/database.py` - Data repository abstraction layer
- `backend/data/*.json` - Configuration and data files

**Frontend Structure:**
- `frontend/templates/index.html` - Main web interface
- `frontend/static/js/main.js` - Core JavaScript functionality
- `frontend/static/css/styles.css` - Application styling

### TimefoldAI Integration

The application uses TimefoldAI v1.22.1b0 for constraint-based optimization:

**Domain Model:**
- `TimeTable` - @planning_solution containing the complete timetable
- `Lesson` - @planning_entity with PlanningVariables for timeslot and room assignment
- Problem facts: `Timeslot`, `Room`, `Subject`, `Teacher`, `StudentGroup`

**Constraints (backend/models/timefold_models.py:74-197):**
- Hard constraints: room_conflict, teacher_conflict, student_group_conflict
- Soft constraints: subject distribution, daily limits, teacher efficiency

**Solver Configuration:**
- 30-second optimization limit for production
- Meta-heuristic algorithms: Tabu Search, Simulated Annealing, Hill Climbing
- HardSoftScore for multi-objective optimization

### API Endpoints

**Core API (backend/api/routes.py):**
- `GET /api/test` - Health check for Railway deployment
- `GET /api/demo-data` - Retrieve demo timetable data
- `GET /api/subjects` - List all subjects
- `GET /api/teachers` - List all teachers  
- `POST /api/optimize` - Start asynchronous optimization
- `GET /api/optimization-status` - Check optimization progress

**Customization API (backend/api/customize_routes.py):**
- Data management endpoints for subjects, teachers, timeslots

### Data Layer

**Repository Pattern:**
- `DataRepository` - Abstract base class for data access
- `JSONDataRepository` - File-based implementation using JSON storage
- Data files located in `backend/data/`: subjects.json, teachers.json, system_config.json

### Deployment

**Railway Platform:**
- Configured via `railway.toml` with health check on `/api/test`
- Uses `Dockerfile` with Python 3.12 and Java 17 for TimefoldAI
- Memory optimization: JVM configured with 400MB limit
- Environment detection via `RAILWAY_ENVIRONMENT` variable

**Docker Configuration:**
- Base image: python:3.12-slim
- Java 17 OpenJDK for TimefoldAI solver
- Exposes port 8000

### Memory and Performance Optimization

The application includes several optimizations for Railway deployment:
- JVM memory limit: 400MB (`JAVA_OPTS=-Xmx400m`)
- Garbage collection optimization with G1GC
- Threaded Flask server for better concurrency
- Async optimization processing to prevent timeouts

### Data Configuration

System configuration managed through `backend/data/system_config.json`:
- Timeslot definitions (periods, days, times)
- Subject weekly hour requirements
- Teacher-subject assignments
- Student group definitions

### Testing Strategy

- `test_data_layer.py` - Tests data repository functionality and lesson generation
- `test_customize.py` - Tests customization API endpoints
- No formal test framework - uses direct Python execution

Note: The codebase contains Japanese language comments and logging messages, indicating it was developed for Japanese educational institutions.