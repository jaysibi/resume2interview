

# ===========================
# Usage Analytics Endpoints
# ===========================

# Password protection for analytics
from fastapi import Header
import os

async def verify_analytics_password(x_analytics_password: str = Header(None)):
    """
    Verify analytics dashboard password from environment variable
    """
    # Get password from environment variable (default: admin123)
    analytics_password = os.getenv("ANALYTICS_PASSWORD", "admin123")
    
    if x_analytics_password is None or x_analytics_password != analytics_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error_response("UNAUTHORIZED", "Invalid or missing analytics password", "Please provide X-Analytics-Password header")
        )
    return True


@app.get("/api/analytics/usage-stats", dependencies=[Depends(verify_analytics_password)])
async def get_usage_stats(db: Session = Depends(get_db)):
    """
    Get current usage statistics from in-memory rate limiter
    Returns real-time counters for today
    """
    try:
        stats = rate_limiter.get_usage_stats()
        return {
            "success": True,
            "data": stats
        }
    except Exception as e:
        logger.error(f"Error fetching usage stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response("INTERNAL_SERVER_ERROR", "Failed to fetch usage statistics", str(e))
        )


@app.get("/api/analytics/usage-logs", dependencies=[Depends(verify_analytics_password)])
async def get_usage_logs(
    days: int = 7,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get historical usage logs from database
    
    - **days**: Number of days to look back (default: 7)
    - **limit**: Maximum number of records to return (default: 100)
    """
    try:
        from datetime import datetime, timedelta
        from sqlalchemy import and_, func as sql_func
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Get recent logs
        logs = db.query(UsageLog).filter(
            UsageLog.created_at >= cutoff_date
        ).order_by(UsageLog.created_at.desc()).limit(limit).all()
        
        # Get aggregate stats
        total_requests = db.query(sql_func.count(UsageLog.id)).filter(
            UsageLog.created_at >= cutoff_date
        ).scalar()
        
        rate_limited_count = db.query(sql_func.count(UsageLog.id)).filter(
            and_(
                UsageLog.created_at >= cutoff_date,
                UsageLog.rate_limited == 1
            )
        ).scalar()
        
        unique_ips = db.query(sql_func.count(sql_func.distinct(UsageLog.ip_address))).filter(
            UsageLog.created_at >= cutoff_date
        ).scalar()
        
        # Top IPs
        top_ips = db.query(
            UsageLog.ip_address,
            sql_func.count(UsageLog.id).label('count')
        ).filter(
            UsageLog.created_at >= cutoff_date
        ).group_by(UsageLog.ip_address).order_by(
            sql_func.count(UsageLog.id).desc()
        ).limit(10).all()
        
        # Endpoint distribution
        endpoint_stats = db.query(
            UsageLog.endpoint,
            sql_func.count(UsageLog.id).label('count')
        ).filter(
            UsageLog.created_at >= cutoff_date
        ).group_by(UsageLog.endpoint).order_by(
            sql_func.count(UsageLog.id).desc()
        ).all()
        
        return {
            "success": True,
            "data": {
                "period_days": days,
                "total_requests": total_requests or 0,
                "rate_limited_requests": rate_limited_count or 0,
                "unique_ips": unique_ips or 0,
                "top_ips": [{"ip": ip, "count": count} for ip, count in top_ips],
                "endpoint_distribution": [{"endpoint": ep, "count": count} for ep, count in endpoint_stats],
                "recent_logs": [
                    {
                        "id": log.id,
                        "ip_address": log.ip_address,
                        "endpoint": log.endpoint,
                        "method": log.method,
                        "status_code": log.status_code,
                        "rate_limited": bool(log.rate_limited),
                        "created_at": log.created_at.isoformat() if log.created_at else None
                    }
                    for log in logs
                ]
            }
        }
    except Exception as e:
        logger.error(f"Error fetching usage logs: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response("INTERNAL_SERVER_ERROR", "Failed to fetch usage logs", str(e))
        )


@app.get("/api/analytics/application-stats", dependencies=[Depends(verify_analytics_password)])
async def get_application_stats(
    days: int = 30,
    db: Session = Depends(get_db)
):
    """
    Get application analysis statistics
    
    - **days**: Number of days to look back (default: 30)
    
    Returns:
    - Total applications analyzed
    - Average match scores (Gap Analysis)
    - Average ATS scores
    - Most common missing skills
    - Top companies/job titles
    - Daily analysis trends
    """
    try:
        from datetime import datetime, timedelta
        from sqlalchemy import and_, func as sql_func, desc
        from models_v2 import Application, GapAnalysis, ATSScore, JobDescription, User
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Total applications
        total_applications = db.query(sql_func.count(Application.id)).filter(
            Application.created_at >= cutoff_date
        ).scalar() or 0
        
        # Unique users who ran analyses
        unique_users = db.query(sql_func.count(sql_func.distinct(Application.user_id))).filter(
            Application.created_at >= cutoff_date
        ).scalar() or 0
        
        # Average match score from Gap Analysis
        avg_match_score = db.query(sql_func.avg(GapAnalysis.match_score)).join(
            Application, Application.id == GapAnalysis.application_id
        ).filter(
            Application.created_at >= cutoff_date
        ).scalar()
        avg_match_score = round(avg_match_score, 1) if avg_match_score else 0
        
        # Average ATS score
        avg_ats_score = db.query(sql_func.avg(ATSScore.ats_score)).join(
            Application, Application.id == ATSScore.application_id
        ).filter(
            Application.created_at >= cutoff_date
        ).scalar()
        avg_ats_score = round(avg_ats_score, 1) if avg_ats_score else 0
        
        # Top companies (from job descriptions)
        top_companies = db.query(
            JobDescription.company,
            sql_func.count(Application.id).label('count')
        ).join(
            Application, Application.jd_id == JobDescription.id
        ).filter(
            and_(
                Application.created_at >= cutoff_date,
                JobDescription.company.isnot(None),
                JobDescription.company != ''
            )
        ).group_by(JobDescription.company).order_by(
            desc('count')
        ).limit(10).all()
        
        # Top job titles
        top_job_titles = db.query(
            JobDescription.title,
            sql_func.count(Application.id).label('count')
        ).join(
            Application, Application.jd_id == JobDescription.id
        ).filter(
            and_(
                Application.created_at >= cutoff_date,
                JobDescription.title.isnot(None),
                JobDescription.title != ''
            )
        ).group_by(JobDescription.title).order_by(
            desc('count')
        ).limit(10).all()
        
        # Most common missing skills
        # Aggregate missing_required_skills from all gap analyses
        gap_analyses = db.query(GapAnalysis).join(
            Application, Application.id == GapAnalysis.application_id
        ).filter(
            Application.created_at >= cutoff_date
        ).all()
        
        missing_skills_counter = {}
        for gap in gap_analyses:
            if gap.missing_required_skills:
                for skill in gap.missing_required_skills:
                    if isinstance(skill, str) and skill.strip():
                        skill_clean = skill.strip().lower()
                        missing_skills_counter[skill_clean] = missing_skills_counter.get(skill_clean, 0) + 1
        
        # Sort by frequency
        top_missing_skills = sorted(missing_skills_counter.items(), key=lambda x: x[1], reverse=True)[:15]
        
        # Daily trend (applications per day)
        daily_trend = db.query(
            sql_func.date(Application.created_at).label('date'),
            sql_func.count(Application.id).label('count')
        ).filter(
            Application.created_at >= cutoff_date
        ).group_by(
            sql_func.date(Application.created_at)
        ).order_by('date').all()
        
        # Score distribution (Gap Analysis)
        score_ranges = {
            "0-20": 0,
            "21-40": 0,
            "41-60": 0,
            "61-80": 0,
            "81-100": 0
        }
        
        scores = db.query(GapAnalysis.match_score).join(
            Application, Application.id == GapAnalysis.application_id
        ).filter(
            Application.created_at >= cutoff_date
        ).all()
        
        for score_tuple in scores:
            score = score_tuple[0]
            if score is not None:
                if score <= 20:
                    score_ranges["0-20"] += 1
                elif score <= 40:
                    score_ranges["21-40"] += 1
                elif score <= 60:
                    score_ranges["41-60"] += 1
                elif score <= 80:
                    score_ranges["61-80"] += 1
                else:
                    score_ranges["81-100"] += 1
        
        return {
            "success": True,
            "data": {
                "period_days": days,
                "total_applications": total_applications,
                "unique_users": unique_users,
                "avg_match_score": avg_match_score,
                "avg_ats_score": avg_ats_score,
                "top_companies": [{"company": company, "count": count} for company, count in top_companies],
                "top_job_titles": [{"title": title, "count": count} for title, count in top_job_titles],
                "top_missing_skills": [{"skill": skill, "count": count} for skill, count in top_missing_skills],
                "daily_trend": [{"date": date.isoformat() if date else None, "count": count} for date, count in daily_trend],
                "score_distribution": score_ranges
            }
        }
    except Exception as e:
        logger.error(f"Error fetching application stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response("INTERNAL_SERVER_ERROR", "Failed to fetch application statistics", str(e))
        )
