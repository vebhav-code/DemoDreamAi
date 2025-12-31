# How to Run DemoDream Backend

## 1. Prerequisites
Ensure you have Python installed. You also need the following libraries:
```bash
pip install -r requirements.txt
```

## 2. Start the AI Engine (Backend)
Open your terminal (Command Prompt or PowerShell) and run these commands:

1. Navigate to the backend folder:
   ```powershell
   cd Ai_Engine
   ```

2. Run the server:
   ```powershell
   uvicorn main:app --reload
   ```
   *You should see output saying "Application startup complete".*

## 3. Start the AI Model (Ollama)
In a **separate** terminal window, ensure your AI model is running:
```powershell
ollama run gemma3:1b
```

## 4. Access the Website
Open `DemoDream/index.html` in your browser.
