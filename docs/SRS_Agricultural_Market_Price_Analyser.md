# <DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING><NAME OF INSTITUTE / UNIVERSITY, CITY>
# SOFTWARE REQUIREMENTS SPECIFICATION (SRS)
**Project Title:** Agricultural Market Price Analyser  
**Standard Academic Compliance:** IEEE Std 830-1998  

---

| SUBMITTED BY: | UNDER THE GUIDANCE OF: |
| :--- | :--- |
| 1. Student Name (Roll No: XXXXXX)<br>2. Student Name (Roll No: XXXXXX)<br>3. Student Name (Roll No: XXXXXX)<br><br>**Degree:** Bachelor of Technology (B.Tech)<br>**Academic Year:** 2026 - 2027 | Prof. / Dr. <Supervisor Name><br><Designation / Title><br>Department of Computer Science & Engg.<br><br>**Status:** 3rd Year Project Specification<br>**Date of Submission:** 01-11-2026 |

---

### Document Revision & Approval History
| Version | Date | Description / Major Changes | Prepared By | Reviewed By |
| :--- | :--- | :--- | :--- | :--- |
| 0.1 | 15-Sep-2026 | Initial Draft & Scope Definition | Project Team | Project Guide |
| 1.0 | 30-Sep-2026 | Final 3rd Year Mid-Term SRS Baseline | Project Team | HOD / Committee |

> *Guidance Note: This Software Requirements Specification document conforms to the IEEE 830-1998 standard recommended practice. All sections are strictly designed for 3rd-year university lab evaluation, project reviews, and system design baselines.*

---

## 1. Introduction

### 1.1 Purpose
The purpose of this Software Requirements Specification (SRS) document is to provide a complete, clear, and unambiguous definition of the functionality, external interfaces, performance targets, and constraints of the proposed system: **'Agricultural Market Price Analyser'**. This specification serves as a binding reference agreement between student developers, project evaluators, academic supervisors, and prospective end users during the 3rd-year engineering curriculum.

### 1.2 Scope of the System
The proposed application is designed to solve **the challenge of price volatility, information asymmetry, and lack of predictive visibility in Indian agricultural wholesale markets (mandis)** by delivering an end-to-end automated platform. Key boundary guidelines include:
* **In-Scope Capabilities:** Centralized data ingestion of historical mandi trade records and meteorological readings (2024 calendar year, 4.7M+ observations across 28 states, 474 districts, 2,755 markets, and 304 commodities); multi-tier price trend analytics; commodity and regional price spread comparisons; agrometeorological correlation analysis (temperature, rainfall, wind speed, pressure); machine learning next-day price prediction (Linear Regression, Random Forest, XGBoost, CatBoost); and an interactive analytical dashboard.
* **Out-of-Scope Boundaries:** Physical IoT hardware fabrication at mandi premises, live auction electronic trading/payment gateway integration, real-time live intraday ticker feeds, and multi-year macroeconomic policy simulation beyond available observed weather features.
* **Expected Benefits:** Reduction of market analysis turnaround time by 60%+, elimination of manual multi-portal price aggregation, empowerment of agricultural planners and farmers with data-driven price transparency, and highly accurate next-day price forecasting ($R^2 > 0.92$ across ML models).

### 1.3 Definitions, Acronyms, and Abbreviations
| Category | Term / Acronym | Definition / Standard Context |
| :--- | :--- | :--- |
| Standard | SRS | Software Requirements Specification (IEEE Std 830-1998 format). |
| Architecture | API | Application Programming Interface for data interchange via JSON/HTTPS. |
| Domain | Mandi / APMC | Agricultural Produce Market Committee regulated wholesale market in India. |
| Domain Metric | Modal Price | The most frequent transaction price observed for a commodity in a mandi on a given date (Rs./Quintal). |
| Storage Format | Parquet | Columnar storage file format optimized for high-performance analytics on large tabular datasets. |
| Machine Learning | XGBoost / CatBoost | Extreme Gradient Boosting and Categorical Boosting algorithms applied for tabular regression. |
| Evaluation Metric | MAE / RMSE / R² | Mean Absolute Error, Root Mean Squared Error, and Coefficient of Determination (regression metrics). |
| Framework | Streamlit | Python open-source web application framework designed for machine learning and data science dashboards. |

### 1.4 References
1. IEEE Std 830-1998: IEEE Recommended Practice for Software Requirements Specifications.
2. Software Engineering (10th Edition): Ian Sommerville, Pearson Education.
3. Agmarknet (Agricultural Marketing Information Network): Directorate of Marketing & Inspection (DMI), Government of India.
4. Open-Meteo & Indian Meteorological Department (IMD) historical weather observation archives.
5. Scikit-learn, XGBoost, and CatBoost official open-source machine learning documentation.

### 1.5 Document Overview
The remainder of this SRS is partitioned into structural sections: Section 2 outlines the product perspective, target user personas, operational context, and design constraints. Section 3 itemizes detailed functional requirements organized into logical software modules. Section 4 specifies external interfaces (UI, Hardware, Software, Network). Section 5 defines non-functional attributes (Performance, Reliability, Security). Finally, Section 6 provides standard academic modeling diagrams.

---

## 2. Overall Description

### 2.1 Product Perspective
The project is structured as a self-contained multi-tier system (comprising a Streamlit interactive presentation layer, an application analytics and ML inference engine, and a persistent Parquet/CSV data store). It processes historical market transactions and meteorological data locally without requiring external commercial server licenses.

```text
[ System Context Architecture (DFD Level 0) ]

+----------------------+       +-------------------------+
| Agmarknet Mandi Data |       | Weather Station Data    |
| (4.7M+ Records 2024) |       | (Temp, Rain, Wind, etc) |
+----------+-----------+       +------------+------------+
           |                                |
           +----------------+---------------+
                            |
                            v
       +-----------------------------------------+
       |   Data Preprocessing & Feature Store     |
       |   (Parquet / Summaries / Metadata)       |
       +--------------------+--------------------+
                            |
                            v
       +-----------------------------------------+
       | Agricultural Market Price Analyser Core |
       | - Analytics & Agrometeorology Engine    |
       | - ML Models (Linear, RF, XGB, CatBoost) |
       +--------------------+--------------------+
                            |
             +--------------+--------------+
             |                             |
             v                             v
+------------------------+    +--------------------------+
| Interactive Dashboard  |    | Model Evaluation Reports |
| (Streamlit Multi-Page) |    | (Metrics, Predictions)   |
+-----------+------------+    +--------------------------+
            |
            v
     [ End Users / Analysts / Farmers ]
```

### 2.2 User Classes and Characteristics
| User Role / Persona | Technical Proficiency | Core Responsibilities & Rights |
| :--- | :--- | :--- |
| System Administrator / Data Scientist | High (Python / ML / DB Management) | Dataset updates, model retraining and hyperparameter calibration, feature engineering configuration, and deployment management. |
| Agricultural Analyst / Policy Researcher | Intermediate (Domain Analyst) | Cross-mandi price spread inspection, long-term volatility analysis, weather-impact correlation study, and summary report generation. |
| Farmer / Trader / General User | Basic (Web Browser User) | Commodity-specific price lookups, next-day price forecast queries, market arrival monitoring, and local mandi comparisons. |

### 2.3 Operating Environment
* **Client Requirements:** Modern web browser (Google Chrome >= v110, Mozilla Firefox >= v108, Edge, Safari); minimum display resolution 1366x768 for desktop, responsive view down to 360x640.
* **Server Runtime Environment:** Linux (Ubuntu 22.04 LTS), macOS, or Windows 10/11; Python 3.10 - 3.13 virtual environment.
* **Database Storage Tier:** Columnar Apache Parquet engine (`pyarrow` / `fastparquet`) and structured CSV tabular repositories for aggregations.

### 2.4 Design and Implementation Constraints
* **Academic Budget Constraint:** Built entirely on open-source libraries (Python, Streamlit, Pandas, Plotly, Scikit-learn, XGBoost, CatBoost) to ensure zero licensing cost.
* **Memory & Scalability Constraint:** In-memory processing of 4.7M rows requires optimized columnar Parquet filtering and cached pre-computed summaries to ensure sub-2-second dashboard response times.
* **Inference Horizon Constraint:** Predictive modeling is strictly calibrated for next-day modal price forecast based on available 1-day price lags and daily meteorological indicators.
* **Modularity Standards:** Strict modular separation between data loading (`data_loader.py`), model serving (`model_loader.py`), reusable components (`ui_components.py`), and dedicated analytics pages (`pages/*.py`).

### 2.5 Assumptions and Dependencies
* **Assumptions:** Input historical records conform to standardized Agmarknet schema (State, District, Market, Commodity, Variety, Grade, Arrival_Date, Prices); client machine supports WebGL for interactive Plotly charts.
* **Dependencies:** Availability of standard Python scientific stack (Python >= 3.10, Streamlit, Pandas, NumPy, Scikit-learn, XGBoost, CatBoost, Plotly, PyArrow, Joblib).

---

## 3. System Features and Functional Requirements

### 3.1 Module 1: Market Intelligence & Historical Analysis
| Req ID | Feature Description | Input / Validation Rule | Priority |
| :--- | :--- | :--- | :--- |
| FR-1.1 | National Market Overview & KPIs | Computes total transaction volume, active mandis, represented states, and average modal price across 2024. | High |
| FR-1.2 | State & District Price Comparison | User selects State/District; system visualizes regional price variations and mandi density. | High |
| FR-1.3 | Commodity Price Spread & Volatility | Commodity dropdown; renders time-series price spreads (Min, Max, Modal prices) over 12 months. | High |

### 3.2 Module 2: Weather Correlation & ML Forecasting Engine
| Req ID | Feature Description | Input / Validation Rule | Priority |
| :--- | :--- | :--- | :--- |
| FR-2.1 | Agrometeorological Correlation Analysis | Select weather parameters (Rainfall, Temp, Wind, Pressure) and commodity; generates scatter plots and correlation coefficients. | Medium |
| FR-2.2 | Machine Learning Next-Day Price Prediction | Inputs: Market, Commodity, Variety, Grade, current modal price, and weather factors; executes selected ML model to output predicted price. | High |
| FR-2.3 | Comparative Model Evaluation Matrix | Visualizes benchmark metrics (MAE, RMSE, R², Training Duration) comparing Linear Regression, Random Forest, XGBoost, and CatBoost against Naive Baseline. | High |

### 3.3 Module 3: Reporting, Visualization & Data Explorer
| Req ID | Feature Description | Input / Validation Rule | Priority |
| :--- | :--- | :--- | :--- |
| FR-3.1 | Interactive Multi-Faceted Data Explorer | Allows multi-column slicing (State, Commodity, Date Range, Price Thresholds) with dynamic data table rendering. | High |
| FR-3.2 | Dataset Export Capabilities | Generates filtered subsets and summary tables downloadable as standard CSV files. | Medium |
| FR-3.3 | Insight Generation & Summary Banners | Automated natural language summary generation for market extremes, high-volatility commodities, and weather anomalies. | Low |

---

## 4. External Interface Requirements

### 4.1 User Interfaces (UI)
The user interface is implemented via Streamlit, providing an intuitive multi-page layout with a persistent sidebar:
1. **Overview:** National macro KPIs, price distribution histograms, and monthly trade movements.
2. **Market Analysis:** Spatial market comparisons, district spreads, and trade density maps.
3. **Commodity Analysis:** Volatility rankings, top commodities by volume, and price range envelopes.
4. **Weather & Price:** Rainfall vs. price shifts, temperature impact scatter analysis, and seasonal trends.
5. **Price Forecast:** Interactive prediction console with model selector, scenario adjustment, and forecast confidence.
6. **Model Performance:** Diagnostic bar charts, error distribution, and academic benchmark leaderboard.
7. **Data Explorer:** Paginated tabular viewer with search, sort, filter, and CSV download.

### 4.2 Hardware Interfaces
* **Standard Deployment:** Standard workstation / PC with keyboard, mouse, and display resolution >= 720p (1080p recommended).
* **Processing Resources:** Minimum 8 GB system RAM and multi-core CPU (Intel i5/AMD Ryzen 5 or Apple Silicon) for efficient parquet querying and model inference.

### 4.3 Software Interfaces
* **Runtime & Language:** Python 3.10 - 3.13.
* **Data Engine:** Apache PyArrow & Pandas for vectorized data manipulation.
* **Machine Learning Libraries:** Scikit-learn (Linear Regression, Random Forest, Preprocessors), XGBoost, CatBoost, and Joblib serialization.
* **Visualization Engine:** Plotly Graph Objects & Plotly Express for client-side responsive SVG/WebGL charts.

### 4.4 Communication Interfaces
* **Protocol:** HTTP/1.1 and WebSockets (TCP/IP) on standard port 8501 for bi-directional state synchronization between browser and Streamlit backend.
* **Data Serialization:** UTF-8 encoded JSON and Arrow binary buffers for tabular data serialization.

---

## 5. Non-Functional Requirements (NFRs)
| Attribute | Target Metric / Standard | Verification & Testing Method |
| :--- | :--- | :--- |
| 5.1 Performance | Initial app launch < 3.0s; page transition < 1.5s; single prediction inference < 200ms. | Streamlit execution profiler, browser DevTools Network/Performance auditing. |
| 5.2 Security | Strict local filesystem sandboxing; input validation on all user filter parameters to prevent buffer/type errors; zero external exposure of proprietary model weights. | Static code analysis, code review, and edge-case boundary testing. |
| 5.3 Reliability | Application uptime >= 99% during demonstration; graceful fallback error banners for unsupported commodity-mandi combinations. | Exception handling stress-testing with unobserved feature values. |
| 5.4 Portability | Cross-platform operation across macOS (ARM64/x86_64), Linux, and Windows; compatible with Chrome, Safari, Firefox, and Edge. | Cross-browser testing and multi-OS deployment verification. |

---

## 6. System Design and Analysis Models

### 6.1 Use Case Model
```text
[ Use Case Specification ]

Actors:
  1. Farmer / Mandi Trader (General User)
  2. Agricultural Market Analyst
  3. Academic Evaluator / Data Scientist

Use Cases:
  - UC-01: View National Market Overview & KPIs (Actors: 1, 2, 3)
  - UC-02: Compare Mandi & Commodity Price Spreads (Actors: 1, 2)
  - UC-03: Analyze Weather vs. Price Correlation (Actors: 2, 3)
  - UC-04: Execute Next-Day Price Forecast (Actors: 1, 2, 3)
  - UC-05: Inspect ML Benchmark & Model Leaderboard (Actors: 2, 3)
  - UC-06: Filter and Export Custom Subsets (Actors: 2, 3)
```

### 6.2 Data Flow Diagram (DFD Level 1)
```text
[ DFD Level 1: Subsystem Information Flow ]

[User Query / Filters]
        |
        v
(1.0 Ingestion & Caching) <=== [Parquet Data Store (4.7M rows)]
        |
        +---> [Filtered DataFrame] ---> (2.0 Market Analytics) ---> [Plotly Interactive Charts]
        |
        +---> [Weather & Price Feats] -> (3.0 Agrometeorology) --> [Correlation Matrix View]
        |
        +---> [Series Feature Vector] -> (4.0 ML Inference Engine) <=== [Trained Models (XGB/Cat/RF)]
                                                    |
                                                    v
                                      [Predicted Next-Day Modal Price]
```

### 6.3 Entity-Relationship & Schema Specification
| Entity Name | Key Attributes | Description |
| :--- | :--- | :--- |
| MarketRecord | Arrival_Date, State, District, Market, Commodity, Variety, Grade, Min_Price, Max_Price, Modal_Price | Daily mandi transaction records gathered across Indian APMC markets. |
| WeatherObservation | nearest_station, station_latitude, station_longitude, distance_km, avg_temp, min_temp, max_temp, wind_speed, air_pressure, rainfall | Meteorological observations mapped to corresponding mandi locations and dates. |
| ModelBenchmark | Model, MAE, RMSE, R2, Training_Rows, Training_Time_Min | Evaluation metrics capturing empirical validation across all machine learning algorithms. |

### 6.4 Activity / Sequence Flow for Price Forecast
```text
User (Browser)               Streamlit Controller             Model Loader             ML Model
     |                                |                            |                      |
     |--- 1. Select State/Commodity ->|                            |                      |
     |--- 2. Input Weather/Lag Price->|                            |                      |
     |                                |-- 3. Assemble Feature Vec ->|                      |
     |                                |                            |-- 4. Load Artifact ->|
     |                                |                            |                      |-- 5. Predict(X)
     |                                |                            |<- 6. Return Float ---|
     |                                |<- 7. Return Prediction ----|                      |
     |<-- 8. Render KPI & Forecast ---|                            |                      |
```

---

## 7. Academic Review & Sign-Off
This Software Requirements Specification document has been submitted and reviewed by the academic supervisory panel:

| Project Coordinator / Guide | Internal Examiner | Head of Department (HOD) |
| :--- | :--- | :--- |
| Signature: _______________________<br><br>Date: ___________________________ | Signature: _______________________<br><br>Date: ___________________________ | Signature: _______________________<br><br>Date: ___________________________ |
