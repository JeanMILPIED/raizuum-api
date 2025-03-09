# raizuum-api is open source api to extract info from CV in the data world

# API Documentation

This FastAPI application provides endpoints to extract text and features from CV files in pdf using Optical Character Recognition (OCR) and other text processing techniques. It also supports authentication using OAuth2.

## Authentication

To interact with the API endpoints, you'll need to authenticate using a valid OAuth2 token. The token must be included in the **Authorization** header of the request.

### OAuth2 Token

The token is provided by the `/login/` endpoint. You can obtain the token by logging in using valid credentials.

### Request Header Example:

Authorization: Bearer YOUR_TOKEN_HERE

### Endpoints
### POST /extract-from-pdf/  
Description:  
This endpoint allows you to upload a PDF file. The file is processed to extract text and relevant features (keywords) from the PDF.  

Request Body:  
file (required): The PDF file you want to upload.  

Request Example:  
```
curl -X 'POST' \
  'http://127.0.0.1:8000/extract-from-pdf/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer YOUR_TOKEN_HERE' \
  -F 'file=@path_to_your_pdf.pdf'
```

Response:  
- extracted_text: The text extracted from the PDF.  
- features: Features extracted from the text using Computer Vision (CV).  

Response Example:  
```
{
    "extracted_text": "This is the extracted text from the PDF.",
    "features": {
        "keywords": ["keyword1", "keyword2"],
        "other_feature": "value"
    }
}
```

Error Responses:  
- 400 Bad Request: If the file is not a PDF or if no text is found in the PDF.  
- 500 Internal Server Error: If there's an error processing the file.  

### POST /extract-features/
Description:  
This endpoint allows you to extract features from a given text. You can provide the text directly in the request body.  

Request Body:  
- text (required): The text you want to process.  
- keywords_dict (optional): A dictionary of keywords to assist in feature extraction.  

Request Example:
```
curl -X 'POST' \
  'http://127.0.0.1:8000/extract-features/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer YOUR_TOKEN_HERE' \
  -H 'Content-Type: application/json' \
  -d '{"text": "Text to extract features from.", "keywords_dict": {"keyword1": "value1"}}'
```

Response:  
- extracted_text: The text after processing.  
- features: Extracted features (e.g., keywords).  

Response Example:  
```
{
    "extracted_text": "Text to extract features from.",
    "features": {
        "keywords": ["keyword1", "value1"]
    }
}
```

### Error Handling
The API responds with appropriate HTTP status codes:  

- 200 OK: Successfully processed the request.  
- 400 Bad Request: Invalid input or missing file.  
- 401 Unauthorized: Missing or invalid OAuth2 token.  
- 500 Internal Server Error: Issues with processing or other internal errors.  

### Running the API  

Clone the repository.  

Install Docker  

Run Docker commands  
```
docker build -t raizuum-api .  
docker run -p 8000:8000 raizuum-api
```

Access the Swagger UI documentation at http://127.0.0.1:8000/docs.  

### Notes
Ensure that you have set up the authentication and have a valid token for accessing the API.  
You can refer to the Swagger UI for more detailed interaction with the API, including testing endpoints directly from the browser.  

### How to Use This Documentation
1. **Add it to `README.md`**: Copy and paste the above Markdown into your `README.md` file.
2. **Make any necessary adjustments**: Feel free to update paths, examples, or add further details specific to your implementation.
3. **Swagger UI**: FastAPI automatically provides an interactive Swagger UI at `/docs`. You can use it to test the endpoints directly in your browser.

---

Let me know if you need any further adjustments! 🚀
