

# ===========================
# Usage Analytics Endpoints
# ===========================

@app.get("/api/analytics/usage-stats")
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


@app.get("/api/analytics/usage-logs")
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
