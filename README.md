#  Autonomous Insurance Claims Processing Agent

## Overview


This project implements a lightweight **Autonomous Insurance Claims Processing Agent** that processes FNOL (First Notice of Loss) documents.  
The agent extracts structured information from unstructured text, validates required fields, classifies the claim, and routes it to the appropriate workflow based on predefined business rules.

---

## 🎯 Problem Statement

Insurance companies receive large volumes of FNOL documents that must be processed quickly and accurately. Manual processing is time-consuming and error-prone.

This project automates:

* Data extraction
* Validation of mandatory fields
* Claim classification
* Intelligent routing
* Reason generation for decisions

---

## ⚙️ Features

### ✅ 1. Field Extraction

Extracts key information from FNOL text:

* **Policy Information**

  * Policy Number
  * Policyholder Name
  * Effective Dates
* **Incident Information**

  * Date
  * Time
  * Location
  * Description
* **Involved Parties**

  * Claimant
  * Third Parties
  * Contact Details
* **Asset Details**

  * Asset Type
  * Asset ID (VIN)
  * Estimated Damage
* **Other Fields**

  * Claim Type
  * Attachments
  * Initial Estimate

---

### ✅ 2. Missing Field Detection

Identifies missing mandatory fields such as:

* Policy Number
* Policyholder Name
* Incident Date
* Incident Location
* Claim Type
* Initial Estimate


---

## 🧠 System Architecture

```
Raw FNOL Text
      ↓
Field Extraction (Regex)
      ↓
Data Cleaning
      ↓
Validation (Missing Fields)
      ↓
Claim Classification
      ↓
Rule Engine (Routing)
      ↓
JSON Output
```

---

## 🛠️ Tech Stack

* Python 3
* Regular Expressions (`re`)
* JSON processing

---

## 📂 Project Structure

```
├── main.py          # Core agent logic
├── README.md        # Project documentation
├── requirements.txt
```

---

## ▶️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/Shiwam-m/Autonomous-Insurance-Claims-Processing-Agent-2-
cd Autonomous Insurance Claims Agent
```

### 2. Run the script

```bash
python main.py
```

---

## 📄 Sample Input

```
AUTOMOBILE LOSS NOTICE
POLICY NUMBER: ABC-123456
NAME OF INSURED John Doe
DATE OF LOSS AND TIME 04/15/2026 10:30 AM
STREET: 123 Maple Avenue CITY: Springfield
DESCRIPTION OF ACCIDENT: Rear-end collision. No fraud.
ESTIMATE AMOUNT: 4500
V.I.N.: 1HGCM82635A
```

---

## 📤 Sample Output

```json
{
  "extractedFields": {
    "policy_number": "ABC-123456",
    "policyholder_name": "John Doe",
    "incident_date": "04/15/2026",
    "incident_time": "10:30 AM",
    "incident_location": "123 Maple Avenue",
    "incident_description": "Rear-end collision. No fraud.",
    "estimated_damage": "4500",
    "initial_estimate": 4500.0,
    "claim_type": "property_damage"
  },
  "missingFields": [],
  "recommendedRoute": "Fast-track",
  "reasoning": "Damage estimate $4500.0 is below threshold."
}
```

---

## 📌 Conclusion

This project demonstrates how rule-based AI systems can automate insurance claim processing, reduce manual effort, and improve decision-making efficiency while maintaining explainability.
