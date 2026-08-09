Assignment Overview
Modern software systems generate logs from multiple components such as applications, containers, databases, PLCs, and infrastructure services. Diagnosing production failures often requires engineers to analyze thousands of log entries, identify patterns, correlate failures across systems, and leverage historical knowledge to determine the most likely root cause.
Your task is to build an AI-Powered Log Analysis Assistant capable of analyzing production logs, retrieving relevant historical incidents, answering user questions about the logs, and generating a structured incident investigation report.
Input Dataset
The attached ZIP archive (wilston_logs.zip) contains three production log files from the Wilston Manufacturing Platform.
wilston_application.log
wilston_docker.log
wilston_plc.log
Each file contains approximately 10,000 log entries, resulting in nearly 30,000 production log records across multiple system components.
The logs include a realistic mixture of:
Normal operational events
Warnings
Application exceptions
Communication failures
Database-related errors
Infrastructure failures
Performance degradation
Repeated error patterns
Your application should process all three log files together and correlate events across multiple sources before generating its analysis.
Problem Statement
Develop an AI-powered application capable of analyzing the provided logs and generating a structured incident investigation report.
Your solution should demonstrate your ability to:
Process large log datasets
Detect important failures
Correlate related events across multiple log sources
Retrieve relevant historical incidents
Use an LLM to generate meaningful analysis
Answer user questions about the incident
Present findings in a clear and structured format
Core Requirements
1. Multi-Source Log Processing
Your application should:
Read log files from the provided ZIP archive.
Parse and normalize logs from all sources.
Preserve the source of each log entry.
Group similar errors together.
Correlate related events across multiple log files.
2. AI-Based Incident Analysis
Using a local LLM (via Ollama), generate:
Executive Summary
Incident Summary
Possible Root Cause(s)
Supporting Evidence
Recommended Corrective Actions
The generated analysis should clearly explain how the conclusions were reached.
3. Retrieval-Augmented Generation (RAG)
Implement a basic Retrieval-Augmented Generation (RAG) pipeline.
You may either:
Create a small historical incident dataset (recommended: 10–20 incidents), or
Use any suitable format (JSON, Markdown, CSV, SQLite, etc.) containing previous incidents, root causes, and resolution steps.
The purpose is to demonstrate how retrieved historical knowledge improves the quality of LLM responses.
Your application should clearly distinguish between:
Evidence extracted from the current logs
Information retrieved from historical incidents
LLM-generated reasoning and recommendations
4. Interactive Log Query Assistant (LLM + RAG)
In addition to report generation, implement an interface that allows users to ask natural language questions about the provided logs.
Example questions include:
What are the most critical errors?
Which service generated the highest number of failures?
Which components experienced repeated failures?
What is the likely root cause of the incident?
Which historical incidents are most similar?
What corrective actions do you recommend?
Show all PostgreSQL-related errors.
How many PLC communication timeout errors occurred?
Which services were affected after the first PLC timeout?
Summarize the overall health of the system.
You are free to implement the interface as:
Command Line Interface (CLI)
Streamlit
Gradio
Simple Web UI
REST API
5. Report Generation
Generate an HTML or Markdown report containing:
Executive Summary
Incident Summary
Major Issues Detected
Timeline of Important Events (optional)
Root Cause Analysis
Supporting Evidence
Similar Historical Incidents
Recommended Fixes
Confidence Level
Technical Requirements
Python 3.10+
Local LLM using Ollama
Vector database for RAG (FAISS, ChromaDB, or similar)
Modular and maintainable project structure
Your project should ideally contain separate modules for:
Log ingestion
Log preprocessing
Embedding generation
Retrieval pipeline
Prompt management
LLM interaction
Response parsing
Report generation
You are free to choose the frameworks and libraries that best fit your implementation.