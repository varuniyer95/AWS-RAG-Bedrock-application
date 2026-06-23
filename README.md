# AWS-RAG-Bedrock-application

Overview
A Retrieval-Augmented Generation (RAG) application built using Amazon Bedrock that allows users to upload PDF documents and ask questions about their content. The system retrieves relevant document chunks and generates context-aware responses using foundation models. Amazon Bedrock Knowledge Bases provides a managed RAG workflow including ingestion, chunking, embeddings, retrieval, and response generation.

Features
PDF document upload
Automated document ingestion and indexing
Semantic search using vector embeddings
Context-aware Q&A
Source citations
Streamlit web interface
AWS serverless architecture
Tech Stack
Amazon Bedrock
Bedrock Knowledge Base
Amazon S3
AWS Lambda
Streamlit
Python
Prerequisites
AWS Account
Bedrock Model Access Enabled
Python 3.10+
AWS CLI Configured
Usage
Upload one or more PDF documents.
Wait for indexing to complete.
Ask questions in natural language.
Receive answers grounded in document content.
Example:

Summarize this document.
What are the key findings?
List all recommendations from the report.
AWS Resources
Amazon S3 Bucket
Amazon Bedrock Knowledge Base
Vector Store (S3 Vectors)
AWS Lambda
Security
IAM-based access control
Encrypted S3 storage
CloudWatch monitoring
Least-privilege permissions
