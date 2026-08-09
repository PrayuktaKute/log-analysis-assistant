# Appendix: Minor / Low-Confidence Incidents

- **Generated:** 2026-08-08T07:07:12.226398+00:00
- **Incident count:** 248

These incidents did not meet the correlation-confidence bar for an individual AI-generated
investigation (either a single repeated-failure pattern with no corroborating correlated event, or a
correlated event below the configured confidence threshold). They are summarized briefly below rather
than as full reports.

## incident-corr-0001 -- Docker container exited unexpectedly

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "PLC communication timeout" (347x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Docker containers exiting unexpectedly under memory pressure (similarity: 0.75)
## incident-corr-0002 -- Kafka publish failed

- Severity: ERROR
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02
- Failure pattern(s): "Slow response detected" (1090x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "Kafka publish failed" (367x), "MongoNetworkError: connection timed out" (338x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.79)
## incident-corr-0003 -- Kafka publish failed

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.82)
## incident-corr-0004 -- Kafka publish failed

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: auth-service, inventory-service, order-service
- Hosts: wilston-prod-01, wilston-prod-02
- Failure pattern(s): "Memory usage high" (1119x), "Retrying downstream request" (1067x), "Kafka publish failed" (367x), "Redis connection lost" (328x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.84)
## incident-corr-0005 -- Docker container exited unexpectedly

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: Docker containers exiting unexpectedly under memory pressure (similarity: 0.76)
## incident-corr-0006 -- PLC communication timeout

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: PLC communication timeouts on shop-floor integration (similarity: 0.75)
## incident-corr-0007 -- Kafka publish failed

- Severity: ERROR
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.79)
## incident-corr-0008 -- PLC communication timeout

- Severity: ERROR
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service
- Hosts: wilston-prod-01, wilston-prod-02
- Failure pattern(s): "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "PLC communication timeout" (347x)
- Closest historical incident: PLC communication timeouts on shop-floor integration (similarity: 0.84)
## incident-corr-0009 -- PostgreSQL error: deadlock detected

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Recurring PostgreSQL deadlocks under high order volume (similarity: 0.79)
## incident-corr-0010 -- Kafka publish failed

- Severity: ERROR
- Correlation confidence: 0.38
- Components: order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-03
- Failure pattern(s): "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Kafka publish failed" (367x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.84)
## incident-corr-0011 -- Docker container exited unexpectedly

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Docker containers exiting unexpectedly under memory pressure (similarity: 0.76)
## incident-corr-0012 -- JWT verification failed

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.74)
## incident-corr-0013 -- MongoNetworkError: connection timed out

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: MongoDB connection timeouts during replica set election (similarity: 0.75)
## incident-corr-0014 -- Redis connection lost

- Severity: ERROR
- Correlation confidence: 0.40
- Components: inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "Redis connection lost" (328x)
- Closest historical incident: Redis cache outage causing cascading latency (similarity: 0.74)
## incident-corr-0016 -- Unhandled exception in order processing

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: auth-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "Kafka publish failed" (367x), "JWT verification failed" (347x)
- Closest historical incident: Unhandled exceptions in order processing after a schema change (similarity: 0.78)
## incident-corr-0018 -- Docker container exited unexpectedly

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Docker containers exiting unexpectedly under memory pressure (similarity: 0.76)
## incident-corr-0019 -- Redis connection lost

- Severity: ERROR
- Correlation confidence: 0.40
- Components: api-gateway, inventory-service, notification-service
- Hosts: wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Slow response detected" (1090x), "Database connection pool above threshold" (1010x), "Redis connection lost" (328x)
- Closest historical incident: Redis cache outage causing cascading latency (similarity: 0.76)
## incident-corr-0020 -- PostgreSQL error: deadlock detected

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Recurring PostgreSQL deadlocks under high order volume (similarity: 0.79)
## incident-corr-0021 -- Database connection pool above threshold

- Severity: WARNING
- Correlation confidence: 0.40
- Components: api-gateway, inventory-service, notification-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x)
- Closest historical incident: Elevated memory usage across services from a slow memory leak (similarity: 0.75)
## incident-corr-0022 -- UnhandledPromiseRejection: TypeError: Cannot read properties of undefined

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: auth-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "External API latency increased" (1076x), "Unhandled exception in order processing" (391x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "PLC communication timeout" (347x), "Redis connection lost" (328x)
- Closest historical incident: Unhandled exceptions in order processing after a schema change (similarity: 0.72)
## incident-corr-0023 -- PostgreSQL error: deadlock detected

- Severity: ERROR
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02
- Failure pattern(s): "Slow response detected" (1090x), "External API latency increased" (1076x), "Database connection pool above threshold" (1010x), "JWT verification failed" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: Recurring PostgreSQL deadlocks under high order volume (similarity: 0.79)
## incident-corr-0024 -- Unhandled exception in order processing

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: Unhandled exceptions in order processing after a schema change (similarity: 0.77)
## incident-corr-0025 -- Redis connection lost

- Severity: ERROR
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Docker container exited unexpectedly" (359x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "Redis connection lost" (328x)
- Closest historical incident: Redis cache outage causing cascading latency (similarity: 0.76)
## incident-corr-0026 -- ECONNRESET while calling payment gateway

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "ECONNRESET while calling payment gateway" (389x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Payment gateway ECONNRESET spikes during provider maintenance (similarity: 0.81)
## incident-corr-0027 -- Docker container exited unexpectedly

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: Docker containers exiting unexpectedly under memory pressure (similarity: 0.77)
## incident-corr-0028 -- Docker container exited unexpectedly

- Severity: ERROR
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x)
- Closest historical incident: Docker containers exiting unexpectedly under memory pressure (similarity: 0.76)
## incident-corr-0029 -- PostgreSQL error: deadlock detected

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Recurring PostgreSQL deadlocks under high order volume (similarity: 0.79)
## incident-corr-0030 -- Unhandled exception in order processing

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, inventory-service, payment-service
- Hosts: wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Unhandled exception in order processing" (391x), "Kafka publish failed" (367x), "JWT verification failed" (347x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.78)
## incident-corr-0031 -- PLC communication timeout

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: PLC communication timeouts on shop-floor integration (similarity: 0.76)
## incident-corr-0032 -- Unhandled exception in order processing

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "JWT verification failed" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Recurring PostgreSQL deadlocks under high order volume (similarity: 0.76)
## incident-corr-0033 -- JWT verification failed

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "Unhandled exception in order processing" (391x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.73)
## incident-corr-0034 -- PostgreSQL error: deadlock detected

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Recurring PostgreSQL deadlocks under high order volume (similarity: 0.80)
## incident-corr-0035 -- Docker container exited unexpectedly

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "Redis connection lost" (328x)
- Closest historical incident: Docker containers exiting unexpectedly under memory pressure (similarity: 0.75)
## incident-corr-0036 -- PostgreSQL error: deadlock detected

- Severity: ERROR
- Correlation confidence: 0.40
- Components: auth-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-02, wilston-prod-03
- Failure pattern(s): "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: Recurring PostgreSQL deadlocks under high order volume (similarity: 0.81)
## incident-corr-0038 -- Unhandled exception in order processing

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "MongoNetworkError: connection timed out" (338x), "Redis connection lost" (328x)
- Closest historical incident: Unhandled exceptions in order processing after a schema change (similarity: 0.78)
## incident-corr-0039 -- Kafka publish failed

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.81)
## incident-corr-0041 -- Docker container exited unexpectedly

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: Docker containers exiting unexpectedly under memory pressure (similarity: 0.76)
## incident-corr-0043 -- PostgreSQL error: deadlock detected

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Database connection pool above threshold" (1010x), "JWT verification failed" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Recurring PostgreSQL deadlocks under high order volume (similarity: 0.79)
## incident-corr-0044 -- Redis connection lost

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Redis cache outage causing cascading latency (similarity: 0.77)
## incident-corr-0045 -- PLC communication timeout

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Database connection pool above threshold" (1010x), "ECONNRESET while calling payment gateway" (389x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: PLC communication timeouts on shop-floor integration (similarity: 0.79)
## incident-corr-0046 -- MongoNetworkError: connection timed out

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: MongoDB connection timeouts during replica set election (similarity: 0.74)
## incident-corr-0048 -- Docker container exited unexpectedly

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "PLC communication timeout" (347x)
- Closest historical incident: Docker containers exiting unexpectedly under memory pressure (similarity: 0.77)
## incident-corr-0049 -- ECONNRESET while calling payment gateway

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "ECONNRESET while calling payment gateway" (389x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: Payment gateway ECONNRESET spikes during provider maintenance (similarity: 0.84)
## incident-corr-0050 -- PLC communication timeout

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "Database connection pool above threshold" (1010x), "ECONNRESET while calling payment gateway" (389x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: PLC communication timeouts on shop-floor integration (similarity: 0.78)
## incident-corr-0051 -- PostgreSQL error: deadlock detected

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Recurring PostgreSQL deadlocks under high order volume (similarity: 0.78)
## incident-corr-0052 -- PostgreSQL error: deadlock detected

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: inventory-service, notification-service, order-service
- Hosts: wilston-prod-01, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "External API latency increased" (1076x), "Database connection pool above threshold" (1010x), "Docker container exited unexpectedly" (359x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: Recurring PostgreSQL deadlocks under high order volume (similarity: 0.81)
## incident-corr-0053 -- Unhandled exception in order processing

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.77)
## incident-corr-0054 -- Kafka publish failed

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.80)
## incident-corr-0055 -- MongoNetworkError: connection timed out

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: auth-service, inventory-service, notification-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02
- Failure pattern(s): "Memory usage high" (1119x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "JWT verification failed" (347x), "MongoNetworkError: connection timed out" (338x)
- Closest historical incident: MongoDB connection timeouts during replica set election (similarity: 0.74)
## incident-corr-0056 -- Kafka publish failed

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "Redis connection lost" (328x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.79)
## incident-corr-0057 -- PostgreSQL error: deadlock detected

- Severity: ERROR
- Correlation confidence: 0.40
- Components: api-gateway, inventory-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Slow response detected" (1090x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "Docker container exited unexpectedly" (359x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: Recurring PostgreSQL deadlocks under high order volume (similarity: 0.81)
## incident-corr-0060 -- PLC communication timeout

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "Redis connection lost" (328x)
- Closest historical incident: PLC communication timeouts on shop-floor integration (similarity: 0.75)
## incident-corr-0061 -- Kafka publish failed

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.80)
## incident-corr-0062 -- Unhandled exception in order processing

- Severity: ERROR
- Correlation confidence: 0.40
- Components: api-gateway, inventory-service, payment-service
- Hosts: wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x)
- Closest historical incident: Unhandled exceptions in order processing after a schema change (similarity: 0.77)
## incident-corr-0063 -- PLC communication timeout

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: PLC communication timeouts on shop-floor integration (similarity: 0.77)
## incident-corr-0064 -- MongoNetworkError: connection timed out

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Database connection pool above threshold" (1010x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x)
- Closest historical incident: MongoDB connection timeouts during replica set election (similarity: 0.74)
## incident-corr-0065 -- UnhandledPromiseRejection: TypeError: Cannot read properties of undefined

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "JWT verification failed" (347x), "MongoNetworkError: connection timed out" (338x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.74)
## incident-corr-0066 -- PLC communication timeout

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: PLC communication timeouts on shop-floor integration (similarity: 0.76)
## incident-corr-0067 -- MongoNetworkError: connection timed out

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: MongoDB connection timeouts during replica set election (similarity: 0.75)
## incident-corr-0068 -- Unhandled exception in order processing

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Unhandled exceptions in order processing after a schema change (similarity: 0.76)
## incident-corr-0069 -- Kafka publish failed

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "Redis connection lost" (328x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.79)
## incident-corr-0070 -- Redis connection lost

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Redis cache outage causing cascading latency (similarity: 0.77)
## incident-corr-0071 -- UnhandledPromiseRejection: TypeError: Cannot read properties of undefined

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "Redis connection lost" (328x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.74)
## incident-corr-0073 -- ECONNRESET while calling payment gateway

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Payment gateway ECONNRESET spikes during provider maintenance (similarity: 0.85)
## incident-corr-0074 -- UnhandledPromiseRejection: TypeError: Cannot read properties of undefined

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, order-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.70)
## incident-corr-0078 -- Kafka publish failed

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "JWT verification failed" (347x), "Redis connection lost" (328x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.79)
## incident-corr-0079 -- UnhandledPromiseRejection: TypeError: Cannot read properties of undefined

- Severity: ERROR
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, notification-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02
- Failure pattern(s): "Memory usage high" (1119x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "JWT verification failed" (347x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.75)
## incident-corr-0080 -- Kafka publish failed

- Severity: ERROR
- Correlation confidence: 0.40
- Components: api-gateway, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "External API latency increased" (1076x), "Database connection pool above threshold" (1010x), "ECONNRESET while calling payment gateway" (389x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "MongoNetworkError: connection timed out" (338x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.80)
## incident-corr-0083 -- UnhandledPromiseRejection: TypeError: Cannot read properties of undefined

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.73)
## incident-corr-0084 -- PLC communication timeout

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Recurring PostgreSQL deadlocks under high order volume (similarity: 0.75)
## incident-corr-0085 -- PostgreSQL error: deadlock detected

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "ECONNRESET while calling payment gateway" (389x), "Kafka publish failed" (367x), "PLC communication timeout" (347x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Recurring PostgreSQL deadlocks under high order volume (similarity: 0.80)
## incident-corr-0087 -- JWT verification failed

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: notification-service, payment-service
- Hosts: wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.73)
## incident-corr-0089 -- MongoNetworkError: connection timed out

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: MongoDB connection timeouts during replica set election (similarity: 0.75)
## incident-corr-0090 -- PLC communication timeout

- Severity: ERROR
- Correlation confidence: 0.34
- Components: auth-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02
- Failure pattern(s): "JWT verification failed" (347x), "PLC communication timeout" (347x)
- Closest historical incident: PLC communication timeouts on shop-floor integration (similarity: 0.76)
## incident-corr-0092 -- PLC communication timeout

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: PLC communication timeouts on shop-floor integration (similarity: 0.77)
## incident-corr-0093 -- Redis connection lost

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Redis cache outage causing cascading latency (similarity: 0.78)
## incident-corr-0094 -- ECONNRESET while calling payment gateway

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Slow response detected" (1090x), "Database connection pool above threshold" (1010x), "ECONNRESET while calling payment gateway" (389x), "MongoNetworkError: connection timed out" (338x)
- Closest historical incident: Payment gateway ECONNRESET spikes during provider maintenance (similarity: 0.82)
## incident-corr-0096 -- ECONNRESET while calling payment gateway

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Payment gateway ECONNRESET spikes during provider maintenance (similarity: 0.80)
## incident-corr-0097 -- MongoNetworkError: connection timed out

- Severity: ERROR
- Correlation confidence: 0.40
- Components: auth-service, notification-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02
- Failure pattern(s): "Slow response detected" (1090x), "Database connection pool above threshold" (1010x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: MongoDB connection timeouts during replica set election (similarity: 0.75)
## incident-corr-0098 -- Redis connection lost

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, order-service, payment-service
- Hosts: wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "Redis connection lost" (328x)
- Closest historical incident: Redis cache outage causing cascading latency (similarity: 0.75)
## incident-corr-0099 -- MongoNetworkError: connection timed out

- Severity: CRITICAL
- Correlation confidence: 0.36
- Components: auth-service, notification-service, payment-service
- Hosts: wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Database connection pool above threshold" (1010x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "MongoNetworkError: connection timed out" (338x)
- Closest historical incident: MongoDB connection timeouts during replica set election (similarity: 0.74)
## incident-corr-0100 -- PLC communication timeout

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: PLC communication timeouts on shop-floor integration (similarity: 0.76)
## incident-corr-0101 -- ECONNRESET while calling payment gateway

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "Docker container exited unexpectedly" (359x), "PLC communication timeout" (347x)
- Closest historical incident: Payment gateway ECONNRESET spikes during provider maintenance (similarity: 0.86)
## incident-corr-0102 -- PostgreSQL error: deadlock detected

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: Recurring PostgreSQL deadlocks under high order volume (similarity: 0.80)
## incident-corr-0103 -- Kafka publish failed

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.80)
## incident-corr-0104 -- Unhandled exception in order processing

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "Redis connection lost" (328x)
- Closest historical incident: Unhandled exceptions in order processing after a schema change (similarity: 0.76)
## incident-corr-0105 -- PLC communication timeout

- Severity: ERROR
- Correlation confidence: 0.40
- Components: api-gateway, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-03
- Failure pattern(s): "Slow response detected" (1090x), "Retrying downstream request" (1067x), "ECONNRESET while calling payment gateway" (389x), "PLC communication timeout" (347x)
- Closest historical incident: PLC communication timeouts on shop-floor integration (similarity: 0.81)
## incident-corr-0106 -- Docker container exited unexpectedly

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, inventory-service, notification-service
- Hosts: wilston-prod-01, wilston-prod-02
- Failure pattern(s): "Memory usage high" (1119x), "Unhandled exception in order processing" (391x), "Docker container exited unexpectedly" (359x), "Redis connection lost" (328x)
- Closest historical incident: Docker containers exiting unexpectedly under memory pressure (similarity: 0.79)
## incident-corr-0107 -- Kafka publish failed

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.80)
## incident-corr-0108 -- PLC communication timeout

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "Kafka publish failed" (367x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: PLC communication timeouts on shop-floor integration (similarity: 0.79)
## incident-corr-0109 -- JWT verification failed

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Redis cache outage causing cascading latency (similarity: 0.74)
## incident-corr-0112 -- PostgreSQL error: deadlock detected

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Recurring PostgreSQL deadlocks under high order volume (similarity: 0.79)
## incident-corr-0113 -- UnhandledPromiseRejection: TypeError: Cannot read properties of undefined

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Unhandled exceptions in order processing after a schema change (similarity: 0.71)
## incident-corr-0114 -- PostgreSQL error: deadlock detected

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Recurring PostgreSQL deadlocks under high order volume (similarity: 0.79)
## incident-corr-0115 -- JWT verification failed

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Recurring PostgreSQL deadlocks under high order volume (similarity: 0.74)
## incident-corr-0116 -- Docker container exited unexpectedly

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Docker containers exiting unexpectedly under memory pressure (similarity: 0.76)
## incident-corr-0117 -- Docker container exited unexpectedly

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: Docker containers exiting unexpectedly under memory pressure (similarity: 0.76)
## incident-corr-0118 -- Redis connection lost

- Severity: CRITICAL
- Correlation confidence: 0.36
- Components: auth-service, inventory-service, notification-service
- Hosts: wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Retrying downstream request" (1067x), "Redis connection lost" (328x)
- Closest historical incident: Redis cache outage causing cascading latency (similarity: 0.74)
## incident-corr-0119 -- JWT verification failed

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.74)
## incident-corr-0120 -- UnhandledPromiseRejection: TypeError: Cannot read properties of undefined

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Unhandled exception in order processing" (391x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Docker container exited unexpectedly" (359x)
- Closest historical incident: Docker containers exiting unexpectedly under memory pressure (similarity: 0.74)
## incident-corr-0121 -- Kafka publish failed

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "ECONNRESET while calling payment gateway" (389x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.80)
## incident-corr-0123 -- PostgreSQL error: deadlock detected

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: Recurring PostgreSQL deadlocks under high order volume (similarity: 0.80)
## incident-corr-0124 -- ECONNRESET while calling payment gateway

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, inventory-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02
- Failure pattern(s): "Slow response detected" (1090x), "Database connection pool above threshold" (1010x), "ECONNRESET while calling payment gateway" (389x), "Kafka publish failed" (367x)
- Closest historical incident: Payment gateway ECONNRESET spikes during provider maintenance (similarity: 0.82)
## incident-corr-0125 -- JWT verification failed

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.75)
## incident-corr-0126 -- UnhandledPromiseRejection: TypeError: Cannot read properties of undefined

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.74)
## incident-corr-0127 -- Kafka publish failed

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "Redis connection lost" (328x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.79)
## incident-corr-0128 -- PLC communication timeout

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Redis cache outage causing cascading latency (similarity: 0.75)
## incident-corr-0129 -- PLC communication timeout

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Redis cache outage causing cascading latency (similarity: 0.75)
## incident-corr-0130 -- UnhandledPromiseRejection: TypeError: Cannot read properties of undefined

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.74)
## incident-corr-0131 -- PostgreSQL error: deadlock detected

- Severity: ERROR
- Correlation confidence: 0.40
- Components: api-gateway, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "JWT verification failed" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Recurring PostgreSQL deadlocks under high order volume (similarity: 0.80)
## incident-corr-0132 -- PostgreSQL error: deadlock detected

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Recurring PostgreSQL deadlocks under high order volume (similarity: 0.79)
## incident-corr-0134 -- Docker container exited unexpectedly

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Docker containers exiting unexpectedly under memory pressure (similarity: 0.76)
## incident-corr-0136 -- Kafka publish failed

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "JWT verification failed" (347x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.79)
## incident-corr-0137 -- Unhandled exception in order processing

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Docker container exited unexpectedly" (359x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: Unhandled exceptions in order processing after a schema change (similarity: 0.76)
## incident-corr-0139 -- PostgreSQL error: deadlock detected

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Recurring PostgreSQL deadlocks under high order volume (similarity: 0.79)
## incident-corr-0140 -- PostgreSQL error: deadlock detected

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: Recurring PostgreSQL deadlocks under high order volume (similarity: 0.80)
## incident-corr-0141 -- UnhandledPromiseRejection: TypeError: Cannot read properties of undefined

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x)
- Closest historical incident: Unhandled exceptions in order processing after a schema change (similarity: 0.71)
## incident-corr-0142 -- MongoNetworkError: connection timed out

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Docker container exited unexpectedly" (359x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: MongoDB connection timeouts during replica set election (similarity: 0.74)
## incident-corr-0143 -- Kafka publish failed

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "ECONNRESET while calling payment gateway" (389x), "Kafka publish failed" (367x), "JWT verification failed" (347x), "PLC communication timeout" (347x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.83)
## incident-corr-0144 -- Unhandled exception in order processing

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Docker container exited unexpectedly" (359x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Unhandled exceptions in order processing after a schema change (similarity: 0.76)
## incident-corr-0146 -- JWT verification failed

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "JWT verification failed" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: Recurring PostgreSQL deadlocks under high order volume (similarity: 0.75)
## incident-corr-0147 -- PLC communication timeout

- Severity: ERROR
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Unhandled exception in order processing" (391x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.75)
## incident-corr-0148 -- MongoNetworkError: connection timed out

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: MongoDB connection timeouts during replica set election (similarity: 0.75)
## incident-corr-0149 -- Docker container exited unexpectedly

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, payment-service
- Hosts: wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Database connection pool above threshold" (1010x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Docker container exited unexpectedly" (359x)
- Closest historical incident: Docker containers exiting unexpectedly under memory pressure (similarity: 0.77)
## incident-corr-0150 -- Docker container exited unexpectedly

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: Docker containers exiting unexpectedly under memory pressure (similarity: 0.78)
## incident-corr-0152 -- Unhandled exception in order processing

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Unhandled exceptions in order processing after a schema change (similarity: 0.76)
## incident-corr-0154 -- MongoNetworkError: connection timed out

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "Redis connection lost" (328x)
- Closest historical incident: MongoDB connection timeouts during replica set election (similarity: 0.75)
## incident-corr-0155 -- JWT verification failed

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "MongoNetworkError: connection timed out" (338x), "Redis connection lost" (328x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.74)
## incident-corr-0156 -- PostgreSQL error: deadlock detected

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Recurring PostgreSQL deadlocks under high order volume (similarity: 0.79)
## incident-corr-0157 -- JWT verification failed

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Database connection pool above threshold" (1010x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.76)
## incident-corr-0158 -- Unhandled exception in order processing

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.77)
## incident-corr-0160 -- Redis connection lost

- Severity: ERROR
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "Kafka publish failed" (367x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Redis cache outage causing cascading latency (similarity: 0.79)
## incident-corr-0161 -- Unhandled exception in order processing

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, notification-service, payment-service
- Hosts: wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "PLC communication timeout" (347x)
- Closest historical incident: Unhandled exceptions in order processing after a schema change (similarity: 0.81)
## incident-corr-0162 -- Redis connection lost

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Redis cache outage causing cascading latency (similarity: 0.77)
## incident-corr-0163 -- JWT verification failed

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.74)
## incident-corr-0164 -- PLC communication timeout

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Recurring PostgreSQL deadlocks under high order volume (similarity: 0.76)
## incident-corr-0165 -- MongoNetworkError: connection timed out

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "Redis connection lost" (328x)
- Closest historical incident: MongoDB connection timeouts during replica set election (similarity: 0.74)
## incident-corr-0166 -- UnhandledPromiseRejection: TypeError: Cannot read properties of undefined

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.74)
## incident-corr-0168 -- JWT verification failed

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "Kafka publish failed" (367x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.78)
## incident-corr-0169 -- PLC communication timeout

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "PLC communication timeout" (347x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Recurring PostgreSQL deadlocks under high order volume (similarity: 0.77)
## incident-corr-0170 -- Kafka publish failed

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, notification-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "Kafka publish failed" (367x), "MongoNetworkError: connection timed out" (338x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.80)
## incident-corr-0171 -- Docker container exited unexpectedly

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Docker containers exiting unexpectedly under memory pressure (similarity: 0.76)
## incident-corr-0172 -- Docker container exited unexpectedly

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Docker containers exiting unexpectedly under memory pressure (similarity: 0.76)
## incident-corr-0173 -- Kafka publish failed

- Severity: ERROR
- Correlation confidence: 0.38
- Components: inventory-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02
- Failure pattern(s): "External API latency increased" (1076x), "Retrying downstream request" (1067x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "PLC communication timeout" (347x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.80)
## incident-corr-0175 -- Redis connection lost

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "PLC communication timeout" (347x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Redis cache outage causing cascading latency (similarity: 0.77)
## incident-corr-0176 -- PLC communication timeout

- Severity: ERROR
- Correlation confidence: 0.40
- Components: api-gateway, inventory-service, order-service
- Hosts: wilston-prod-01, wilston-prod-02
- Failure pattern(s): "Memory usage high" (1119x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Kafka publish failed" (367x), "PLC communication timeout" (347x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.80)
## incident-corr-0177 -- JWT verification failed

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.74)
## incident-corr-0178 -- Redis connection lost

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Redis cache outage causing cascading latency (similarity: 0.78)
## incident-corr-0179 -- PLC communication timeout

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Docker container exited unexpectedly" (359x), "PLC communication timeout" (347x)
- Closest historical incident: PLC communication timeouts on shop-floor integration (similarity: 0.76)
## incident-corr-0180 -- PostgreSQL error: deadlock detected

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Recurring PostgreSQL deadlocks under high order volume (similarity: 0.79)
## incident-corr-0181 -- Unhandled exception in order processing

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.77)
## incident-corr-0182 -- UnhandledPromiseRejection: TypeError: Cannot read properties of undefined

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "Redis connection lost" (328x)
- Closest historical incident: Docker containers exiting unexpectedly under memory pressure (similarity: 0.70)
## incident-corr-0184 -- MongoNetworkError: connection timed out

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "Redis connection lost" (328x)
- Closest historical incident: MongoDB connection timeouts during replica set election (similarity: 0.75)
## incident-corr-0185 -- PostgreSQL error: deadlock detected

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "ECONNRESET while calling payment gateway" (389x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: Recurring PostgreSQL deadlocks under high order volume (similarity: 0.81)
## incident-corr-0186 -- PostgreSQL error: deadlock detected

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "Unhandled exception in order processing" (391x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "JWT verification failed" (347x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Recurring PostgreSQL deadlocks under high order volume (similarity: 0.79)
## incident-corr-0187 -- Kafka publish failed

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.80)
## incident-corr-0188 -- JWT verification failed

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "Redis connection lost" (328x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.74)
## incident-corr-0189 -- PostgreSQL error: deadlock detected

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Recurring PostgreSQL deadlocks under high order volume (similarity: 0.79)
## incident-corr-0190 -- PLC communication timeout

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "Kafka publish failed" (367x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "Redis connection lost" (328x)
- Closest historical incident: PLC communication timeouts on shop-floor integration (similarity: 0.77)
## incident-corr-0192 -- Unhandled exception in order processing

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Docker container exited unexpectedly" (359x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: Unhandled exceptions in order processing after a schema change (similarity: 0.76)
## incident-corr-0194 -- Kafka publish failed

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.80)
## incident-corr-0195 -- UnhandledPromiseRejection: TypeError: Cannot read properties of undefined

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Unhandled exceptions in order processing after a schema change (similarity: 0.71)
## incident-corr-0196 -- Kafka publish failed

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.80)
## incident-corr-0197 -- Kafka publish failed

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Slow response detected" (1090x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.82)
## incident-corr-0198 -- Redis connection lost

- Severity: ERROR
- Correlation confidence: 0.40
- Components: api-gateway, inventory-service, notification-service
- Hosts: wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "Unhandled exception in order processing" (391x), "Docker container exited unexpectedly" (359x), "Redis connection lost" (328x)
- Closest historical incident: Docker containers exiting unexpectedly under memory pressure (similarity: 0.77)
## incident-corr-0200 -- Docker container exited unexpectedly

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Docker container exited unexpectedly" (359x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: Docker containers exiting unexpectedly under memory pressure (similarity: 0.76)
## incident-corr-0202 -- Redis connection lost

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Redis cache outage causing cascading latency (similarity: 0.79)
## incident-corr-0203 -- JWT verification failed

- Severity: ERROR
- Correlation confidence: 0.40
- Components: inventory-service, notification-service, order-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Database connection pool above threshold" (1010x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "Redis connection lost" (328x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.75)
## incident-corr-0204 -- PLC communication timeout

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "Docker container exited unexpectedly" (359x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: PLC communication timeouts on shop-floor integration (similarity: 0.77)
## incident-corr-0205 -- Unhandled exception in order processing

- Severity: ERROR
- Correlation confidence: 0.40
- Components: api-gateway, inventory-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Unhandled exception in order processing" (391x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "JWT verification failed" (347x), "Redis connection lost" (328x)
- Closest historical incident: Unhandled exceptions in order processing after a schema change (similarity: 0.77)
## incident-corr-0206 -- MongoNetworkError: connection timed out

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: MongoDB connection timeouts during replica set election (similarity: 0.76)
## incident-corr-0207 -- Kafka publish failed

- Severity: ERROR
- Correlation confidence: 0.40
- Components: auth-service, notification-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "PLC communication timeout" (347x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.78)
## incident-corr-0209 -- MongoNetworkError: connection timed out

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: MongoDB connection timeouts during replica set election (similarity: 0.75)
## incident-corr-0210 -- PostgreSQL error: deadlock detected

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Docker container exited unexpectedly" (359x), "PLC communication timeout" (347x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: Recurring PostgreSQL deadlocks under high order volume (similarity: 0.80)
## incident-corr-0211 -- MongoNetworkError: connection timed out

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "ECONNRESET while calling payment gateway" (389x), "Kafka publish failed" (367x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: MongoDB connection timeouts during replica set election (similarity: 0.76)
## incident-corr-0212 -- PostgreSQL error: deadlock detected

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Recurring PostgreSQL deadlocks under high order volume (similarity: 0.79)
## incident-corr-0214 -- PostgreSQL error: deadlock detected

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Recurring PostgreSQL deadlocks under high order volume (similarity: 0.79)
## incident-corr-0215 -- Docker container exited unexpectedly

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: Docker containers exiting unexpectedly under memory pressure (similarity: 0.76)
## incident-corr-0216 -- UnhandledPromiseRejection: TypeError: Cannot read properties of undefined

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.74)
## incident-corr-0217 -- Redis connection lost

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "JWT verification failed" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Redis cache outage causing cascading latency (similarity: 0.77)
## incident-corr-0218 -- UnhandledPromiseRejection: TypeError: Cannot read properties of undefined

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Database connection pool above threshold" (1010x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.74)
## incident-corr-0219 -- PostgreSQL error: deadlock detected

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Recurring PostgreSQL deadlocks under high order volume (similarity: 0.78)
## incident-corr-0220 -- PLC communication timeout

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "ECONNRESET while calling payment gateway" (389x), "Kafka publish failed" (367x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "Redis connection lost" (328x)
- Closest historical incident: PLC communication timeouts on shop-floor integration (similarity: 0.77)
## incident-corr-0221 -- ECONNRESET while calling payment gateway

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "Kafka publish failed" (367x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Payment gateway ECONNRESET spikes during provider maintenance (similarity: 0.82)
## incident-corr-0223 -- Redis connection lost

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Redis cache outage causing cascading latency (similarity: 0.78)
## incident-corr-0224 -- MongoNetworkError: connection timed out

- Severity: ERROR
- Correlation confidence: 0.40
- Components: auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: MongoDB connection timeouts during replica set election (similarity: 0.76)
## incident-corr-0225 -- PLC communication timeout

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.75)
## incident-corr-0227 -- JWT verification failed

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "Redis connection lost" (328x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.76)
## incident-corr-0228 -- Docker container exited unexpectedly

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Docker containers exiting unexpectedly under memory pressure (similarity: 0.76)
## incident-corr-0229 -- PLC communication timeout

- Severity: CRITICAL
- Correlation confidence: 0.38
- Components: api-gateway, inventory-service, order-service
- Hosts: wilston-prod-01, wilston-prod-02
- Failure pattern(s): "JWT verification failed" (347x), "PLC communication timeout" (347x), "Redis connection lost" (328x)
- Closest historical incident: PLC communication timeouts on shop-floor integration (similarity: 0.77)
## incident-corr-0231 -- Unhandled exception in order processing

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.77)
## incident-corr-0232 -- Kafka publish failed

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.79)
## incident-corr-0233 -- Unhandled exception in order processing

- Severity: ERROR
- Correlation confidence: 0.40
- Components: notification-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x)
- Closest historical incident: Unhandled exceptions in order processing after a schema change (similarity: 0.76)
## incident-corr-0234 -- Redis connection lost

- Severity: ERROR
- Correlation confidence: 0.40
- Components: api-gateway, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Redis cache outage causing cascading latency (similarity: 0.79)
## incident-corr-0235 -- JWT verification failed

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Recurring PostgreSQL deadlocks under high order volume (similarity: 0.74)
## incident-corr-0237 -- JWT verification failed

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Redis cache outage causing cascading latency (similarity: 0.74)
## incident-corr-0238 -- PostgreSQL error: deadlock detected

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: auth-service, notification-service, order-service
- Hosts: wilston-prod-01, wilston-prod-03
- Failure pattern(s): "Database connection pool above threshold" (1010x), "Docker container exited unexpectedly" (359x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Recurring PostgreSQL deadlocks under high order volume (similarity: 0.79)
## incident-corr-0239 -- Kafka publish failed

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.79)
## incident-corr-0240 -- Kafka publish failed

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.80)
## incident-corr-0242 -- ECONNRESET while calling payment gateway

- Severity: ERROR
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "PLC communication timeout" (347x)
- Closest historical incident: Payment gateway ECONNRESET spikes during provider maintenance (similarity: 0.80)
## incident-corr-0243 -- JWT verification failed

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.74)
## incident-corr-0244 -- PostgreSQL error: deadlock detected

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, inventory-service, notification-service, order-service
- Hosts: wilston-prod-01, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Docker container exited unexpectedly" (359x), "PLC communication timeout" (347x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: Recurring PostgreSQL deadlocks under high order volume (similarity: 0.77)
## incident-corr-0245 -- MongoNetworkError: connection timed out

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: MongoDB connection timeouts during replica set election (similarity: 0.75)
## incident-corr-0246 -- Unhandled exception in order processing

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Unhandled exceptions in order processing after a schema change (similarity: 0.76)
## incident-corr-0247 -- Unhandled exception in order processing

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "PLC communication timeout" (347x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: Unhandled exceptions in order processing after a schema change (similarity: 0.80)
## incident-corr-0248 -- Unhandled exception in order processing

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: Recurring PostgreSQL deadlocks under high order volume (similarity: 0.75)
## incident-corr-0249 -- Redis connection lost

- Severity: ERROR
- Correlation confidence: 0.40
- Components: auth-service, inventory-service, notification-service, order-service
- Hosts: wilston-prod-01, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "Docker container exited unexpectedly" (359x), "MongoNetworkError: connection timed out" (338x), "Redis connection lost" (328x)
- Closest historical incident: Redis cache outage causing cascading latency (similarity: 0.75)
## incident-corr-0250 -- Docker container exited unexpectedly

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "Redis connection lost" (328x)
- Closest historical incident: Docker containers exiting unexpectedly under memory pressure (similarity: 0.78)
## incident-corr-0251 -- JWT verification failed

- Severity: ERROR
- Correlation confidence: 0.40
- Components: auth-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "JWT verification failed" (347x)
- Closest historical incident: Payment gateway ECONNRESET spikes during provider maintenance (similarity: 0.80)
## incident-corr-0253 -- MongoNetworkError: connection timed out

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: MongoDB connection timeouts during replica set election (similarity: 0.75)
## incident-corr-0254 -- Redis connection lost

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Redis cache outage causing cascading latency (similarity: 0.79)
## incident-corr-0255 -- Kafka publish failed

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.80)
## incident-corr-0256 -- Docker container exited unexpectedly

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Docker containers exiting unexpectedly under memory pressure (similarity: 0.77)
## incident-corr-0257 -- Unhandled exception in order processing

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Recurring PostgreSQL deadlocks under high order volume (similarity: 0.76)
## incident-corr-0258 -- PostgreSQL error: deadlock detected

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, notification-service, order-service
- Hosts: wilston-prod-01, wilston-prod-02
- Failure pattern(s): "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: Recurring PostgreSQL deadlocks under high order volume (similarity: 0.80)
## incident-corr-0259 -- Unhandled exception in order processing

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "JWT verification failed" (347x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Unhandled exceptions in order processing after a schema change (similarity: 0.77)
## incident-corr-0261 -- Redis connection lost

- Severity: ERROR
- Correlation confidence: 0.40
- Components: api-gateway, inventory-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Kafka publish failed" (367x), "Redis connection lost" (328x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.79)
## incident-corr-0262 -- Kafka publish failed

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.81)
## incident-corr-0263 -- Unhandled exception in order processing

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: auth-service, notification-service, order-service
- Hosts: wilston-prod-01, wilston-prod-03
- Failure pattern(s): "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "PLC communication timeout" (347x), "Redis connection lost" (328x)
- Closest historical incident: Unhandled exceptions in order processing after a schema change (similarity: 0.81)
## incident-corr-0265 -- Unhandled exception in order processing

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Docker container exited unexpectedly" (359x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: Unhandled exceptions in order processing after a schema change (similarity: 0.76)
## incident-corr-0266 -- Docker container exited unexpectedly

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "Redis connection lost" (328x)
- Closest historical incident: Docker containers exiting unexpectedly under memory pressure (similarity: 0.77)
## incident-corr-0267 -- UnhandledPromiseRejection: TypeError: Cannot read properties of undefined

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.72)
## incident-corr-0268 -- UnhandledPromiseRejection: TypeError: Cannot read properties of undefined

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.72)
## incident-corr-0269 -- Unhandled exception in order processing

- Severity: CRITICAL
- Correlation confidence: 0.36
- Components: auth-service, order-service
- Hosts: wilston-prod-01, wilston-prod-03
- Failure pattern(s): "Slow response detected" (1090x), "External API latency increased" (1076x), "Unhandled exception in order processing" (391x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x)
- Closest historical incident: Unhandled exceptions in order processing after a schema change (similarity: 0.74)
## incident-corr-0270 -- Docker container exited unexpectedly

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "ECONNRESET while calling payment gateway" (389x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Docker containers exiting unexpectedly under memory pressure (similarity: 0.77)
## incident-corr-0271 -- Unhandled exception in order processing

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "Retrying downstream request" (1067x), "Unhandled exception in order processing" (391x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Docker container exited unexpectedly" (359x)
- Closest historical incident: Unhandled exceptions in order processing after a schema change (similarity: 0.76)
## incident-corr-0272 -- Kafka publish failed

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.79)
## incident-corr-0273 -- Kafka publish failed

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "PLC communication timeout" (347x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.80)
## incident-corr-0274 -- JWT verification failed

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Recurring PostgreSQL deadlocks under high order volume (similarity: 0.74)
## incident-corr-0275 -- UnhandledPromiseRejection: TypeError: Cannot read properties of undefined

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: inventory-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02
- Failure pattern(s): "Slow response detected" (1090x), "Unhandled exception in order processing" (391x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "PLC communication timeout" (347x)
- Closest historical incident: Unhandled exceptions in order processing after a schema change (similarity: 0.73)
## incident-corr-0276 -- JWT verification failed

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.75)
## incident-corr-0277 -- PostgreSQL error: deadlock detected

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Recurring PostgreSQL deadlocks under high order volume (similarity: 0.79)
## incident-corr-0278 -- PLC communication timeout

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: PLC communication timeouts on shop-floor integration (similarity: 0.77)
## incident-corr-0279 -- JWT verification failed

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.75)
## incident-corr-0280 -- Unhandled exception in order processing

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Unhandled exceptions in order processing after a schema change (similarity: 0.76)
## incident-corr-0281 -- Redis connection lost

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Redis cache outage causing cascading latency (similarity: 0.77)
## incident-corr-0282 -- ECONNRESET while calling payment gateway

- Severity: ERROR
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "ECONNRESET while calling payment gateway" (389x), "MongoNetworkError: connection timed out" (338x)
- Closest historical incident: Payment gateway ECONNRESET spikes during provider maintenance (similarity: 0.84)
## incident-corr-0283 -- Kafka publish failed

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.80)
## incident-corr-0284 -- UnhandledPromiseRejection: TypeError: Cannot read properties of undefined

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02
- Failure pattern(s): "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "JWT verification failed" (347x)
- Closest historical incident: Payment gateway ECONNRESET spikes during provider maintenance (similarity: 0.71)
## incident-corr-0285 -- MongoNetworkError: connection timed out

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: MongoDB connection timeouts during replica set election (similarity: 0.75)
## incident-corr-0286 -- Redis connection lost

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Redis cache outage causing cascading latency (similarity: 0.78)
## incident-corr-0287 -- ECONNRESET while calling payment gateway

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: Payment gateway ECONNRESET spikes during provider maintenance (similarity: 0.81)
## incident-corr-0289 -- Redis connection lost

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Docker container exited unexpectedly" (359x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "Redis connection lost" (328x)
- Closest historical incident: Redis cache outage causing cascading latency (similarity: 0.76)
## incident-corr-0291 -- UnhandledPromiseRejection: TypeError: Cannot read properties of undefined

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Docker container exited unexpectedly" (359x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "Redis connection lost" (328x)
- Closest historical incident: Unhandled exceptions in order processing after a schema change (similarity: 0.71)
## incident-corr-0292 -- PLC communication timeout

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Slow response detected" (1090x), "External API latency increased" (1076x), "Kafka publish failed" (367x), "JWT verification failed" (347x), "PLC communication timeout" (347x)
- Closest historical incident: Kafka publish failures during broker rebalance (similarity: 0.78)
## incident-corr-0293 -- ECONNRESET while calling payment gateway

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "ECONNRESET while calling payment gateway" (389x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Payment gateway ECONNRESET spikes during provider maintenance (similarity: 0.81)
## incident-corr-0295 -- PostgreSQL error: deadlock detected

- Severity: CRITICAL
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x), "Redis connection lost" (328x)
- Closest historical incident: Recurring PostgreSQL deadlocks under high order volume (similarity: 0.79)
## incident-corr-0296 -- Unhandled exception in order processing

- Severity: ERROR
- Correlation confidence: 0.40
- Components: api-gateway, auth-service, inventory-service, notification-service, order-service, payment-service
- Hosts: wilston-prod-01, wilston-prod-02, wilston-prod-03
- Failure pattern(s): "Memory usage high" (1119x), "Slow response detected" (1090x), "External API latency increased" (1076x), "Retrying downstream request" (1067x), "Database connection pool above threshold" (1010x), "Unhandled exception in order processing" (391x), "ECONNRESET while calling payment gateway" (389x), "UnhandledPromiseRejection: TypeError: Cannot read properties of undefined" (370x), "Kafka publish failed" (367x), "Docker container exited unexpectedly" (359x), "JWT verification failed" (347x), "PLC communication timeout" (347x), "MongoNetworkError: connection timed out" (338x), "PostgreSQL error: deadlock detected" (337x)
- Closest historical incident: Unhandled exceptions in order processing after a schema change (similarity: 0.76)
