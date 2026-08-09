# Incident Report: Unhandled exception in order processing

- **Incident ID:** incident-corr-0091
- **Severity:** CRITICAL
- **Generated:** 2026-08-07T18:21:14.151575+00:00
- **Confidence Level:** medium

## Executive Summary

A critical incident is occurring across multiple services, with a high number of errors and fatalities reported.

## Incident Summary

The current incident involves a series of failures in various services, including payment-service, notification-service, order-service, and auth-service. The top recurring messages include 'Unhandled exception in order processing', 'Docker container exited unexpectedly', and 'PLC communication timeout'.

## Major Issues Detected

### 'Memory usage high' recurred 1119 time(s), including a burst of 241 within 15 minute(s)

- Occurrences: 1119
- First seen: 2026-08-01 09:00:08.309000+00:00
- Last seen: 2026-08-01 10:19:42.420000+00:00
- Affected sources: application, docker, plc
### 'Slow response detected' recurred 1090 time(s), including a burst of 225 within 15 minute(s)

- Occurrences: 1090
- First seen: 2026-08-01 09:00:01.585000+00:00
- Last seen: 2026-08-01 10:19:43.737000+00:00
- Affected sources: application, docker, plc
### 'Unhandled exception in order processing' recurred 391 time(s), including a burst of 97 within 15 minute(s)

- Occurrences: 391
- First seen: 2026-08-01 09:00:13.453000+00:00
- Last seen: 2026-08-01 10:18:59.493000+00:00
- Affected sources: application, docker, plc
### 'Docker container exited unexpectedly' recurred 359 time(s), including a burst of 90 within 15 minute(s)

- Occurrences: 359
- First seen: 2026-08-01 09:00:14.104000+00:00
- Last seen: 2026-08-01 10:19:04.726000+00:00
- Affected sources: application, docker, plc
### Correlation group `corr-0091`

- Components: auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01
- Window: 2026-08-01 09:21:54.056000+00:00 -> 2026-08-01 09:22:23.992000+00:00
- Confidence: 0.60

## Timeline of Important Events

- **2026-08-01 09:00:01.180000+00:00** [first_critical_error] First critical error -- First ERROR/CRITICAL event: 'PLC communication timeout' on payment-service@wilston-prod-03
- **2026-08-01 09:00:14.104000+00:00** [fatal_event] Fatal: Docker container exited unexpectedly -- First FATAL occurrence of 'Docker container exited unexpectedly' on notification-service@wilston-prod-03
- **2026-08-01 09:00:25.866000+00:00** [fatal_event] Fatal: ECONNRESET while calling payment gateway -- First FATAL occurrence of 'ECONNRESET while calling payment gateway' on payment-service@wilston-prod-02
- **2026-08-01 09:00:39.409000+00:00** [fatal_event] Fatal: Kafka publish failed -- First FATAL occurrence of 'Kafka publish failed' on notification-service@wilston-prod-01
- **2026-08-01 09:00:43.174000+00:00** [fatal_event] Fatal: PLC communication timeout -- First FATAL occurrence of 'PLC communication timeout' on order-service@wilston-prod-02
- **2026-08-01 09:00:51.993000+00:00** [fatal_event] Fatal: PostgreSQL error: deadlock detected -- First FATAL occurrence of 'PostgreSQL error: deadlock detected' on order-service@wilston-prod-03
- **2026-08-01 09:01:54.029000+00:00** [fatal_event] Fatal: Unhandled exception in order processing -- First FATAL occurrence of 'Unhandled exception in order processing' on order-service@wilston-prod-01
- **2026-08-01 09:02:06.014000+00:00** [fatal_event] Fatal: UnhandledPromiseRejection: TypeError: Cannot read properties of undefined -- First FATAL occurrence of 'UnhandledPromiseRejection: TypeError: Cannot read properties of undefined' on notification-service@wilston-prod-02
- **2026-08-01 09:03:11.816000+00:00** [fatal_event] Fatal: JWT verification failed -- First FATAL occurrence of 'JWT verification failed' on auth-service@wilston-prod-02
- **2026-08-01 09:04:38.661000+00:00** [recovery_event] Incident corr-0015 resolved -- All 3 component/host pair(s) involved in incident corr-0015 showed normal activity again by this point
- **2026-08-01 09:10:08.868000+00:00** [recovery_event] Incident corr-0037 resolved -- All 2 component/host pair(s) involved in incident corr-0037 showed normal activity again by this point
- **2026-08-01 09:10:45.626000+00:00** [recovery_event] Incident corr-0040 resolved -- All 5 component/host pair(s) involved in incident corr-0040 showed normal activity again by this point
- **2026-08-01 09:11:04.923000+00:00** [recovery_event] Incident corr-0042 resolved -- All 2 component/host pair(s) involved in incident corr-0042 showed normal activity again by this point
- **2026-08-01 09:12:03.805000+00:00** [recovery_event] Incident corr-0047 resolved -- All 2 component/host pair(s) involved in incident corr-0047 showed normal activity again by this point
- **2026-08-01 09:14:43.358000+00:00** [recovery_event] Incident corr-0058 resolved -- All 3 component/host pair(s) involved in incident corr-0058 showed normal activity again by this point
- **2026-08-01 09:15:00.436000+00:00** [recovery_event] Incident corr-0059 resolved -- All 2 component/host pair(s) involved in incident corr-0059 showed normal activity again by this point
- **2026-08-01 09:18:43.557000+00:00** [recovery_event] Incident corr-0072 resolved -- All 4 component/host pair(s) involved in incident corr-0072 showed normal activity again by this point
- **2026-08-01 09:19:12.749000+00:00** [recovery_event] Incident corr-0075 resolved -- All 2 component/host pair(s) involved in incident corr-0075 showed normal activity again by this point
- **2026-08-01 09:19:21.352000+00:00** [recovery_event] Incident corr-0076 resolved -- All 1 component/host pair(s) involved in incident corr-0076 showed normal activity again by this point
- **2026-08-01 09:19:27.837000+00:00** [recovery_event] Incident corr-0077 resolved -- All 1 component/host pair(s) involved in incident corr-0077 showed normal activity again by this point
- **2026-08-01 09:20:10.357000+00:00** [recovery_event] Incident corr-0081 resolved -- All 3 component/host pair(s) involved in incident corr-0081 showed normal activity again by this point
- **2026-08-01 09:22:33.317000+00:00** [recovery_event] Incident corr-0091 resolved -- All 5 component/host pair(s) involved in incident corr-0091 showed normal activity again by this point
- **2026-08-01 09:23:06.914000+00:00** [recovery_event] Incident corr-0095 resolved -- All 3 component/host pair(s) involved in incident corr-0095 showed normal activity again by this point
- **2026-08-01 09:30:35.593000+00:00** [recovery_event] Incident corr-0122 resolved -- All 1 component/host pair(s) involved in incident corr-0122 showed normal activity again by this point
- **2026-08-01 09:34:25.870000+00:00** [recovery_event] Incident corr-0133 resolved -- All 2 component/host pair(s) involved in incident corr-0133 showed normal activity again by this point
- **2026-08-01 09:35:21.459000+00:00** [recovery_event] Incident corr-0135 resolved -- All 3 component/host pair(s) involved in incident corr-0135 showed normal activity again by this point
- **2026-08-01 09:35:28.905000+00:00** [recovery_event] Incident corr-0138 resolved -- All 2 component/host pair(s) involved in incident corr-0138 showed normal activity again by this point
- **2026-08-01 09:37:53.490000+00:00** [recovery_event] Incident corr-0145 resolved -- All 3 component/host pair(s) involved in incident corr-0145 showed normal activity again by this point
- **2026-08-01 09:39:30.603000+00:00** [recovery_event] Incident corr-0153 resolved -- All 4 component/host pair(s) involved in incident corr-0153 showed normal activity again by this point
- **2026-08-01 09:44:13.439000+00:00** [recovery_event] Incident corr-0167 resolved -- All 6 component/host pair(s) involved in incident corr-0167 showed normal activity again by this point
- **2026-08-01 09:46:10.917000+00:00** [recovery_event] Incident corr-0174 resolved -- All 6 component/host pair(s) involved in incident corr-0174 showed normal activity again by this point
- **2026-08-01 09:51:30.486000+00:00** [recovery_event] Incident corr-0193 resolved -- All 6 component/host pair(s) involved in incident corr-0193 showed normal activity again by this point
- **2026-08-01 09:53:02.316000+00:00** [recovery_event] Incident corr-0199 resolved -- All 4 component/host pair(s) involved in incident corr-0199 showed normal activity again by this point
- **2026-08-01 09:53:03.156000+00:00** [recovery_event] Incident corr-0201 resolved -- All 2 component/host pair(s) involved in incident corr-0201 showed normal activity again by this point
- **2026-08-01 09:55:25.949000+00:00** [recovery_event] Incident corr-0213 resolved -- All 2 component/host pair(s) involved in incident corr-0213 showed normal activity again by this point
- **2026-08-01 10:00:34.836000+00:00** [recovery_event] Incident corr-0230 resolved -- All 3 component/host pair(s) involved in incident corr-0230 showed normal activity again by this point
- **2026-08-01 10:01:47.238000+00:00** [recovery_event] Incident corr-0236 resolved -- All 2 component/host pair(s) involved in incident corr-0236 showed normal activity again by this point
- **2026-08-01 10:03:21.583000+00:00** [recovery_event] Incident corr-0241 resolved -- All 4 component/host pair(s) involved in incident corr-0241 showed normal activity again by this point
- **2026-08-01 10:09:31.494000+00:00** [recovery_event] Incident corr-0264 resolved -- All 2 component/host pair(s) involved in incident corr-0264 showed normal activity again by this point
- **2026-08-01 10:16:55.504000+00:00** [recovery_event] Incident corr-0288 resolved -- All 3 component/host pair(s) involved in incident corr-0288 showed normal activity again by this point
- **2026-08-01 10:17:21.799000+00:00** [recovery_event] Incident corr-0290 resolved -- All 2 component/host pair(s) involved in incident corr-0290 showed normal activity again by this point
- **2026-08-01 10:18:20.417000+00:00** [recovery_event] Incident corr-0294 resolved -- All 3 component/host pair(s) involved in incident corr-0294 showed normal activity again by this point

## Root Cause Analysis

### (medium likelihood) Insufficient memory allocation for Docker containers may have caused the OOM-kill event.

- 359 occurrences of 'Docker container exited unexpectedly' on notification-service@wilston-prod-03
### (low likelihood) A slow response detected in performance could be related to a memory leak or high CPU usage.

- 1090 occurrences of 'Slow response detected' on api-gateway@wilston-prod-01
### (high likelihood) An unhandled exception in order processing may indicate a problem with the order-service or its dependencies.

- 391 occurrences of 'Unhandled exception in order processing' on order-service@wilston-prod-01

**How this conclusion was reached:** Based on the current log evidence, it appears that there may be multiple potential root causes contributing to this incident. Further investigation is required to determine the most likely cause and implement corrective actions.

**Open questions:**
- What was the impact of the slow response detected in performance?
- Are there any other services or components experiencing issues?

## Supporting Evidence

- total_logs=30000, errors=2922, warnings=5362, fatals=651
- affected_hosts=['wilston-prod-01', 'wilston-prod-02', 'wilston-prod-03']
- top_recurring_messages=[('Health check passed', 2173), ('Request completed', 2165), ('Redis cache hit', 2157), ('Redis cache miss', 2129), ('Connected to PostgreSQL', 2125)]

## Similar Historical Incidents

- **Unhandled exceptions in order processing after a schema change** (similarity: 0.77)
  The order service began throwing unhandled exceptions while processing a subset of orders after a backward-incompatible field rename in an upstream event schema.
- **Docker containers exiting unexpectedly under memory pressure** (similarity: 0.76)
  Multiple service containers were OOM-killed during a traffic spike.
- **Elevated memory usage across services from a slow memory leak** (similarity: 0.69)
  Gradual memory growth was observed across the gateway and notification services over several days, eventually triggering restarts.
- **Kafka publish failures during broker rebalance** (similarity: 0.66)
  Order and notification events failed to publish to Kafka during a rolling broker restart.
- **Recurring PostgreSQL deadlocks under high order volume** (similarity: 0.64)
  Repeated deadlock errors from PostgreSQL during checkout traffic spikes, causing order and payment requests to fail.

LLM-cited historical incidents (attributed precedent, not current fact):
- inc-009: Unhandled exceptions in order processing after a schema change -- Both incidents involve unhandled exceptions in the order-service, suggesting a possible root cause of inadequate error handling or schema validation.

## Recommended Fixes

- Investigate and address potential memory allocation issues for Docker containers.
- Monitor performance metrics to identify any slow responses or high CPU usage.
- Review and validate error handling mechanisms in the order-service, particularly after a recent schema change.

## Confidence Level

**medium**

_The model judged current log evidence insufficient for a fully confident conclusion._
