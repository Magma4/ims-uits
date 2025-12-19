# IMS-UITS
**Inventory Management System (Internal Tool)**

## Overview
IMS-UITS is a Django-based internal inventory management system designed to track organizational assets and handle employee equipment requests. The application centralizes inventory control, request approvals, asset lifecycle tracking (released vs returned), and administrative reporting.

This project was built to solve a real operational problem: **managing shared equipment securely and transparently within an organization**.

> Note: The system is intended for internal use and is typically deployed within a local network to protect sensitive asset data.

---

## Problem This Project Solves
Manual inventory tracking using spreadsheets made it difficult to:
- Know current stock availability
- Track which employee had which item
- Enforce return deadlines
- Generate reliable audit reports

IMS-UITS replaces these workflows with a structured, role-based web application.

---

## Core Features

### Inventory & Asset Tracking
- CRUD management for inventory items
- Automatic quantity updates on release and return
- Detailed asset metadata storage

### Request & Approval Workflow
- Employees submit equipment requests
- Admins approve, release, and receive returned items
- Real-time request status updates (`Pending`, `Released`, `Returned`)
- Automatic overdue item detection

### Dashboard & Reporting
- Admin dashboard with key metrics and alerts
- Search and filter requests by user, item, status, or date
- Export reports to **Excel (.xlsx)** and **PDF**

### Notifications & Access Control
- Automated email reminders for overdue assets
- Role-based permissions:
  - Superusers
  - Sub-admins
  - Employees

---

## Technical Implementation

**Backend**
- Python 3.x
- Django 5.x
- Modular Django apps with clear separation of concerns

**Database**
- SQLite (local deployment)

**Frontend**
- Bootstrap 4
- JavaScript

**Async & Background Tasks**
- Celery for email notifications and background processing

**Reporting**
- `openpyxl` for Excel exports
- `reportlab` for PDF generation

---

## What I Built
- Designed the data models for inventory items, requests, and user roles
- Implemented the full request lifecycle (approve, release, return)
- Built role-based access control for admins and employees
- Developed exportable reporting features (Excel and PDF)
- Integrated background tasks for automated email reminders


---

## 🚀 Running Locally

### Prerequisites
- Python 3.10+
- `pip`

### Setup
```bash
git clone <internal-repo-url>/ims-uits.git
cd ims-uits
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
