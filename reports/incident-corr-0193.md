# Incident Report: ECONNRESET while calling payment gateway

- **Incident ID:** incident-corr-0193
- **Severity:** CRITICAL
- **Generated:** 2026-08-07T19:16:08.640922+00:00
- **Confidence Level:** high

## Executive Summary

Current incident: Payment gateway ECONNRESET spikes during provider maintenance

## Incident Summary

The payment service experienced a spike in ECONNRESET errors calling the external payment gateway, which is attributed to unannounced maintenance performed by the payment provider.

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
### 'External API latency increased' recurred 1076 time(s), including a burst of 219 within 15 minute(s)

- Occurrences: 1076
- First seen: 2026-08-01 09:00:01.508000+00:00
- Last seen: 2026-08-01 10:19:11.780000+00:00
- Affected sources: application, docker, plc
### 'Retrying downstream request' recurred 1067 time(s), including a burst of 226 within 15 minute(s)

- Occurrences: 1067
- First seen: 2026-08-01 09:00:06.780000+00:00
- Last seen: 2026-08-01 10:19:02.041000+00:00
- Affected sources: application, docker, plc
### 'Database connection pool above threshold' recurred 1010 time(s), including a burst of 219 within 15 minute(s)

- Occurrences: 1010
- First seen: 2026-08-01 09:00:05.728000+00:00
- Last seen: 2026-08-01 10:19:00.326000+00:00
- Affected sources: application, docker, plc
### 'Unhandled exception in order processing' recurred 391 time(s), including a burst of 97 within 15 minute(s)

- Occurrences: 391
- First seen: 2026-08-01 09:00:13.453000+00:00
- Last seen: 2026-08-01 10:18:59.493000+00:00
- Affected sources: application, docker, plc
### 'ECONNRESET while calling payment gateway' recurred 389 time(s), including a burst of 91 within 15 minute(s)

- Occurrences: 389
- First seen: 2026-08-01 09:00:12.870000+00:00
- Last seen: 2026-08-01 10:19:06.541000+00:00
- Affected sources: application, docker, plc
### 'UnhandledPromiseRejection: TypeError: Cannot read properties of undefined' recurred 370 time(s), including a burst of 92 within 15 minute(s)

- Occurrences: 370
- First seen: 2026-08-01 09:00:16.775000+00:00
- Last seen: 2026-08-01 10:19:42.603000+00:00
- Affected sources: application, docker, plc
### 'Docker container exited unexpectedly' recurred 359 time(s), including a burst of 90 within 15 minute(s)

- Occurrences: 359
- First seen: 2026-08-01 09:00:14.104000+00:00
- Last seen: 2026-08-01 10:19:04.726000+00:00
- Affected sources: application, docker, plc
### 'JWT verification failed' recurred 347 time(s), including a burst of 81 within 15 minute(s)

- Occurrences: 347
- First seen: 2026-08-01 09:00:46.683000+00:00
- Last seen: 2026-08-01 10:19:28.234000+00:00
- Affected sources: application, docker, plc
### 'Redis connection lost' recurred 328 time(s), including a burst of 76 within 15 minute(s)

- Occurrences: 328
- First seen: 2026-08-01 09:00:04.529000+00:00
- Last seen: 2026-08-01 10:18:42.788000+00:00
- Affected sources: application, docker, plc
### Correlation group `corr-0193`

- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-02
- Window: 2026-08-01 09:50:51.839000+00:00 -> 2026-08-01 09:51:21.018000+00:00
- Confidence: 0.60

## Timeline of Important Events

- **2026-08-01 09:00:01.180000+00:00** [first_critical_error] First critical error -- First ERROR/CRITICAL event: 'PLC communication timeout' on payment-service@wilston-prod-03
- **2026-08-01 09:00:14.104000+00:00** [fatal_event] Fatal: Docker container exited unexpectedly -- First FATAL occurrence of 'Docker container exited unexpectedly' on notification-service@wilston-prod-03
- **2026-08-01 09:00:25.866000+00:00** [fatal_event] Fatal: ECONNRESET while calling payment gateway -- First FATAL occurrence of 'ECONNRESET while calling payment gateway' on payment-service@wilston-prod-02
- **2026-08-01 09:00:30.780000+00:00** [fatal_event] Fatal: Redis connection lost -- First FATAL occurrence of 'Redis connection lost' on api-gateway@wilston-prod-03
- **2026-08-01 09:00:39.409000+00:00** [fatal_event] Fatal: Kafka publish failed -- First FATAL occurrence of 'Kafka publish failed' on notification-service@wilston-prod-01
- **2026-08-01 09:00:43.174000+00:00** [fatal_event] Fatal: PLC communication timeout -- First FATAL occurrence of 'PLC communication timeout' on order-service@wilston-prod-02
- **2026-08-01 09:00:51.993000+00:00** [fatal_event] Fatal: PostgreSQL error: deadlock detected -- First FATAL occurrence of 'PostgreSQL error: deadlock detected' on order-service@wilston-prod-03
- **2026-08-01 09:01:54.029000+00:00** [fatal_event] Fatal: Unhandled exception in order processing -- First FATAL occurrence of 'Unhandled exception in order processing' on order-service@wilston-prod-01
- **2026-08-01 09:02:06.014000+00:00** [fatal_event] Fatal: UnhandledPromiseRejection: TypeError: Cannot read properties of undefined -- First FATAL occurrence of 'UnhandledPromiseRejection: TypeError: Cannot read properties of undefined' on notification-service@wilston-prod-02
- **2026-08-01 09:03:11.816000+00:00** [fatal_event] Fatal: JWT verification failed -- First FATAL occurrence of 'JWT verification failed' on auth-service@wilston-prod-02
- **2026-08-01 09:03:39.818000+00:00** [fatal_event] Fatal: MongoNetworkError: connection timed out -- First FATAL occurrence of 'MongoNetworkError: connection timed out' on api-gateway@wilston-prod-02
- **2026-08-01 09:04:38.661000+00:00** [recovery_event] Incident corr-0015 resolved -- All 3 component/host pair(s) involved in incident corr-0015 showed normal activity again by this point
- **2026-08-01 09:04:39.521000+00:00** [recovery_event] Incident corr-0017 resolved -- All 1 component/host pair(s) involved in incident corr-0017 showed normal activity again by this point
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
- **2026-08-01 09:21:32.448000+00:00** [recovery_event] Incident corr-0088 resolved -- All 2 component/host pair(s) involved in incident corr-0088 showed normal activity again by this point
- **2026-08-01 09:22:33.317000+00:00** [recovery_event] Incident corr-0091 resolved -- All 5 component/host pair(s) involved in incident corr-0091 showed normal activity again by this point
- **2026-08-01 09:23:06.914000+00:00** [recovery_event] Incident corr-0095 resolved -- All 3 component/host pair(s) involved in incident corr-0095 showed normal activity again by this point
- **2026-08-01 09:26:58.163000+00:00** [recovery_event] Incident corr-0111 resolved -- All 3 component/host pair(s) involved in incident corr-0111 showed normal activity again by this point
- **2026-08-01 09:30:35.593000+00:00** [recovery_event] Incident corr-0122 resolved -- All 1 component/host pair(s) involved in incident corr-0122 showed normal activity again by this point
- **2026-08-01 09:34:25.870000+00:00** [recovery_event] Incident corr-0133 resolved -- All 2 component/host pair(s) involved in incident corr-0133 showed normal activity again by this point
- **2026-08-01 09:35:21.459000+00:00** [recovery_event] Incident corr-0135 resolved -- All 3 component/host pair(s) involved in incident corr-0135 showed normal activity again by this point
- **2026-08-01 09:35:28.905000+00:00** [recovery_event] Incident corr-0138 resolved -- All 2 component/host pair(s) involved in incident corr-0138 showed normal activity again by this point
- **2026-08-01 09:37:53.490000+00:00** [recovery_event] Incident corr-0145 resolved -- All 3 component/host pair(s) involved in incident corr-0145 showed normal activity again by this point
- **2026-08-01 09:39:30.603000+00:00** [recovery_event] Incident corr-0153 resolved -- All 4 component/host pair(s) involved in incident corr-0153 showed normal activity again by this point
- **2026-08-01 09:44:13.439000+00:00** [recovery_event] Incident corr-0167 resolved -- All 6 component/host pair(s) involved in incident corr-0167 showed normal activity again by this point
- **2026-08-01 09:46:10.917000+00:00** [recovery_event] Incident corr-0174 resolved -- All 6 component/host pair(s) involved in incident corr-0174 showed normal activity again by this point
- **2026-08-01 09:50:54.103000+00:00** [recovery_event] Incident corr-0191 resolved -- All 2 component/host pair(s) involved in incident corr-0191 showed normal activity again by this point
- **2026-08-01 09:51:30.486000+00:00** [recovery_event] Incident corr-0193 resolved -- All 6 component/host pair(s) involved in incident corr-0193 showed normal activity again by this point
- **2026-08-01 09:53:02.316000+00:00** [recovery_event] Incident corr-0199 resolved -- All 4 component/host pair(s) involved in incident corr-0199 showed normal activity again by this point
- **2026-08-01 09:53:03.156000+00:00** [recovery_event] Incident corr-0201 resolved -- All 2 component/host pair(s) involved in incident corr-0201 showed normal activity again by this point
- **2026-08-01 09:55:25.949000+00:00** [recovery_event] Incident corr-0213 resolved -- All 2 component/host pair(s) involved in incident corr-0213 showed normal activity again by this point
- **2026-08-01 09:58:12.630000+00:00** [recovery_event] Incident corr-0222 resolved -- All 4 component/host pair(s) involved in incident corr-0222 showed normal activity again by this point
- **2026-08-01 09:59:13.813000+00:00** [recovery_event] Incident corr-0226 resolved -- All 4 component/host pair(s) involved in incident corr-0226 showed normal activity again by this point
- **2026-08-01 10:00:34.836000+00:00** [recovery_event] Incident corr-0230 resolved -- All 3 component/host pair(s) involved in incident corr-0230 showed normal activity again by this point
- **2026-08-01 10:01:47.238000+00:00** [recovery_event] Incident corr-0236 resolved -- All 2 component/host pair(s) involved in incident corr-0236 showed normal activity again by this point
- **2026-08-01 10:03:21.583000+00:00** [recovery_event] Incident corr-0241 resolved -- All 4 component/host pair(s) involved in incident corr-0241 showed normal activity again by this point
- **2026-08-01 10:09:31.494000+00:00** [recovery_event] Incident corr-0264 resolved -- All 2 component/host pair(s) involved in incident corr-0264 showed normal activity again by this point
- **2026-08-01 10:16:55.504000+00:00** [recovery_event] Incident corr-0288 resolved -- All 3 component/host pair(s) involved in incident corr-0288 showed normal activity again by this point
- **2026-08-01 10:17:21.799000+00:00** [recovery_event] Incident corr-0290 resolved -- All 2 component/host pair(s) involved in incident corr-0290 showed normal activity again by this point
- **2026-08-01 10:18:20.417000+00:00** [recovery_event] Incident corr-0294 resolved -- All 3 component/host pair(s) involved in incident corr-0294 showed normal activity again by this point

## Root Cause Analysis

### (high likelihood) Payment provider performed unannounced maintenance that closed idle connections mid-request

- ECONNRESET while calling payment gateway
- BURST: 97 occurrences in one window starting 2026-08-01T09:44:33.772000+00:00
### (low likelihood) Connection reset-aware retry logic and shortened idle-connection keep-alive interval not implemented

- ECONNRESET while calling payment gateway
- BURST: 97 occurrences in one window starting 2026-08-01T09:44:33.772000+00:00

**How this conclusion was reached:** Based on the historical incident precedent, it is likely that the unannounced maintenance performed by the payment provider caused the ECONNRESET spikes. The current incident's severity and similarity to the previous incident support this conclusion.

**Open questions:**
- What was the exact duration of the payment provider's maintenance window?
- Were there any other services affected by the ECONNRESET spikes?

## Supporting Evidence

- ECONNRESET while calling payment gateway
- BURST: 97 occurrences in one window starting 2026-08-01T09:44:33.772000+00:00

## Similar Historical Incidents

- **Payment gateway ECONNRESET spikes during provider maintenance** (similarity: 0.80)
  The payment service saw a burst of ECONNRESET errors calling the external payment gateway.
- **Unhandled exceptions in order processing after a schema change** (similarity: 0.69)
  The order service began throwing unhandled exceptions while processing a subset of orders after a backward-incompatible field rename in an upstream event schema.
- **Redis cache outage causing cascading latency** (similarity: 0.69)
  Redis connection pool exhausted after a network partition, leading to cache misses and connection resets across auth and gateway services.
- **Docker containers exiting unexpectedly under memory pressure** (similarity: 0.69)
  Multiple service containers were OOM-killed during a traffic spike.
- **Kafka publish failures during broker rebalance** (similarity: 0.67)
  Order and notification events failed to publish to Kafka during a rolling broker restart.

LLM-cited historical incidents (attributed precedent, not current fact):
- inc-007: Payment gateway ECONNRESET spikes during provider maintenance -- Similar incident with a similar root cause, but the current incident is more severe due to the unannounced maintenance

## Recommended Fixes

- Implement connection reset-aware retry logic and shorten idle-connection keep-alive interval
- Notify payment provider of upcoming maintenance window to avoid similar incidents in the future

## Confidence Level

**high**
