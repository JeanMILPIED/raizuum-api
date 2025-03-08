import os

folders = [
    "app",
    "app/routes",
    "app/services",
    "app/models",
    "app/utils"
]

files = [
    "app/main.py",
    "app/routes/ocr.py",
    "app/routes/auth.py",
    "app/services/ocr_service.py",
    "app/services/auth_service.py",
    "app/models/user_model.py",
    "app/utils/security.py",
    ".env",
    "requirements.txt",
    "Dockerfile",
    "docker-compose.yml",
    "README.md"
]

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Create empty files
for file in files:
    with open(file, "w") as f:
        pass

print("✅ Project structure created successfully!")
