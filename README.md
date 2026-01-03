# Secure Cloud Exchange System

A full-stack cloud file management system designed to handle secure document and media exchange between client devices and a centralized cloud server. The application implements version control, role-based access control, and audit logging to ensure data integrity and security.

## Project Overview

This system allows users to upload, download, and manage files securely over HTTPS. It features a custom file storage backend that supports file versioning (tracking changes by date, size, and version number) and allows for the retrieval of specific file iterations.

The architecture separates the frontend (React) from the backend (FastAPI), utilizing asynchronous processing for efficient I/O operations during file transfers.

## Key Features

- Secure Authentication: Implements JWT-based authentication with login and logout capabilities.

- Role-Based Access Control (RBAC): Granular permissions for file operations (Read, Write, Update) based on user roles.

- File Versioning: Automatically handles version control. When a file with an existing name is uploaded, the system archives the previous version and increments the version number.

- Streamed File Transfer: Supports uploading and downloading of large files using asynchronous streams to minimize memory usage.

- Data Integrity: files are verified using SHA-256 checksums upon upload.

- Audit Logging ("LogBook"): A comprehensive logging system that records all user login events and file operations (uploads, downloads, modifications) in a persistent database.

- Batch Operations: Capability to bundle multiple files for simplified transfer.

## Technical Stack
### Backend
- Language: Python 3.10+

- Framework: FastAPI (Asynchronous Web Framework)

- Database: SQLAlchemy (Async ORM) with SQLite (Dev) / PostgreSQL (Prod)

- Storage: Local filesystem with path traversal protection and SHA-256 hashing

- Key Libraries:

    - aiofiles for non-blocking file I/O

    - pydantic for data validation

    - alembic for database migrations

### Frontend

- Framework: React.js

- State Management: Context API

- Styling: CSS Modules / Custom CSS

## Architecture Details

Storage Strategy Files are stored using a deterministic directory structure to ensure isolation between users and versions: user/{userID}/file/{fileId}/v{version_number}/{safe_logical_name}

### Security

- Path Safety: The system sanitizes filenames and validates paths to prevent directory traversal attacks.

- Token Management: Access is managed via secure HTTP-only cookies or Bearer tokens (depending on specific configuration).

## Setup and Installation

1. Clone the repository
```Bash
git clone https://github.com/yourusername/secure-cloud-exchange.git
cd secure-cloud-exchange
```
2. Backend Setup
```Bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
3. Database Initialization The project uses Alembic for migrations.
```Bash
alembic upgrade head
```
4. Frontend Setup
```Bash
cd frontend
npm install
npm start
```
## Future Improvements

- Migration from local storage to S3/Azure Blob Storage buckets.

- Implementation of compression algorithms for batch downloads.

- Enhanced preview generation for media files.