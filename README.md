# Webzaar Backend Setup

### Step-1: Clone the Directory:
```git clone https://github.com/vilalali/webzaar-backend.git```

```cd webzaar-backend/```

### Before running the below command ensure that you are in "webzaar-backend" dir.
### Step-2: Setup the python virtualenv:
* Note: If virtual environment is not installed in your system, Then first you have to install the virtualenv.
  
```sudo apt install python3-virtualenv```
#### Now create the virtual environment, run the below command:
```python3 -m venv venvDwebzaar```
```python -m venv venvDwebzaar```
#### Activate the virtual Environment running the below command:
```source venvDwebzaar/bin/activate```

### Step-3: Install the required package by running the below command:
```pip install -r req.txt```
#### For testing in localhost run the below command:
```python run.py```


### Step-4: Now test the api open your browser and paste the url:
```http://localhost:5000//collectionTableData```

#### Output will be:
```
[
  {
    "formatted_date": "20:08:2023 04:08:18",
    "id": 3,
    "lastmodified": "Sun, 20 Aug 2023 04:08:18 GMT",
    "name": "Collection 3"
  },
  {
    "formatted_date": "20:08:2023 04:08:18",
    "id": 2,
    "lastmodified": "Sun, 20 Aug 2023 04:08:18 GMT",
    "name": "Collection 2"
  },
  {
    "formatted_date": "20:08:2023 04:08:18",
    "id": 1,
    "lastmodified": "Sun, 20 Aug 2023 04:08:18 GMT",
    "name": "Collection 1"
  }
]

```

### Step-5: Before running the step-4 you have to setup the db:
```
mysql -u root -p
CREATE DATABASE tribedb;
use tribedb;
```
```
CREATE TABLE collection (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    lastmodified DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE content (
    id INT AUTO_INCREMENT PRIMARY KEY,
    srctxt TEXT NOT NULL,
    tgttxt TEXT,
    domainname VARCHAR(255) NOT NULL,
    psrcmd5 VARCHAR(255),
    multipart INT,
    part INT,
    lastmodified DATETIME DEFAULT CURRENT_TIMESTAMP
);
```
#### Run the below query for inserting temp data:
```
INSERT INTO collection (name) VALUES ('Collection 1');
INSERT INTO collection (name) VALUES ('Collection 2');
INSERT INTO collection (name) VALUES ('Collection 3');
```
```
INSERT INTO content (srctxt, tgttxt, domainname, psrcmd5, multipart, part) VALUES ('Source Text 1', 'Target Text 1', 'Domain 1', 'psrcmd5_1', 0, 1);
INSERT INTO content (srctxt, tgttxt, domainname, psrcmd5, multipart, part) VALUES ('Source Text 2', 'Target Text 2', 'Domain 2', 'psrcmd5_2', 1, 2);
INSERT INTO content (srctxt, tgttxt, domainname, psrcmd5, multipart, part) VALUES ('Source Text 3', 'Target Text 3', 'Domain 3', 'psrcmd5_3', 0, 1);
```



---

Document written and maintain by [Vilal Ali](https://vilal-ali.github.io/my-profile/index.html)

