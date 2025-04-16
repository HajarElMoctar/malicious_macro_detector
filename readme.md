# 🧠 Malicious Word Macro Detector

A smart AI-powered tool to detect, analyze, and explain potential threats in Microsoft Word documents containing VBA macros.

---

## 📦 Features

- 🔍 **Static Analysis**
  - Scans `.doc` and `.docm` files for embedded VBA macros
  - Flags suspicious keywords like `Shell`, `WScript`, `CreateObject`, etc.
  - Scores severity of macros based on keyword patterns

- 🧪 **Dynamic Analysis**
  - Uses **Hybrid Analysis** sandbox to execute and observe real-time macro behavior
  - Fetches verdict, threat score, behavior classification, and report link

- 🤖 **AI-Powered Summary & Chatbot**
  - Summarizes the static & dynamic results using **Azure OpenAI (GPT-4)**
  - Supports a persistent session chat for follow-up questions
  - Offers smart suggestions for user queries

- 📄 **PDF Report Generator**
  - Exports combined summary and chat history into a downloadable, readable report
  - Built with ReportLab for layout integrity

- 🧩 **Drag-and-Drop UI**
  - Modern Bootstrap-based interface
  - Easy toggling between static and dynamic analysis
  - Real-time response and report download

---

## 🚀 How It Works

### 📁 1. Upload a `.doc` or `.docm` file
- Drag and drop into the UI
- File is saved and scanned for embedded macros

### 🧠 2. AI Summarization
- Extracted code and behavioral info are sent to GPT-4 (Azure OpenAI)
- A detailed natural language report is generated

### 💬 3. Follow-Up Chat
- Ask the AI questions like:
  - "Is this macro dangerous?"
  - "What kind of payload is used?"
  - "How can I remove it?"

### 🧾 4. Export Your Report
- Download the full AI report + chat log as a well-formatted PDF

---

## 🛠️ Setup Instructions

### ✅ Requirements
- Python 3.10+
- An [Azure OpenAI](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/) account with deployment setup
- A [Hybrid Analysis](https://www.hybrid-analysis.com/) API key

### 📁 Folder Structure
```
macro_detector/
├── app.py
├── .env
├── static/
│   └── main.js
├── templates/
│   └── index.html
├── analysis/
│   ├── static_analysis.py
│   ├── dynamic_analysis.py
│   ├── threat_score.py
│   └── report_generator.py
└── openai_api.py
```

### ⚙️ .env File Example

AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_API_VERSION=2023-12-01
HYBRID_API_KEY=your_hybrid_analysis_api_key


### ▶️ Run the App

# Create virtual environment (optional)
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Start the Flask app
python app.py


---

## 🧪 Hybrid Analysis Notes
- Environment ID used: `160` (Windows 10 64-bit)
- Analysis can take up to 10 minutes
- If the file was already submitted, the system fetches the existing report using SHA256
- Public report link is included in the output

---

## 📌 Key Technologies
- **Flask** – Backend server
- **Bootstrap 5** – Frontend UI
- **Azure OpenAI (ChatGPT 4)** – Natural language analysis
- **Hybrid Analysis API** – Dynamic sandboxing
- **ReportLab** – PDF generation

---

## 📷 UI Preview

Main Page:

![macro detector main page](https://github.com/user-attachments/assets/2533a33a-0cae-4483-8901-5c98d7ac5a3e)

After dropping a document (analysing):

![macro detector analysing](https://github.com/user-attachments/assets/a0f9da00-ccbe-449c-90da-456b3762cd60)

Report Results:

![macro detector results](https://github.com/user-attachments/assets/0fc29f6b-fc98-4471-9b16-50d9bb08d0a9)

Chat Box:

![macro detector chat box](https://github.com/user-attachments/assets/5a9274ca-856b-4286-ac9a-f12246e47802)

AI Chat Response: 

![macro detector chat response](https://github.com/user-attachments/assets/16c541a1-9c0c-4321-9a7b-badbd5db9b06)

Sample PDF Report downloaded:

![macro detector sample pdf](https://github.com/user-attachments/assets/381c72df-252b-41dd-807c-6d3dd572422a)

---

## 🙌 Acknowledgments
- Hybrid Analysis by CrowdStrike
- Azure OpenAI team
- Python and Flask contributors

---

## 📄 License

---

## 📬 Contact
Feel free to reach out for collaboration, feedback, or questions:
**Authors**: Hajar El Moctar, Sara Idris, Nada Maarafiya 


