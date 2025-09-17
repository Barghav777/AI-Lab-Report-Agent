# 🔬 AI Lab Report Agent

## 👤 Author Information
- **Name:** D Barghav
- **University:** IIT, Jammu 
- **Department:** Mechanical Engineering
- **Email:** 2023UME0253@iitjammu.ac.in
- **GitHub:** [Barghav777](https://github.com/Barghav777)  
- **LinkedIn:** [Barghav Dhamodharan](https://www.linkedin.com/in/barghav-dhamodharan-11892a321/)  


This project is an **AI agent** built as a web application to automate the creation of scientific lab reports. It takes a lab manual and experimental observations as input and generates a complete, structured report.

## ✨ Features

-   **Web-Based UI:** A simple and clean user interface built with Flask for uploading lab manuals and entering observation data.
-   **RAG for Context:** Uses a Retrieval-Augmented Generation (RAG) pipeline with FAISS to extract the Aim, Theory, and Procedure from the provided lab manual.
-   **AI Code Generation:** A fine-tuned `microsoft/Phi-3-mini` model, accessed via the Hugging Face API, generates Python code for performing calculations based on observations.
-   **Automated Calculations:** The generated Python code is executed in a sandboxed environment to produce the final numerical results for the report.
-   **High-Speed Report Writing:** The final report is synthesized using the powerful `Llama3` model, accessed via the high-speed Groq API.
-   **Built-in Evaluation:** A complete evaluation suite is included to score the **agent's** report quality using ROUGE metrics.

---
## ⚙️ Project Workflow

The **AI agent** follows a five-step pipeline to generate a report:

1.  **Input:** The user uploads a lab manual (PDF, DOCX) and provides experimental observations in JSON format through the web interface.
2.  **RAG Context Retrieval:** The text is extracted from the manual. A LangChain and FAISS vector store is built in memory to find and retrieve the most relevant sections (Aim, Theory, etc.).
3.  **Code Generation:** A fine-tuned `Phi-3` model (via Hugging Face API) writes Python code for calculations.
4.  **Execution:** The code is executed to get numerical results.
5.  **Final Report Generation:** The RAG context, user observations, and calculated results are combined into a final prompt and sent to the Llama 3 model via the Groq API, which writes the complete, structured lab report.

---
## 🛠️ Tech Stack

-   **Backend:** Python, Flask
-   **Frontend:** HTML, CSS, JavaScript
-   **AI Orchestration:** LangChain
-   **Vector Store:** FAISS
-   **LLM APIs:**
    -   Hugging Face Inference API (for the fine-tuned coder model)
    -   Groq API (for the final report writer)
-   **Core AI Libraries:** PyTorch, Transformers

---
## 🚀 Getting Started

### 1. Prerequisites
-   Python 3.11+
-   A Hugging Face account and API Token
-   A Groq account and API Key

### 2. Installation
1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd LabReportAgent
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    # Windows
    python -m venv .venv
    .\\.venv\\Scripts\\Activate.ps1
    ```
3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### 3. Configuration
1.  Create a file named `.env` in the root of the project directory (`LabReportAgent/`).
2.  Add your API keys to the `.env` file:
    ```
    GROQ_API_KEY='gsk_YourGroqApiKey'
    HF_API_TOKEN='hf_YourHuggingFaceApiToken'
    ```

---
## ▶️ Usage

1.  **Run the Flask Application:**
    ```bash
    python run.py
    ```
2.  **Open the Web Interface:** Navigate to `http://127.0.0.1:5000` in your web browser.
3.  **Upload and Enter Data:**
    -   Click to upload your lab manual.
    -   Paste your experimental observations in the text area in JSON format.
    -   Click "Generate Report."

---
## 📊 Evaluation

The project includes a suite to quantitatively measure the quality of the generated reports.

1.  **Prepare the Dataset:**
    -   Open the `evaluation/eval_dataset.jsonl` file.
    -   This file contains sample experiments. For each line, you **must** update the `manual_path` to point to the correct location of your lab manual files on your local machine.

2.  **Run the Evaluation Script:**
    Make sure your virtual environment is activated and you are in the project's root directory.
    ```bash
    python -m evaluation.evaluate
    ```

3.  **Review the Results:**
    -   A summary of the average **ROUGE-1** and **ROUGE-L** scores will be printed in the terminal.
    -   A new folder, `evaluation/evaluation_results/`, will be created. Inside, a timestamped `.txt` file will contain a detailed, side-by-side comparison of the generated reports and the "golden" reference reports for manual analysis.
