# Technical Documentation: ITD (Insider Threat Detection) Platform

## 1. System Overview
The **Insider Threat Detection (ITD) Platform** is a dual-interface security solution designed to monitor, detect, and mitigate internal organizational threats in real-time. It combines a high-fidelity **Security Operations Center (SOC)** for administrators with a stealthy **Employee Portal** (branded as PORTAL/NEXUS) to provide end-to-end telemetry and forensic analysis.

---

## 2. Technical Architecture
The system follows a modular **Micro-Monolith architecture** built on Flask, utilizing a real-time ingestion pipeline and a multi-model ML engine.

### Core Components:
*   **Ingestion Layer:** Uses `Watchdog` and `SocketIO` for real-time monitoring of file system events and user activity.
*   **Detection Engine:** A multi-layered ML system featuring **Isolation Forest**, **LOF (Local Outlier Factor)**, and **One-Class SVM** for anomaly detection.
*   **Forensic Module:** Automated snapshot generator that captures system state and evidence when high-risk behavior is detected.
*   **Identity Layer:** Rigid RBAC (Role-Based Access Control) with Zero-Trust principles.

---

## 3. Technology Stack
*   **Backend:** Python 3.x, Flask (Web Framework).
*   **Database:** SQLite / SQLAlchemy (ORM) for structured logs and forensic records.
*   **Real-time:** Flask-SocketIO (WebSockets) for live alert piping.
*   **ML/AI:** Scikit-learn (Isolation Forest, SVM), NumPy, Pandas.
*   **Frontend:** Vanilla Javascript, CSS3 (Premium GenZ AI Theme), HTML5 (Semantic).
*   **Forensics:** Custom FPDF/ReportLab logic for forensic PDF generation.

---

## 4. Machine Learning Implementation
### Dataset & Training
*   **Dataset:** High-fidelity **Synthetic Behavior Dataset** modeled after CMU CERT v4.2 patterns.
*   **Training Baseline:** 100+ "Normal Workday" samples (9:00-17:00, Mon-Fri).
*   **Anomalies:** Injected outliers including time-of-day violations, mass file access, and privilege escalation attempts.

### Multi-Model Voting System:
1.  **Isolation Forest:** Primary model for detecting global anomalies in activity timestamps and types.
2.  **One-Class SVM:** Secondary validation for behavior boundary checking.
3.  **LSTM Sequence Logic (Simulated):** Analyzes chronological event chains (e.g., `cron_mod` -> `file_access` -> `sudo`) to detect multi-stage attack precursors like Logic Bombs.

---

## 5. Security Features
*   **Automated Kill Switch:** Instant session revocation and user suspension for High-Severity alerts (excluding Super Admins).
*   **Forensic Snapshots:** Every high-risk alert triggers a **Chain of Custody** forensic report containing user metadata, IP addresses, and activity timestamps.
*   **Real-time Telemetry:** Filesystem monitoring via `realtime_agent.py` which tracks all CRUD operations in secure directories.
*   **XAI (Explainable AI):** Every alert includes a "Model Explanation" detailing exactly why the activity was flagged (e.g., "Out-of-hours activity detected" or "Anomalous sequence detected").

---

## 6. Design System (Aesthetic Specifications)
The platform utilizes a **GenZ AI / Stealth Aesthetic**:
*   **Theme:** Dark Mode (Obsidian Base: `#050505`).
*   **Accents:** Neon Violet (`#8b5cf6`) and Cyber Cyan (`#06b6d4`) gradients.
*   **Components:** 
    *   **Glassmorphism:** 20px Backdrop Blur on cards and sidebars.
    *   **Typography:** Plus Jakarta Sans (Main), Space Grotesk (Headers), JetBrains Mono (Forensic logs).
    *   **Transitions:** 0.3s cubic-bezier easing on all interactive elements.

---

## 7. Functional Endpoints
*   **SOC Core (`/dashboard`):** Real-time activity stream, alert management, and forensic vault access.
*   **Employee Portal (`/portal`):** Productivity-focused view of files and personal activity, designed to mask monitoring systems.
*   **Incident Response (`/alerts`):** Interface for investigators to review, update, or delete detected incidents.
