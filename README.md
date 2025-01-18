# 25-1-KeYThon-2-be

## Installation and Setup
1. **클론**:
   ```bash
   git clone https://github.com/sounmu/25-1-KeYThon-2-be
   ```
2. **가상 환경 설정**:
   ```bash
   cd src
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # macOS/Linux
   ```
3. **의존성 설치**:
   ```bash
   pip install -r requirements.txt
   ```
4. **서버 실행**:
   ```bash
   uvicorn main:app --reload
   ```
