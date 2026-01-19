# PDF Extraction API Documentation

## Overview
The PDF extraction API allows users to upload PDF files and extract their text content for further processing (summarization, translation, quiz generation, etc.).

## Endpoints

### 1. Extract PDF Text
**Endpoint:** `POST /api/v1/articles/extract-pdf`

**Authentication:** Required (Bearer Token)

**Description:** Upload a PDF file and extract its text content.

#### Request
- **Method:** POST
- **Content-Type:** multipart/form-data
- **Headers:**
  ```
  Authorization: Bearer <your_access_token>
  ```
- **Body:**
  - `file`: PDF file (required)

#### Example using cURL
```bash
curl -X POST "http://localhost:8000/api/v1/articles/extract-pdf" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "file=@/path/to/your/document.pdf"
```

#### Example using Python (requests)
```python
import requests

url = "http://localhost:8000/api/v1/articles/extract-pdf"
headers = {
    "Authorization": "Bearer YOUR_ACCESS_TOKEN"
}
files = {
    "file": open("document.pdf", "rb")
}

response = requests.post(url, headers=headers, files=files)
print(response.json())
```

#### Success Response (200 OK)
```json
{
  "status": "success",
  "message": "PDF extracted successfully",
  "article_id": 123,
  "data": {
    "full_text": "Complete extracted text from all pages...",
    "pages": [
      "Text from page 1...",
      "Text from page 2...",
      "Text from page 3..."
    ],
    "page_count": 3,
    "file_name": "document.pdf"
  }
}
```

#### Error Responses

**400 Bad Request** - Invalid file type
```json
{
  "detail": "Only PDF files are allowed"
}
```

**401 Unauthorized** - Missing or invalid token
```json
{
  "detail": "Invalid authentication credentials"
}
```

**500 Internal Server Error** - Processing error
```json
{
  "detail": "Error processing PDF: [error message]"
}
```

---

### 2. Extract Wikipedia Content
**Endpoint:** `POST /api/v1/articles/extract-wiki`

**Authentication:** Required (Bearer Token)

**Description:** Extract content from a Wikipedia article URL.

#### Request
- **Method:** POST
- **Content-Type:** application/json
- **Headers:**
  ```
  Authorization: Bearer <your_access_token>
  ```
- **Body:**
  ```json
  {
    "url": "https://en.wikipedia.org/wiki/Artificial_intelligence"
  }
  ```

#### Success Response (200 OK)
```json
{
  "status": "success",
  "message": "Wikipedia content extracted successfully",
  "article_id": 124,
  "data": {
    "title": "Artificial intelligence",
    "content": "Full article content...",
    "summary": "Brief summary...",
    "url": "https://en.wikipedia.org/wiki/Artificial_intelligence",
    "language": "en"
  }
}
```

---

### 3. Get All Articles
**Endpoint:** `GET /api/v1/articles/`

**Authentication:** Required (Bearer Token)

**Description:** Retrieve all articles for the current authenticated user.

#### Success Response (200 OK)
```json
{
  "articles": [
    {
      "id": 123,
      "user_id": 1,
      "url": "pdf://document.pdf",
      "title": "document.pdf",
      "action": "summary",
      "created_at": "2026-01-19T10:30:00"
    },
    {
      "id": 124,
      "user_id": 1,
      "url": "https://en.wikipedia.org/wiki/Artificial_intelligence",
      "title": "Artificial intelligence",
      "action": "summary",
      "created_at": "2026-01-19T11:00:00"
    }
  ]
}
```

---

### 4. Get Article by ID
**Endpoint:** `GET /api/v1/articles/{article_id}`

**Authentication:** Required (Bearer Token)

**Description:** Retrieve a specific article by its ID.

#### Success Response (200 OK)
```json
{
  "article": {
    "id": 123,
    "user_id": 1,
    "url": "pdf://document.pdf",
    "title": "document.pdf",
    "action": "summary",
    "created_at": "2026-01-19T10:30:00"
  }
}
```

---

## Implementation Details

### File Processing Flow
1. User uploads PDF file via multipart/form-data
2. Server validates file type (must be .pdf)
3. File is saved to temporary location
4. PyPDFLoader from langchain-community extracts text from all pages
5. Extracted content is returned with metadata
6. Temporary file is cleaned up automatically
7. Article record is saved to database for tracking

### Database Schema
```python
Article:
  - id: Integer (Primary Key)
  - user_id: Integer (Foreign Key to users)
  - url: String (PDF path or Wikipedia URL)
  - title: String (Filename or article title)
  - action: Enum (summary, translation, quiz)
  - created_at: DateTime
```

### Dependencies
- **langchain-community**: PDF loading and processing
- **pypdf**: PDF parsing library
- **python-multipart**: File upload handling
- **tempfile**: Temporary file management

### Security Considerations
- Authentication required for all endpoints
- File type validation (only PDF allowed)
- Temporary files are automatically cleaned up
- User can only access their own articles

---

## Testing the API

### 1. Get Authentication Token
First, login to get an access token:
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "yourpassword"
  }'
```

### 2. Upload PDF
Use the token from step 1:
```bash
curl -X POST "http://localhost:8000/api/v1/articles/extract-pdf" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "file=@test.pdf"
```

### 3. View Uploaded Articles
```bash
curl -X GET "http://localhost:8000/api/v1/articles/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## Frontend Integration Example

### React (using fetch)
```javascript
const uploadPDF = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch('http://localhost:8000/api/v1/articles/extract-pdf', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    },
    body: formData
  });
  
  const data = await response.json();
  return data;
};
```

### Streamlit
```python
import streamlit as st
import requests

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    files = {"file": uploaded_file}
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    
    response = requests.post(
        "http://localhost:8000/api/v1/articles/extract-pdf",
        headers=headers,
        files=files
    )
    
    if response.status_code == 200:
        data = response.json()
        st.success(data["message"])
        st.write(data["data"]["full_text"])
```

---

## Next Steps

After extracting PDF content, you can:
1. **Generate Summary**: Use LLM services to create summaries
2. **Translate Content**: Translate to different languages
3. **Generate Quiz**: Create quiz questions from the content
4. **Export**: Export to various formats (PDF, DOCX, etc.)

See the LLM Service documentation for content processing options.
