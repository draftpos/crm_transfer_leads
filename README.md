# CRM Lead Transfer & User Offboarding (crm_transfer_user_disable)

[![Odoo Version](https://img.shields.io/badge/Odoo-17.0%20%7C%2018.0-714B67?logo=odoo&logoColor=white)](https://www.odoo.com)
[![License: LGPL-3](https://img.shields.io/badge/License-LGPL--3-blue.svg)](LICENSE)
[![Category](https://img.shields.io/badge/Category-Sales%2FCRM-orange.svg)]()
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()

> **Seamless Lead Ownership Reassignment, Team Territory Restructuring & Safe User Offboarding with Zero Lead Loss.**

---

## 📌 Overview

**CRM Lead Transfer & User Offboarding** provides enterprise sales operations with the tools needed to manage sales representative turnover, reassignment, and team restructurings. It ensures that when sales reps depart or shift territories, 100% of their active leads and history are safely migrated to new owners without data loss or broken activity links.

---

## ✨ Key Features

### 1. 🔄 Interactive Lead Transfer Wizard
- **Source & Destination Matching**: Select source sales rep and target sales rep with real-time lead count previews.
- **Selective or Full Transfer**: Reassign all leads or filter by stages, teams, or territories.
- **Smart Team Sync**: Automatically aligns sales team attribution to match the new representative.

### 2. 🛡️ Safe User Offboarding & Archiving
- **1-Click Transfer & Disable**: Reassign all active pipeline leads and immediately archive/disable the departing user's Odoo login credentials in one atomic transaction.
- **Zero Orphaned Leads**: Guarantees no lead is left unassigned or assigned to a deactivated user.

### 3. 📝 Complete Audit Chatter Trail
- **Activity Preservation**: Retains complete history, past chatters, notes, and attachments without altering historical creation dates.
- **Audit Logging**: Adds an explicit audit log entry detailing who initiated the transfer, the previous owner, and the transfer timestamp.

### 4. 👥 Active Salesperson Dynamic Filtering
- Context-aware domain filters ensure users only select active representatives who currently manage leads, eliminating dropdown clutter.

---

## 🚀 Installation & Setup

1. **Clone or Copy** this addon into your Odoo custom addons directory:
   ```bash
   git clone git@github.com:draftpos/crm_transfer_leads.git crm_transfer_user_disable
   ```
2. **Update Addons List**:
   - Activate Developer Mode (`Settings` -> `General Settings` -> `Activate Developer Mode`).
   - Navigate to `Apps` -> `Update Apps List`.
3. **Install the Module**:
   - Search for **CRM Transfer Leads & User Disable** (`crm_transfer_user_disable`).
   - Click **Install** or **Upgrade**.

---

## 📁 Technical Information

| Attribute | Value |
|---|---|
| **Technical Name** | `crm_transfer_user_disable` |
| **Category** | Sales/CRM |
| **Odoo Compatibility** | Odoo 17.0+ & Odoo 18.0+ |
| **Dependencies** | `crm`, `mail` |
| **License** | LGPL-3 |
| **Author** | DraftPOS & Havano Solutions |

---

## 📄 License

This module is licensed under the **GNU Lesser General Public License v3.0 (LGPL-3)**. See the [LICENSE](LICENSE) file for details.
