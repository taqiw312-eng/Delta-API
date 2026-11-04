from fastapi import FastAPI, HTTPException
import requests
from bs4 import BeautifulSoup

app = FastAPI()

@app.get("/")
def home():
    return {"status": "online", "message": "Delta API is running!"}

@app.get("/get-key")
def get_delta_key(url: str):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="فشل الاتصال بالرابط")
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        key_element = soup.find("code") or soup.find("input", {"id": "key"})
        extracted_key = key_element.get_text(strip=True) if key_element else "EXAMPLE_DELTA_KEY_123"

        return {
            "status": "success",
            "url": url,
            "key": extracted_key
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
      
