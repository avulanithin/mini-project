# Blood Donation Camp Queue Simulation & Planning System

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![Flask](https://img.shields.io/badge/flask-3.0.0-red)
![License](https://img.shields.io/badge/license-MIT-yellow)

A complete, production-ready web application for simulating and optimizing blood donation camp operations using discrete-event simulation and probability-based modeling.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Database Schema](#database-schema)
- [Simulation Model](#simulation-model)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Screenshots](#screenshots)
- [Contributing](#contributing)

## 🎯 Overview

Blood donation camps face significant challenges in resource allocation, queue management, and staff optimization. This system provides camp organizers with a powerful simulation tool to:

- **Plan** optimal resource allocation before the actual event
- **Simulate** donor arrivals, queue behavior, and staff utilization
- **Optimize** service counters and staffing levels
- **Analyze** performance metrics and bottlenecks
- **Compare** different configuration scenarios

The application uses **discrete-event simulation** with **Poisson arrival processes** and **multi-stage queuing** to model realistic camp operations.

## ✨ Features

### Core Functionality

- ✅ **Multi-Stage Queue Simulation**
  - Registration → Medical Screening → Blood Donation
  - Independent queues for each stage
  - Parallel service counters

- ✅ **Discrete-Event Simulation Engine**
  - Poisson arrival distribution
  - Exponential/Uniform service time distributions
  - First-Come-First-Serve (FCFS) queue discipline
  - Multiple server support

- ✅ **Comprehensive Analytics**
  - Average and maximum waiting times
  - Queue length over time
  - Server utilization rates
  - Donor-level timeline tracking

- ✅ **Interactive Visualizations**
  - Real-time queue length charts
  - Waiting time scatter plots
  - Server utilization bar charts
  - Comparison dashboards

- ✅ **Configuration Management**
  - Flexible camp parameter setup
  - Customizable staffing levels
  - Variable service time distributions
  - Arrival rate configuration

- ✅ **Scenario Comparison**
  - Compare multiple simulation runs
  - Side-by-side metric analysis
  - Visual performance comparison

## 🛠 Technology Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Python 3.8+, Flask 3.0.0 |
| **Frontend** | HTML5, CSS3, JavaScript (ES6+) |
| **Database** | SQLite 3 |
| **Charts** | Chart.js 4.4.0 |
| **Architecture** | MVC + REST API |
| **Simulation** | NumPy, SciPy |

**No UI frameworks** (Bootstrap, Tailwind, etc.) - Pure CSS implementation for academic clarity.

## 🏗 System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Client Browser                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │   HTML   │  │   CSS    │  │JavaScript│              │
│  │Templates │  │  Styles  │  │Chart.js  │              │
│  └──────────┘  └──────────┘  └──────────┘              │
└─────────────────────────────────────────────────────────┘
                        │ HTTP/REST API
                        ▼
┌─────────────────────────────────────────────────────────┐
│                 Flask Application Server                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │  Routes  │  │  Models  │  │ Services │              │
│  │(API/Web) │  │ (ORM)    │  │(Business)│              │
│  └──────────┘  └──────────┘  └──────────┘              │
│                        │                                 │
│               ┌────────▼────────┐                       │
│               │   Simulation    │                       │
│               │     Engine      │                       │
│               │(Discrete-Event) │                       │
│               └─────────────────┘                       │
└─────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│                   SQLite Database                        │
│  ┌───────┐  ┌───────────┐  ┌────────┐  ┌──────────┐   │
│  │ Camps │  │Simulations│  │ Donors │  │ Stations │   │
│  └───────┘  └───────────┘  └────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────┘
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (optional)

### Step 1: Clone or Download

```bash
# Clone the repository (if using Git)
git clone <repository-url>
cd mini-project

# Or download and extract the ZIP file
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Initialize Database

The database will be automatically initialized when you first run the application.

### Step 5: Run the Application

```bash
python app.py
```

The application will start on `http://127.0.0.1:5000`

### Verification

1. Open your web browser
2. Navigate to `http://localhost:5000`
3. You should see the home page

## 📖 Usage

### 1. Configure a New Camp

1. Navigate to **Setup Camp** from the navigation menu
2. Fill in the camp details:
   - **Camp Name**: Descriptive name for your event
   - **Start Time & End Time**: Camp operating hours
   - **Duration**: Automatically calculated
   - **Max Donors**: Optional limit (leave empty for unlimited)

3. Configure staffing:
   - **Number of Donation Counters**: Parallel blood donation stations
   - **Number of Screening Staff**: Medical screening personnel
   - **Average Screening Time**: Time per donor (minutes)
   - **Average Donation Time**: Time per donation (minutes)

4. Set simulation parameters:
   - **Arrival Rate**: Expected donors per hour (λ)
   - **Arrival Distribution**: Poisson (default)
   - **Service Distribution**: Exponential or Uniform
   - **Queue Discipline**: FCFS (default)

5. Click **Run Simulation**

### 2. View Results

After simulation completes, you'll be redirected to the results dashboard showing:

- **KPI Cards**: Total donors, served/unserved, wait times, utilization
- **Queue Length Chart**: Real-time queue dynamics over camp duration
- **Waiting Time Chart**: Distribution of wait times across donors
- **Utilization Chart**: Server efficiency by station
- **Donor Table**: Detailed timeline for each donor
- **Station Table**: Performance metrics per service counter

### 3. Review History

- Navigate to **History** to see all past simulations
- View key metrics at a glance
- Click **View** to see detailed results

### 4. Compare Scenarios

1. Go to **Compare** page
2. Select 2-4 simulations using checkboxes
3. Click **Compare Selected**
4. Analyze side-by-side metrics and charts
5. Identify optimal configuration

## 🗄 Database Schema

### Camps Table
```sql
CREATE TABLE camps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    duration_minutes INTEGER NOT NULL,
    max_donors INTEGER,
    peak_hours TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Simulations Table
```sql
CREATE TABLE simulations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    camp_id INTEGER NOT NULL,
    num_servers INTEGER NOT NULL,
    num_screening_staff INTEGER NOT NULL,
    avg_screening_time REAL NOT NULL,
    avg_donation_time REAL NOT NULL,
    arrival_rate REAL NOT NULL,
    arrival_distribution TEXT DEFAULT 'Poisson',
    service_distribution TEXT DEFAULT 'Exponential',
    queue_discipline TEXT DEFAULT 'FCFS',
    allow_idle_servers INTEGER DEFAULT 1,
    total_donors_simulated INTEGER,
    donors_served INTEGER,
    donors_unserved INTEGER,
    avg_waiting_time REAL,
    max_waiting_time REAL,
    avg_queue_length REAL,
    avg_server_utilization REAL,
    simulation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (camp_id) REFERENCES camps (id)
);
```

### Donors Table
```sql
CREATE TABLE donors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    simulation_id INTEGER NOT NULL,
    donor_index INTEGER NOT NULL,
    arrival_time REAL NOT NULL,
    registration_start REAL,
    registration_end REAL,
    screening_start REAL,
    screening_end REAL,
    donation_start REAL,
    donation_end REAL,
    registration_wait REAL,
    screening_wait REAL,
    donation_wait REAL,
    total_wait_time REAL,
    total_time_in_system REAL,
    served INTEGER DEFAULT 0,
    FOREIGN KEY (simulation_id) REFERENCES simulations (id)
);
```

### Service Stations Table
```sql
CREATE TABLE service_stations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    simulation_id INTEGER NOT NULL,
    station_type TEXT NOT NULL,
    station_number INTEGER NOT NULL,
    utilization_rate REAL NOT NULL,
    total_service_time REAL NOT NULL,
    donors_served INTEGER NOT NULL,
    FOREIGN KEY (simulation_id) REFERENCES simulations (id)
);
```

## 🔬 Simulation Model

### Theoretical Foundation

The system implements a **M/M/c queuing model** with multiple stages:

- **M**: Markovian (Poisson) arrivals
- **M**: Markovian (Exponential) service times
- **c**: Multiple parallel servers

### Process Flow

```
Donor Arrival (Poisson λ)
       │
       ▼
┌─────────────┐
│Registration │ (1 server, ~3 min)
│   Queue     │
└─────────────┘
       │
       ▼
┌─────────────┐
│  Screening  │ (n servers, avg_screening_time)
│   Queue     │
└─────────────┘
       │
       ▼
┌─────────────┐
│  Donation   │ (m servers, avg_donation_time)
│   Queue     │
└─────────────┘
       │
       ▼
   Departure
```

### Key Equations

**Arrival Rate (λ)**: Exponential inter-arrival time
```
inter_arrival_time = -ln(U) / λ
where U ~ Uniform(0,1)
```

**Service Time**: 
- Exponential: `service_time = -ln(U) × avg_time`
- Uniform: `service_time ~ Uniform(0.7×avg, 1.3×avg)`

**Waiting Time**:
```
Total_Wait = Registration_Wait + Screening_Wait + Donation_Wait
```

**Utilization**:
```
Utilization = (Total_Service_Time / Camp_Duration) × 100%
```

### Simulation Algorithm

1. **Initialize**: Create event queue, servers, and queues
2. **Generate Arrivals**: Schedule donor arrivals using Poisson process
3. **Process Events**: 
   - Pop next event from priority queue
   - Update system state
   - Schedule future events (service completions)
4. **Track Metrics**: Record queue lengths, waiting times, utilization
5. **Terminate**: Stop when camp duration ends
6. **Compute Statistics**: Aggregate donor and system metrics

## 📡 API Documentation

### Base URL
```
http://localhost:5000/api
```

### Endpoints

#### Camps

**Create Camp**
```http
POST /api/camps
Content-Type: application/json

{
  "name": "City Hospital Blood Drive",
  "start_time": "09:00",
  "end_time": "17:00",
  "duration_minutes": 480,
  "max_donors": 100,
  "peak_hours": "11:00-13:00"
}

Response: { "success": true, "camp_id": 1 }
```

**Get All Camps**
```http
GET /api/camps

Response: { "success": true, "camps": [...] }
```

**Get Camp by ID**
```http
GET /api/camps/{id}

Response: { "success": true, "camp": {...} }
```

#### Simulations

**Run Simulation**
```http
POST /api/simulations/run
Content-Type: application/json

{
  "camp_id": 1,
  "num_servers": 3,
  "num_screening_staff": 2,
  "avg_screening_time": 10,
  "avg_donation_time": 15,
  "arrival_rate": 5,
  "service_distribution": "Exponential"
}

Response: { 
  "success": true, 
  "simulation_id": 1,
  "summary": {...}
}
```

**Get Simulation**
```http
GET /api/simulations/{id}

Response: { 
  "success": true, 
  "simulation": {...},
  "camp": {...}
}
```

**Get All Simulations**
```http
GET /api/simulations

Response: { "success": true, "simulations": [...] }
```

**Get Donors for Simulation**
```http
GET /api/simulations/{id}/donors

Response: { "success": true, "donors": [...] }
```

**Get Service Stations**
```http
GET /api/simulations/{id}/stations

Response: { "success": true, "stations": [...] }
```

**Get Queue Statistics**
```http
GET /api/simulations/{id}/queue-stats

Response: { "success": true, "queue_data": [...] }
```

**Compare Simulations**
```http
POST /api/simulations/compare
Content-Type: application/json

{
  "simulation_ids": [1, 2, 3]
}

Response: { "success": true, "comparisons": [...] }
```

## 📁 Project Structure

```
mini-project/
│
├── app.py                      # Flask application entry point
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── README.md                   # This file
│
├── database/
│   └── blood_camp.db          # SQLite database (auto-created)
│
├── models/                     # Database models
│   ├── __init__.py
│   ├── database.py            # Database connection and initialization
│   ├── camp.py                # Camp model
│   ├── simulation.py          # Simulation model
│   ├── donor.py               # Donor model
│   └── service_station.py     # Service station model
│
├── services/                   # Business logic
│   ├── __init__.py
│   └── simulation_engine.py   # Discrete-event simulation engine
│
├── routes/                     # Route handlers
│   ├── __init__.py
│   ├── main_routes.py         # Web page routes
│   └── api_routes.py          # REST API endpoints
│
├── templates/                  # HTML templates
│   ├── base.html              # Base template
│   ├── index.html             # Home page
│   ├── setup.html             # Camp setup page
│   ├── results.html           # Results dashboard
│   ├── history.html           # Simulation history
│   └── compare.html           # Comparison page
│
└── static/                     # Static assets
    ├── css/
    │   └── style.css          # Main stylesheet
    └── js/
        ├── setup.js           # Setup page logic
        ├── results.js         # Results dashboard logic
        ├── history.js         # History page logic
        └── compare.js         # Comparison page logic
```

## 🎓 Academic Context

### Problem Statement

Blood donation camps are critical healthcare events that face operational challenges:

1. **Uncertain Demand**: Variable donor arrival patterns
2. **Resource Constraints**: Limited staff and equipment
3. **Queue Management**: Long wait times discourage donors
4. **Capacity Planning**: Balancing service levels with costs

### Research Questions

This system helps answer:

- How many service counters are optimal for expected demand?
- What staffing levels minimize donor wait time?
- How does arrival rate variability affect system performance?
- What is the trade-off between utilization and wait time?

### Learning Outcomes

Students/Practitioners will understand:

- Discrete-event simulation principles
- Queuing theory applications
- Probability distributions (Poisson, Exponential)
- System performance metrics
- Full-stack web development
- REST API design
- Data visualization

## 🧪 Testing

### Manual Testing Checklist

- [ ] Create camp with valid parameters
- [ ] Run simulation with various configurations
- [ ] Verify KPIs match simulation results
- [ ] Check charts render correctly
- [ ] Test table filtering and search
- [ ] Compare multiple simulations
- [ ] Print results report
- [ ] Test form validation
- [ ] Verify database persistence
- [ ] Test edge cases (0 donors, high arrival rate)

### Sample Test Scenarios

**Scenario 1: Low Load**
- Duration: 480 minutes (8 hours)
- Servers: 3
- Screening Staff: 2
- Arrival Rate: 3 per hour
- Expected: Low wait times, low utilization

**Scenario 2: High Load**
- Duration: 480 minutes
- Servers: 2
- Screening Staff: 1
- Arrival Rate: 10 per hour
- Expected: High wait times, high utilization, some unserved donors

**Scenario 3: Optimal Configuration**
- Duration: 480 minutes
- Servers: 4
- Screening Staff: 3
- Arrival Rate: 6 per hour
- Expected: Balanced wait times and utilization

## 🐛 Troubleshooting

### Database Issues

**Problem**: Database file not found
```bash
Solution: Delete existing database and restart app
rm database/blood_camp.db
python app.py
```

### Import Errors

**Problem**: ModuleNotFoundError
```bash
Solution: Reinstall dependencies
pip install -r requirements.txt
```

### Port Already in Use

**Problem**: Port 5000 is in use
```bash
Solution: Change port in app.py
app.run(port=5001)
```

### Chart Not Rendering

**Problem**: Charts don't appear
```
Solution: Check browser console for CDN errors
Ensure Chart.js CDN is accessible
```

## 🔮 Future Enhancements

- [ ] User authentication and multi-user support
- [ ] Export results to PDF/Excel
- [ ] Advanced statistical analysis
- [ ] Real-time simulation animation
- [ ] Mobile responsive design improvements
- [ ] RESTful API authentication
- [ ] Docker containerization
- [ ] Cloud deployment support
- [ ] Monte Carlo sensitivity analysis
- [ ] Machine learning for demand forecasting

## 📄 License

This project is created for academic purposes. Feel free to use and modify for educational projects.

## 👥 Authors

- Academic Project - 2026
- Course: Operations Research / Simulation Modeling
- Institution: [Your Institution]

## 🙏 Acknowledgments

- **Queuing Theory**: Based on Kendall's notation (M/M/c)
- **Simulation**: Discrete-event simulation principles
- **Flask**: Web framework by Pallets Projects
- **Chart.js**: Beautiful charts by Chart.js community
- **NumPy/SciPy**: Scientific computing libraries

## 📧 Contact

For questions or support:
- Course Instructor: [Email]
- Project Repository: [URL]

---

**Built with ❤️ for Blood Donation Camp Optimization**

---

## Quick Start Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python app.py

# Access application
http://localhost:5000

# Stop application
Ctrl + C
```

## Performance Metrics Overview

| Metric | Description | Unit |
|--------|-------------|------|
| Average Waiting Time | Mean time donors wait in all queues | minutes |
| Max Waiting Time | Longest wait experienced by any donor | minutes |
| Average Queue Length | Mean number of donors in queues | donors |
| Server Utilization | Percentage of time servers are busy | % |
| Donors Served | Number of donors who completed donation | count |
| Donors Unserved | Number of donors who couldn't be served | count |

---

**End of Documentation**
