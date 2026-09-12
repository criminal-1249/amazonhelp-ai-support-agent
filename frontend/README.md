# Amazon Help AI Support Agent - Frontend

A production-grade, responsive customer support chat interface built with **React** and **Vite**, powered by a Retrieval-Augmented Generation (RAG) backend.

## Key Features

- **Live AI Support Chat**: Direct query-parameter integration with FastAPI backend (`POST /chat?message=...`).
- **RAG Evidence Viewer**: Collapsible case reference view displaying retrieved historical customer queries, official agent answers, and conversation IDs.
- **Intent Classification Badges**: Visual indicator tags for recognized intents (e.g., Order Status, Damaged Product, Refund Issue).
- **Automated Escalation Decisioning**: Highlights whether inquiries are `✓ Automatically handled` or `⚠ Requires escalation` with expandable reasoning (`Why?`).
- **Dynamic Welcome Screen**: Quick-start prompt suggestions for common inquiries.
- **Thread History & Local Persistence**: Multi-conversation support persisted locally in the browser.
- **Responsive Layout**: Desktop sidebar and mobile drawer with real-time agent online indicator.

---

## 1. How to Install

Ensure you have **Node.js 18+** installed.

Open your terminal in the `frontend` directory:

```bash
cd frontend
npm install
```

---

## 2. How to Configure `VITE_API_URL`

The frontend communicates with the backend via the `VITE_API_URL` environment variable.

### Local Development
In the `frontend/` directory, the `.env` file points to your local FastAPI backend:

```env
VITE_API_URL=http://127.0.0.1:8000
```

### Production (e.g. Render / Cloud Backend)
When deploying your backend to a cloud host such as Render, update the environment variable:

```env
VITE_API_URL=https://YOUR-RENDER-BACKEND.onrender.com
```

---

## 3. How to Run Locally

### Step 1: Start the Backend
Make sure your FastAPI server is running on port 8000:

```bash
# In project root:
python -m uvicorn app:app --host 127.0.0.1 --port 8000
```

### Step 2: Start the Frontend
In the `frontend/` folder:

```bash
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

---

## 4. How to Build for Production

To create an optimized production build:

```bash
npm run build
```

This generates output assets in the `dist/` directory.

You can preview the production bundle locally with:

```bash
npm run preview
```

---

## 5. How to Deploy to Vercel

The application is preconfigured with `vercel.json` for single-page application (SPA) routing.

### Option A: Deploy via Vercel CLI

1. Install the Vercel CLI (if not already installed):
   ```bash
   npm install -g vercel
   ```

2. From the `frontend/` directory, log in and deploy:
   ```bash
   cd frontend
   vercel
   ```

3. When prompted, add your production backend URL as an environment variable:
   ```bash
   VITE_API_URL=https://YOUR-RENDER-BACKEND.onrender.com
   ```

4. Deploy to production:
   ```bash
   vercel --prod
   ```

### Option B: Deploy via Vercel Web Dashboard (Git Integration)

1. Push your repository to GitHub / GitLab / Bitbucket.
2. Go to [vercel.com](https://vercel.com) and click **"Add New Project"**.
3. Import your repository.
4. Set the **Root Directory** to `frontend`.
5. Under **Environment Variables**, add:
   - **Key**: `VITE_API_URL`
   - **Value**: `https://YOUR-RENDER-BACKEND.onrender.com` (or your active production backend endpoint)
6. Click **Deploy**. Vercel will build and serve your app globally.
