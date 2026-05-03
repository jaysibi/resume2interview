"""
Create a proper Job Description in the database for testing
"""
from db import SessionLocal
from models import JobDescription
from datetime import datetime

# Sample job description with substantial content
jd_text = """Senior Data Scientist

We are seeking an experienced Senior Data Scientist to join our AI team.

Required Skills:
- Expert knowledge of Python (pandas, numpy, scikit-learn, matplotlib)
- Machine Learning algorithms (supervised and unsupervised learning)
- Deep Learning frameworks (TensorFlow, PyTorch, Keras)
- SQL and database optimization
- Statistical analysis and A/B testing
- Data visualization (Tableau, Power BI)
- Communication and stakeholder management

Preferred Skills:
- Cloud platforms (AWS SageMaker, Azure ML, GCP AI Platform)
- Big Data technologies (Spark, Hadoop, Kafka)
- Natural Language Processing and Computer Vision
- MLOps and model deployment experience
- Experience with Docker and Kubernetes

Responsibilities:
- Design and implement machine learning models to solve business problems
- Analyze large-scale datasets to extract actionable insights
- Collaborate with engineering teams to deploy models to production
- Present findings and recommendations to senior leadership
- Mentor junior data scientists

Requirements:
- Master's or PhD in Computer Science, Statistics, Mathematics, or related field
- 5+ years of experience in data science or machine learning
- Proven track record of deploying ML models to production
- Strong problem-solving and analytical skills
"""

db = SessionLocal()
try:
    jd = JobDescription(
        filename="test_senior_data_scientist.txt",
        raw_text=jd_text,
        mandatory_skills=["Python", "Machine Learning", "SQL", "Statistics"],
        preferred_skills=["Deep Learning", "Cloud platforms", "Big Data"],
        keywords=["Python", "pandas", "scikit-learn", "TensorFlow", "PyTorch", "SQL", "Tableau"]
    )
    db.add(jd)
    db.commit()
    db.refresh(jd)
    
    print(f"✅ Created Job Description with ID: {jd.id}")
    print(f"Text length: {len(jd.raw_text)} chars")
    print(f"Created at: {jd.created_at}")
    
except Exception as e:
    db.rollback()
    print(f"❌ Error: {e}")
finally:
    db.close()
