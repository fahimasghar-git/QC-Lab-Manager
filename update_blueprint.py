path = '/Users/fahimasghar/.gemini/antigravity/brain/92c2e6e3-0cd4-4132-971d-a7f129b6d815/iso17025_lims_blueprint.md'

content = """# 🏗️ Vital Agri Nutrients - ISO 17025 LIMS Blueprint

This document tracks the digital transformation of the physical ISO 17025 QMS into the Django LIMS application.

## 📐 Core Architectural Principles
1. **1:1 Data Entry Rule:** Every field or signature line visible on a physical ISO printout MUST have a corresponding data entry field in the Django Admin backend.
2. **Digital Chain of Approval:** All forms requiring signatures (Prepared By, Checked By, Approved By) will eventually utilize a digital approval workflow (Admin Actions) where the logged-in user clicks 'Approve', capturing their timestamp and name, similar to the Sample/CoA verification workflow.
3. **Template Standardization:** All ISO printable forms use `xhtml2pdf` generating standardized A4/Landscape PDFs containing a Master Document Control header (Format No, Revision No, Issue Date, Page No) and the standalone Corporate Logo (PNAC logo exclusively on CoA).

## 📊 Forms Digitization Status

> **Total Forms Tracked:** 27
> **Fully Digitized:** 15 (55%)
> **Pending:** 12 (45%)

---

### ✅ Fully Completed (Backend + Printable Forms)
*These forms have been completely digitized. The data is managed in the database, and the system can generate a pixel-perfect ISO-compliant PDF.*

**Clause 5 & 6 (Structural & Resource Requirements)**
- [x] **QCL-FRM-1.04** - Competency Monitoring of Laboratory Personnel (Resources Module)
- [x] **QCL-FRM-2.09** - Evaluation of Competency (Resources Module)
- [x] **QCL-FRM-4.02** - Master List of Equipments (Resources Module)
- [x] **QCL-FRM-4.03** - Equipment Maintenance Record (Resources Module)
- [x] **QCL-FRM-4.04** - Calibration Program (Resources Module)
- [x] **QCL-FRM-5.01** - CRM List (Metrological Traceability / ReagentStandards)

**Clause 6.6 (External Providers & Purchasing)**
- [x] **QCL-FRM-6.01** - Supplier Selection Form
- [x] **QCL-FRM-6.02** - Approved Supplier / Service Provider List
- [x] **QCL-FRM-6.03** - External Provider Evaluation & Re-evaluation Form
- [x] **QCL-FRM-6.04** - Supplier Performance Monitoring
- [x] **QCL-FRM-6.07** - Store Purchase Demand
- [x] **QCL-FRM-6.08** - Products/Services Inspection Form (RM Checking)

**Clause 7 (Process Requirements - Samples)**
- [x] **QCL-FRM-12.01** - Analysis Request
- [x] **QCL-FRM-12.03** - Certificate of Analysis

**Clause 8 (Management System - Non-Conformance)**
- [x] **QCL-FRM-14.01** - Non-Conformance Form

---

### 📝 Pending Digitization
*These forms are currently sitting in the ISO 17025 folder and have not yet been mapped into the LIMS.*

**Clause 6.2 (Personnel Authorizations)**
- [ ] **QCL-FRM-1.01** - Personnel Authorization Permit
- [ ] **QCL-FRM-1.02** - List of Authorized Staff

**Clause 6.6 (External Providers & Purchasing)**
- [ ] **QCL-FRM-6.05** - Comparative Statement
- [ ] **QCL-FRM-6.06** - Supplier Evaluation Plan

**Clause 8.7 (Non-Conformances & Corrective Actions)**
- [ ] **QCL-FRM-14.02** - Non-Conformance Log *(Can be derived from existing NC DB)*
- [ ] **QCL-FRM-14.03** - Root Cause Analysis Form

**Clause 7 & 8 (Process & Quality Assurance)**
- [ ] **QCL-FRM-17.14** - Lab Cleaning Inspection Sheet
- [ ] **QCL-FRM-19.01** - Assignment, Summary and Review Form
- [ ] **QCL-FRM-20.01** - Master List of Records
- [ ] **QCL-FRM-20.02** - Master List of Files and Folders
- [ ] **QCL-FRM-21.01** - Customer Feedback Form
- [ ] **QCL-FRM-22.01** - Sample Return Form

---

## 🛠️ Next Steps

1. **Finish Clause 6.6:** Digitize the final two purchasing forms (QCL-FRM-6.05 Comparative Statement, QCL-FRM-6.06 Supplier Evaluation Plan).
2. **Audits & Non-Conformance:** Expand the existing NC models to generate the 14.02 Log and 14.03 Root Cause Analysis standalone forms.
3. **Personnel & Authorization:** Build out the Personnel Authorization (1.01, 1.02) tracking.
"""

with open(path, 'w') as f:
    f.write(content)

print("Blueprint completely rewritten and updated.")
