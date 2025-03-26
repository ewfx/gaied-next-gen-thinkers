# 🚀 Email Classifications for Loan Servicing Platform


## 📌 Table of Contents
- [Introduction](#introduction)
- [Demo](#demo)
- [Inspiration](#inspiration)
- [What It Does](#what-it-does)
- [How We Built It](#how-we-built-it)
- [Challenges We Faced](#challenges-we-faced)
- [How to Run](#how-to-run)
- [Tech Stack](#tech-stack)
- [Team](#team)

---

## 🎯 Introduction
This project leverages Generative AI and OCR to classify emails and extract key information for a loan servicing platform. It automates the processing of incoming service requests, reducing manual effort and improving turnaround time.

## 🎥 Demo
🔗 [Live Demo](#) (if applicable)  
📹 [Video Demo](#)
[Video1]<video controls src="artifacts/demo/demo_1_realtime_processing.mp4" title="Title"></video>
[Video2](artifacts/demo/demo_2_duplicate_handling.mkv)  
🖼️ Screenshots:

![Screenshot][Hackathon2025_snaps](artifacts/arch/Hachathon2025_snaps.docx)
![Flow Diagram][FlowDiagram](artifacts/arch/FlowDiagram.pptx)
![PPT](link-to-image)[PPT](artifacts/arch/Hackathon_PPT_Next_Gen_Thinkers_Final.pptx)

## 💡 Inspiration
Loan servicing platforms receive a high volume of customer emails, often containing critical service requests and attachments. Manually sorting and responding to these emails is time-consuming and prone to errors. This project automates the classification of emails and extraction of relevant data, enhancing efficiency and accuracy.

## ⚙️ What It Does
- Automatically classifies emails into predefined categories (e.g., Payment Inquiry, Loan Adjustment, Account Closure).
- Extracts relevant data from email bodies and attachments (PDFs, Word documents) using OCR.
- Identifies duplicate information from email forwards and replies, updating existing service requests if relevant (e.g., amount changes, deal name changes); otherwise, marking them as duplicates.
- Classifies emails based on priority, considering the email body first. If the body contains minimal information, attachments are prioritized for classification.
- Assigns confidence scores to classifications and handles cases where multiple classifications have equal scores.
- Enables seamless integration with loan servicing workflows.

## 🛠️ How We Built It
- Utilized Gemini AI models for text classification.
- Integrated OCR technology (Tesseract) for extracting text from attachments.
- Developed a pipeline to filter, classify, and extract email content efficiently.
- Implemented the solution using Gemini AI models, LangChain, OCR, Python, React and Material UI.
- Stored extracted data in a structured format for downstream processing.

## 🚧 Challenges We Faced
- Handling low-confidence classifications and ensuring accurate email routing.
- Processing large attachments efficiently without performance bottlenecks.
- Managing diverse email formats and unstructured text content.
- Ensuring security and compliance with data privacy regulations.

## 🏃 How to Run
1. Clone the repository  
   ```sh
   git clone https://github.com/ewfx/gaied-next-gen-thinkers
   ```
2. Install dependencies  
   ```sh
   npm install  # for react
   pip install -r requirements.txt # for Python
   configure IMAP # for testing our solution
   ```
3. Run the project  
   ```sh
   npm run dev  # for react UI
   python process_email.py # for python
   ```

## 🏗️ Tech Stack
- 🔹 Frontend: React, Material UI
- 🔹 Backend: Node.js
- 🔹 Database:
- 🔹 Other: Langchain, IMAP
- 🔹 AI & NLP: Gemini AI for text classification
- 🔹 OCR: Tesseract

## 👥 Team
- **Your Name** - NextGenThinkers
- **Teammate 2** - [GitHub](#) | [LinkedIn](#)
