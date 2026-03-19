# Sivakumar Jegatheesan — Portfolio

A full-stack portfolio with a **Python FastAPI backend** and a **React-style HTML/JS frontend**.

---

## Project Structure

```
portfolio/
├── backend_main.py         # FastAPI backend (Python)
├── portfolio_frontend.html # Standalone frontend (HTML + vanilla React-style JS)
└── README.md
```

---

## Backend — FastAPI (Python)

### Install dependencies
```bash
pip install fastapi uvicorn pydantic python-multipart
```

### Run the server
```bash
uvicorn backend_main:app --reload --port 8000
```

### API Endpoints

| Method | Endpoint              | Description                  |
|--------|-----------------------|------------------------------|
| GET    | /                     | Health check                 |
| GET    | /api/profile          | Profile summary              |
| GET    | /api/skills           | Categorized skills           |
| GET    | /api/experience       | Work experience              |
| GET    | /api/projects         | All projects                 |
| GET    | /api/education        | Education history            |
| GET    | /api/portfolio        | Full portfolio (all-in-one)  |
| POST   | /api/contact          | Submit contact form          |

Interactive API docs: **http://localhost:8000/docs**

---

## Frontend — HTML/JS

Open `portfolio_frontend.html` directly in your browser, or serve it:

```bash
# Simple Python server
python -m http.server 3000
# Then open http://localhost:3000/portfolio_frontend.html
```

### Connect to the backend
In `portfolio_frontend.html`, the contact form posts to:
```
http://localhost:8000/api/contact
```
Make sure the backend is running on port 8000 for the form to work.

To load portfolio data dynamically from the API instead of the inline JS data, replace the
top of the `<script>` block with:

```javascript
const res = await fetch('http://localhost:8000/api/portfolio');
const { skills, experience, projects, education } = await res.json();
```

---

## Migrate to React (optional)

To use this as a proper React app:
```bash
npx create-react-app siva-portfolio
# Copy component logic from portfolio_frontend.html into src/App.jsx
# Run: npm start
```

---

## Deploy

- **Backend**: Deploy to AWS Lambda (with Mangum), Railway, Render, or any VPS.
- **Frontend**: Deploy to Vercel, Netlify, or GitHub Pages.
- **Update CORS origins** in `backend_main.py` to match your deployed frontend URL.

---

## Contact Email (optional)

To receive email alerts on form submission, configure SMTP in `backend_main.py`:
```python
server.login("your-email@gmail.com", "your-app-password")
```
Then uncomment `background_tasks.add_task(send_email_notification, form)` in the `/api/contact` route.
