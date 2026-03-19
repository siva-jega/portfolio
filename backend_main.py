"""
Sivakumar Jegatheesan — Portfolio Backend
Stack: Python 3.11+ · FastAPI · Pydantic · CORS-ready

Run:
  pip install fastapi uvicorn pydantic python-multipart
  uvicorn backend_main:app --reload --port 8000

Docs auto-generated at: http://localhost:8000/docs
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Sivakumar Jegatheesan — Portfolio API",
    description="Backend API serving portfolio data and contact form submissions.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Validation Error Handler ─────────────────────────────────────────────────

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        field = " -> ".join(str(x) for x in err["loc"] if x != "body")
        errors.append(f"{field}: {err['msg']}")
    logger.warning(f"Validation error: {errors}")
    return JSONResponse(
        status_code=422,
        content={"success": False, "errors": errors},
    )

# ─── Data Models ─────────────────────────────────────────────────────────────

class ContactForm(BaseModel):
    name: str
    email: EmailStr
    subject: Optional[str] = "Portfolio Inquiry"
    message: str

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip()

    @field_validator("message")
    @classmethod
    def message_min_length(cls, v):
        if len(v.strip()) < 3:
            raise ValueError("Message must be at least 3 characters")
        return v.strip()


class ContactResponse(BaseModel):
    success: bool
    message: str
    timestamp: str


# ─── Static Portfolio Data ────────────────────────────────────────────────────

PROFILE = {
    "name": "Sivakumar Jegatheesan",
    "title": "AI Systems & Backend Engineer",
    "location": "Boston, MA",
    "email": "s.jegatheesan001@umb.edu",
    "phone": "+1 (508) 816-4970",
    "summary": (
        "AI Systems and Backend Engineer with 3+ years of experience designing "
        "distributed services, real-time data pipelines, and cloud-native platforms. "
        "Specialized in event-driven architectures, large-scale analytics workflows, "
        "and applied AI conversational systems."
    ),
    "links": {
        "github": "https://github.com/siva-jega",
        "linkedin": "https://linkedin.com",
        "leetcode": "https://leetcode.com",
    },
}

SKILLS = {
    "Languages": ["Python", "Go", "TypeScript", "SQL", "Bash"],
    "AI Systems": ["LLM Applications", "Prompt Engineering", "Conversational AI", "Feature Engineering"],
    "Backend & Infra": ["FastAPI", "Fiber", "Axum", "Microservices", "REST", "WebSockets"],
    "Distributed Systems": ["Apache Kafka", "Event Streaming", "ETL Pipelines", "Data Modelling"],
    "Databases": ["PostgreSQL", "MongoDB", "Redis", "MySQL", "DynamoDB", "Neo4j"],
    "Cloud & DevOps": ["AWS Lambda", "S3", "API Gateway", "Docker", "Kubernetes", "CI/CD"],
    "Observability": ["OpenTelemetry", "Prometheus", "CloudWatch", "Distributed Tracing"],
}

EXPERIENCE = [
    {
        "company": "Mariyano Technologies Pvt Ltd",
        "role": "Backend Developer",
        "location": "Chennai, India",
        "duration": "Jun 2023 — May 2025",
        "highlights": [
            "Designed serverless data processing pipelines (AWS Lambda) handling millions of records/day.",
            "Led DB migration DynamoDB → MongoDB, reducing aggregation query latency by ~40%.",
            "Built automated ETL reporting jobs, cutting manual analysis effort by 60%.",
            "Implemented structured logging + CloudWatch dashboards, reducing incident resolution by ~35%.",
        ],
    },
    {
        "company": "Msys Technologies Pvt Ltd",
        "role": "Software Engineer",
        "location": "Bangalore, India",
        "duration": "Aug 2022 — May 2023",
        "highlights": [
            "Developed high-throughput microservices and REST APIs for concurrent workloads.",
            "Implemented async worker concurrency models, improving batch throughput by ~2x.",
            "Contributed to system architecture reviews and API lifecycle governance.",
            "Introduced automated testing and performance validation strategies.",
        ],
    },
    {
        "company": "Virtusa Consulting & Services",
        "role": "Intern Delivery",
        "location": "Chennai, India",
        "duration": "Feb 2022 — May 2022",
        "highlights": [
            "Implemented enterprise-grade SSO integrations using Okta.",
            "Configured OAuth2 and SAML flows for seamless cross-application session federation.",
        ],
    },
]

PROJECTS = [
    {
        "title": "AI Audio Conversational Platform",
        "stack": ["Python", "FastAPI", "WebSockets", "LLM APIs", "Streaming"],
        "github": "https://github.com/siva-jega/audio_chatbot",
        "description": (
            "Real-time conversational AI platform integrating speech recognition, "
            "LLM reasoning, and TTS synthesis with duplex streaming pipelines."
        ),
        "highlights": [
            "Duplex streaming pipelines for low-latency voice interaction",
            "Modular orchestration for prompt management & dialogue state",
            "Token streaming + inference caching to reduce perceived latency",
        ],
    },
    {
        "title": "Distributed Event Processing & Analytics Platform",
        "stack": ["Python", "Kafka", "FastAPI", "PostgreSQL", "Redis", "OpenTelemetry"],
        "github": "https://github.com/siva-jega/event_processing/",
        "description": (
            "Event-driven analytics platform supporting scalable ingestion, "
            "normalization, and reporting pipelines with end-to-end observability."
        ),
        "highlights": [
            "Async ingestion services publishing to Kafka",
            "Resilient consumers with retries, backoff & dead-letter queues",
            "Redis caching + Prometheus metrics + Superset dashboards",
        ],
    },
    {
        "title": "Cloud-Native Commerce Microservices Platform",
        "stack": ["Go", "Rust", "MySQL", "Redis", "Kubernetes", "Docker"],
        "github": "https://bbapp.in",
        "description": (
            "Domain-driven microservices handling auth, order orchestration, "
            "partner operations and notifications deployed on GKE."
        ),
        "highlights": [
            "OTP login, JWT lifecycle management & RBAC enforcement",
            "Pricing engines, wallet mechanics & payment webhooks",
            "Rust-based notification system with observability instrumentation",
        ],
    },
    {
        "title": "Resume Skill Extraction Engine",
        "stack": ["Python", "Flask", "NLP", "MySQL"],
        "github": "https://github.com/siva-jega/resume-extraction",
        "description": (
            "Resume parsing engine extracting structured skill intelligence "
            "from multi-format documents with synonym resolution."
        ),
        "highlights": [
            "Text normalization pipelines for accurate skill detection",
            "Dictionary-driven extraction with hierarchical metadata",
            "JWT-secured ingestion APIs",
        ],
    },
]

EDUCATION = [
    {
        "institution": "University of Massachusetts Boston",
        "degree": "Master of Science — Information Technology",
        "duration": "Sept 2025 — May 2027 (Expected)",
        "gpa": "3.275 / 4.0",
    },
    {
        "institution": "Hindustan Institute of Technology and Science",
        "degree": "Bachelor of Technology — Computer Science",
        "duration": "Sept 2018 — May 2022",
        "gpa": "7.66 / 10.0",
    },
]

# In-memory contact store (replace with DB in production)
contact_submissions: list[dict] = []


# ─── Routes ──────────────────────────────────────────────────────────────────

@app.get("/", tags=["Health"])
def root():
    return {"status": "online", "api": "Sivakumar Portfolio API", "version": "1.0.0"}


@app.get("/api/profile", tags=["Portfolio"])
def get_profile():
    """Returns full profile summary."""
    return PROFILE


@app.get("/api/skills", tags=["Portfolio"])
def get_skills():
    """Returns categorized skills."""
    return SKILLS


@app.get("/api/experience", tags=["Portfolio"])
def get_experience():
    """Returns work experience list."""
    return EXPERIENCE


@app.get("/api/projects", tags=["Portfolio"])
def get_projects():
    """Returns all projects."""
    return PROJECTS


@app.get("/api/education", tags=["Portfolio"])
def get_education():
    """Returns education history."""
    return EDUCATION


@app.get("/api/portfolio", tags=["Portfolio"])
def get_full_portfolio():
    """Returns the complete portfolio data in one call."""
    return {
        "profile": PROFILE,
        "skills": SKILLS,
        "experience": EXPERIENCE,
        "projects": PROJECTS,
        "education": EDUCATION,
    }


@app.post("/api/contact", response_model=ContactResponse, tags=["Contact"])
async def submit_contact(form: ContactForm, background_tasks: BackgroundTasks):
    """
    Handles contact form submissions.
    Stores submission and optionally sends email notification.
    """
    submission = {
        **form.model_dump(),
        "timestamp": datetime.utcnow().isoformat(),
        "id": len(contact_submissions) + 1,
    }
    contact_submissions.append(submission)
    logger.info(f"New contact submission from {form.email} — {form.subject}")

    # Background email notification (configure SMTP credentials to enable)
    # background_tasks.add_task(send_email_notification, form)

    return ContactResponse(
        success=True,
        message="Thanks for reaching out! I'll get back to you within 24 hours.",
        timestamp=submission["timestamp"],
    )


@app.get("/api/contact/submissions", tags=["Admin"])
def list_submissions(secret: str = ""):
    """
    Admin endpoint to view contact submissions.
    Protect this with proper auth in production!
    """
    if secret != "your-admin-secret":
        raise HTTPException(status_code=403, detail="Forbidden")
    return {"count": len(contact_submissions), "submissions": contact_submissions}


# ─── Optional email helper ────────────────────────────────────────────────────

def send_email_notification(form: ContactForm):
    """
    Configure with your SMTP server to receive email alerts.
    Uncomment usage in the contact route above.
    """
    try:
        msg = MIMEText(
            f"From: {form.name} <{form.email}>\n\n{form.message}"
        )
        msg["Subject"] = f"[Portfolio] {form.subject}"
        msg["From"] = "noreply@portfolio.com"
        msg["To"] = "s.jegatheesan001@umb.edu"

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login("your-email@gmail.com", "your-app-password")
            server.sendmail(msg["From"], msg["To"], msg.as_string())
    except Exception as e:
        logger.error(f"Email notification failed: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend_main:app", host="0.0.0.0", port=8000, reload=True)
