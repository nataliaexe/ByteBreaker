# ByteBreaker API Documentation

## REST API Endpoints

### Base URL
`http://localhost:8000`

### Endpoints

#### GET /
Returns API information

**Response:**
```json
{
  "name": "ByteBreaker API",
  "version": "1.0.0",
  "status": "running"
}
GET /status

Get framework status

Response:
json

{
  "modules_loaded": ["recon", "scanner", "exploit", "cracker", "forensics"],
  "results_count": 0,
  "authorizations": 0,
  "config_valid": true
}

POST /authorize

Authorize target for testing

Request:
json

{
  "target": "example.com",
  "scope": ["recon", "scan"],
  "authorized_by": "John Doe",
  "days": 30
}

Response:
json

{
  "status": "success",
  "message": "Authorized example.com"
}

POST /recon

Run reconnaissance

Request:
json

{
  "target": "example.com",
  "options": {
    "port_scan": true,
    "ssl_check": true
  }
}

POST /scan

Run vulnerability scan

Request:
json

{
  "target": "example.com",
  "scan_type": "full"
}

POST /crack

Crack password hash

Request:
json

{
  "hash": "5f4dcc3b5aa765d61d8327deb882cf99",
  "hash_type": "md5"
}

POST /forensics

Run forensic analysis

Request:
json

{
  "file_path": "/path/to/file",
  "analysis_type": "full"
}

Authentication

Currently, the API does not implement authentication. For production use, implement proper authentication mechanisms.
Error Handling

All endpoints return appropriate HTTP status codes:

    200: Success

    400: Bad request

    403: Permission denied

    404: Not found

    500: Internal server error

Rate Limiting

Rate limiting should be implemented for production use to prevent abuse.
WebSocket Support

Real-time updates via WebSocket are planned for future versions.
