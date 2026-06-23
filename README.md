# AWS RAG Application with Amazon Bedrock

A Retrieval-Augmented Generation (RAG) application built using Amazon Bedrock that enables users to upload PDF documents and interact with them through natural language queries. The system retrieves relevant document chunks and generates context-aware responses using foundation models, providing accurate and grounded answers based on the uploaded content.

## Overview

This project leverages Amazon Bedrock Knowledge Bases to implement a fully managed RAG workflow, including:

* Document ingestion
* Text chunking
* Vector embedding generation
* Semantic retrieval
* Response generation using foundation models

The application provides an intuitive web interface for uploading documents and querying their contents without requiring manual data processing or indexing workflows.

## Features

* PDF document upload and processing
* Automated document ingestion and indexing
* Semantic search powered by vector embeddings
* Context-aware question answering
* Source attribution and citations
* Interactive Streamlit user interface
* Serverless AWS architecture
* Scalable and managed RAG pipeline

## Tech Stack

| Component      | Technology                     |
| -------------- | ------------------------------ |
| Frontend       | Streamlit                      |
| Backend        | Python                         |
| LLM Platform   | Amazon Bedrock                 |
| Knowledge Base | Amazon Bedrock Knowledge Bases |
| Storage        | Amazon S3                      |
| Compute        | AWS Lambda                     |
| Vector Store   | Amazon S3 Vectors              |

## Prerequisites

Before running the project, ensure you have:

* An AWS Account
* Access to Amazon Bedrock models
* Python 3.10 or higher
* AWS CLI configured with appropriate permissions
* IAM permissions for Bedrock, S3, and Lambda services

## Usage

1. Upload one or more PDF documents.
2. Wait for the ingestion and indexing process to complete.
3. Enter your question in natural language.
4. Review the generated response along with supporting citations.

### Example Queries

* Summarize this document.
* What are the key findings?
* List all recommendations from the report.
* What risks are identified in the document?
* Compare the conclusions across uploaded documents.

## AWS Services Used

* Amazon Bedrock
* Amazon Bedrock Knowledge Bases
* Amazon S3
* AWS Lambda
* Amazon S3 Vectors
* AWS IAM
* Amazon CloudWatch

## Security

This solution follows AWS security best practices:

* IAM-based access control
* Least-privilege permissions
* Encrypted document storage in Amazon S3
* Secure access to Bedrock resources
* CloudWatch logging and monitoring

## Future Enhancements

* Multi-document comparison
* Chat history persistence
* Support for DOCX and TXT files
* User authentication and authorization
* Hybrid search (keyword + semantic)
* Streaming response generation

## License

This project is licensed under the MIT License.
