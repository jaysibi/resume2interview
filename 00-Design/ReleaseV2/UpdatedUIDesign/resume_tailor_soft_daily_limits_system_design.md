# Resume Tailor — Soft Daily Limits System Design

## Objective

Design a lightweight, scalable, and cost-effective abuse prevention system for Resume Tailor.

The system should:
- prevent excessive free usage,
- protect backend resources,
- reduce automated abuse,
- maintain a smooth user experience,
- and support MVP-scale growth.

---

# High-Level Architecture

```text
Client Browser
↓
Frontend (Next.js)
↓
API Gateway / FastAPI
↓
Rate Limit Middleware
↓
Redis (runtime counters)
↓
PostgreSQL/Supabase (analytics + monitoring)
↓
ATS Processing Engine
```

---

# Daily Limit Strategy

## Rule

All users are limited to:

- 5 resume analyses per day

This applies to:
- anonymous users
- logged-in users

---

# Tracking Strategy

To reduce abuse while avoiding heavy authentication requirements, the system tracks multiple identifiers.

## Track These Identifiers

| Identifier | Purpose |
|---|---|
| IP Address | Basic abuse detection |
| Browser Fingerprint | Device uniqueness |
| Session ID | Session continuity |

---

# Identity Resolution Logic

## Anonymous User Key

```text
anonymous_key =
hash(ip + browser_fingerprint + session_id)
```

This becomes the unique tracking identity for rate limiting.

---

# Runtime Counter Storage — Redis

Redis is used because:
- extremely fast,
- ideal for counters,
- supports automatic expiration (TTL),
- inexpensive to operate.

---

# Redis Key Structure

## Example

```text
anon:{hash}:2026-05-07
```

---

# Redis Value Example

```json
{
  "count": 3
}
```

---

# TTL Configuration

Each Redis key expires automatically after:

```text
24 hours
```

---

# Persistent Monitoring Storage

In addition to Redis counters, usage analytics are stored in PostgreSQL or Supabase.

Purpose:
- monitoring,
- abuse detection,
- analytics,
- future reporting.

---

# Database Schema

## Table: usage_logs

| Column | Type |
|---|---|
| id | UUID |
| ip_address | TEXT |
| fingerprint | TEXT |
| session_id | TEXT |
| analysis_count | INTEGER |
| created_at | TIMESTAMP |

---

# Backend Request Flow

---

## Step 1 — User Submits Resume

User clicks:

```text
Analyze Resume
```

---

## Step 2 — Extract Identifiers

Backend extracts:

```python
ip_address
browser_fingerprint
session_id
```

---

## Step 3 — Build Tracking Key

```python
tracking_key = hash(ip + fingerprint + session_id)
```

---

## Step 4 — Query Redis

```python
count = redis.get(redis_key)
```

---

## Step 5 — Apply Daily Limit Rule

```python
if count >= 5:
    deny_request()
```

---

## Step 6 — Increment Counter

```python
redis.incr(redis_key)
redis.expire(redis_key, 86400)
```

---

# Friendly UX Design

The system should avoid aggressive or hostile messaging.

Instead of showing:

```text
Limit exceeded.
```

Use a softer experience.

---

# Recommended UX Copy

## Daily Limit Modal

```jsx
<div className="bg-yellow-50 border border-yellow-200 rounded-2xl p-6">

  <h3 className="text-xl font-semibold text-yellow-800">
    Daily Free Limit Reached
  </h3>

  <p className="mt-3 text-yellow-700 leading-7">
    You’ve reached today’s free analysis limit.
  </p>

  <p className="mt-2 text-yellow-700 leading-7">
    We’re currently offering limited free access while improving
    Resume Tailor for early users.
  </p>

  <button className="mt-5 bg-blue-600 text-white px-6 py-3 rounded-xl">
    Try Again Tomorrow
  </button>

</div>
```

---

# Additional Abuse Protection

## 1. Browser Fingerprinting

Recommended:
- FingerprintJS (community edition)

Benefits:
- tracks repeat devices,
- reduces bypass attempts,
- improves abuse detection.

---

## 2. Cloudflare Protection

Recommended:
- Cloudflare Free Tier

Benefits:
- bot filtering,
- DDoS protection,
- edge-level rate limiting.

---

## 3. Cooldown Between Requests

Prevent rapid repeated submissions.

Example:

```text
Please wait 30 seconds before another analysis.
```

---

## 4. Request Queueing

Recommended flow:

```text
Queued → Processing → Results
```

Benefits:
- smoother load handling,
- reduced burst traffic,
- improved system stability.

---

# Monitoring Metrics

The system should actively track operational and abuse-related metrics.

## Metrics to Monitor

| Metric | Purpose |
|---|---|
| Requests per day | Overall traffic tracking |
| Resume analyses per day | Usage measurement |
| Top IP addresses | Abuse detection |
| Fingerprint reuse frequency | Spam detection |
| Failed uploads | Error monitoring |
| Rate-limit denials | Abuse trend tracking |
| Average processing time | Performance monitoring |
| Queue wait time | Load management |
| Anonymous repeat users | Retention visibility |

---

# Recommended Tech Stack

| Layer | Tool |
|---|---|
| Frontend | Next.js |
| Backend | FastAPI |
| Runtime Counter Store | Redis / Upstash |
| Persistent Database | PostgreSQL / Supabase |
| Fingerprinting | FingerprintJS |
| Protection Layer | Cloudflare |

---

# MVP Recommendation

For the MVP launch, implement only:

- Redis counters
- IP + fingerprint tracking
- 5 analyses/day limit
- Friendly UX messaging
- Basic monitoring metrics

Avoid overengineering early-stage protection systems.
