# 🚀 Logistics Management API

This is a Django REST Framework (DRF) API for managing vendors, trucks, drivers, missions, and cargo in a logistics system.

---

## **📌 1. Setup Instructions**

### **1️⃣ Clone the Repository**

```bash
git clone https://github.com/Y4Clab/WFP-TRACKER-SYSTEM.git
cd logitrack
```

### **2️⃣ Create and Activate a Virtual Environment**

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### **3️⃣ Install Dependencies**

```bash
pip install -r requirements.txt
```

### **4️⃣ Configure PostgreSQL Database**

Ensure PostgreSQL is installed and running. Then, create a new database called logitrack:

### **5️⃣ Update `settings.py`**

Modify your database settings in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'logitrack',
        'USER': 'logistics_user', #change to your user name
        'PASSWORD': 'securepassword', #change to your password
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## **📌 2. Running the Server**

### **1️⃣ Apply Migrations**

```bash
python manage.py migrate
```

### **2️⃣ Create a Superuser**

```bash
python manage.py createsuperuser
```

Enter the required details (username, email, password).

### **3️⃣ Start the Server**

```bash
python manage.py runserver
```

The API will be available at:  
🔗 **http://127.0.0.1:8000/**

---

## **📌 3. Populate the Database Using psql**

### **1️⃣ populate the database**

```bash
psql -U <replace-with-your-database-user> -d logitrack < logitrack_db.sql
```

---

## **📌 6. Useful Commands**

| Command                            | Description                  |
| ---------------------------------- | ---------------------------- |
| `python manage.py migrate`         | Apply database migrations    |
| `python manage.py createsuperuser` | Create an admin user         |
| `python manage.py runserver`       | Start the development server |

---

## **📌 7. Notes**

- Ensure **PostgreSQL** is installed and running before starting the server.
- Default **admin panel** is available at **`http://127.0.0.1:8000/admin/`**.

---
