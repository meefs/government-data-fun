# OpenGovDash - Open Government Data Dashboard

## 📌 About OpenGovDash
OpenGovDash is a lightweight web application that enables users to explore open government data from various federal agencies. It provides two main views:

1. **Agency View** – Browse data categorized by agencies (e.g., DOJ, SEC, NASA).
2. **Topic View** – Explore data sorted into topics like Cybersecurity, Healthcare, Elections, etc.

The application integrates OpenGov API and OpenAI API to enhance search functionality and context-based insights.

---

## 🚀 Getting Started

### Prerequisites
Ensure you have the following installed on your system:

- **Python 3.8+** (Backend)
- **Node.js 16+** (Frontend)
- **npm or yarn** (Package Manager)

---

## 🏗️ Installation

### **Step 1: Clone the Repository**
```bash
git clone https://github.com/your-repo/opengovdash.git
cd opengovdash
```

### **Step 2: Set Up Backend (Flask API)**
1. Navigate to the backend folder:
   ```bash
   cd api
   ```
2. Create a virtual environment (Optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set your API keys in an `.env` file (in the `api/` directory):
   ```
   OPENGOV_API_KEY=your_opengov_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```
5. Run the backend server:
   ```bash
   python app.py
   ```
   The API should now be running on `http://localhost:5000`.

---

### **Step 3: Set Up Frontend (React App)**
1. Open a new terminal and navigate to the frontend folder:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the frontend development server:
   ```bash
   npm start
   ```
4. Open your browser and visit `http://localhost:3000`.

---

## 🔑 Setting Up API Keys

To use OpenGovDash, you need API keys for:

1. **OpenGov API Key** – Get it from [api.data.gov](https://api.data.gov/signup/).
2. **OpenAI API Key** – Sign up at [OpenAI](https://platform.openai.com/signup/) and generate a key.

Once obtained, enter your API keys in the UI when prompted.

---

## 🖥️ How to Use OpenGovDash

### **1. Getting API Keys**
- Click the **"Get Started"** button on the homepage to set up API keys.
- Enter your OpenGov API Key and OpenAI API Key.
- Click **Save & Proceed**.

### **2. Exploring Data**
- **Agency View**: Click on an agency in the sidebar (e.g., DOJ, SEC, NASA) to see the latest 10 results.
- **Topic View**: Click on categories like Healthcare, Cybersecurity, or Elections to explore cross-agency data.
- Use **search and filter options** to refine your results.

### **3. Special Features**
- **DOJ Section**: Explore press releases, budget reports, and case filings separately.
- **SEC Section**: Search for a company using its **CIK (Central Index Key)** and fetch its latest **8-K, 10-K, 10-Q** filings.
- **NASA Section**: The background updates daily with the **APOD (Astronomy Picture of the Day)**.
- **AI Context Search**: Use OpenAI API to summarize and analyze selected datasets.

---

## 🛠️ Troubleshooting

### **Backend Issues**
❌ _Issue: `ModuleNotFoundError: No module named flask`_
✔️ **Fix**: Run `pip install -r requirements.txt`

❌ _Issue: `Error: API key is required`_
✔️ **Fix**: Add your API keys in `.env` and restart the server.

### **Frontend Issues**
❌ _Issue: `Module not found: Can't resolve 'react-router-dom'`_
✔️ **Fix**: Run `npm install react-router-dom` in the frontend folder.

❌ _Issue: `Module not found: Can't resolve 'axios'`_
✔️ **Fix**: We replaced `axios` with `fetch()`. Make sure you’re using the latest code.

---

## 🌐 Deploying OpenGovDash

### **Backend Deployment (Flask API)**
1. Use **Gunicorn** for production:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```
2. Deploy to a cloud platform like **AWS, DigitalOcean, or Heroku**.

### **Frontend Deployment (React)**
1. Build the React app:
   ```bash
   npm run build
   ```
2. Host on **Netlify, Vercel, or AWS S3**.

---

## 🤝 Contributing

- Fork the repository  
- Create a feature branch (`git checkout -b feature-name`)  
- Commit your changes (`git commit -m "Added feature X"`)  
- Push to the branch (`git push origin feature-name`)  
- Open a Pull Request  

---

## 📜 License
This project is licensed under the **MIT License**.
