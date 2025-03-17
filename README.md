# !nkster Backend

This repository contains the backend for the !nkster mobile application, built with Flask, SQLAlchemy, and PostgreSQL.

---

## **Setup Instructions**

### **1. Clone the Repository**
```bash
git clone https://github.com/drizzle021/inkster-backend.git
cd inkster-backend
```

### **2. Create V-Environment**
#### Windows
```bash
python -m venv venv
.\venv\Scripts\activate
```
#### Linux/Mac
```bash
python3 -m venv venv
source venv/bin/activate
```
### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```
### **4. Set Up Environment Variables**

Create a `.env` file in the root directory of the project and add the following variables:

```plaintext
HOST=127.0.0.1
PORT=5000
DATABASE_URI=postgresql+psycopg2://<username>:<password>@<host>:<port>/<database_name>
```


## **Start**
Run the application using the following command:
```bash
python run.py
```







