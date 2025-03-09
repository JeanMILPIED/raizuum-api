from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from app.services.ocr_service import extract_text_from_pdf, get_features_text_cv, process_pdf
import io

from app.models.ocr_request import OCRRequest #FIXME: should we use ?

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")

def authenticate_request(token: str = Depends(oauth2_scheme)):
    from app.utils.security import decode_access_token
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload

@router.post("/extract-from-pdf/")
async def extract_from_pdf(file: UploadFile = File(...), token: str = Depends(authenticate_request)):
    try:
        if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")

        extracted_text = await process_pdf(file)
        if not extracted_text:
            raise HTTPException(status_code=400, detail="No text found in the PDF")

        keywords_dict = {}
        extracted_text, features = get_features_text_cv(extracted_text, keywords_dict)
        return {"extracted_text": extracted_text, "features": features}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@router.post("/extract-features/")
def extract_features(request: OCRRequest):
    extracted_text, features = get_features_text_cv(request.text, request.keywords_dict)
    return {"extracted_text": extracted_text, "features": features}
