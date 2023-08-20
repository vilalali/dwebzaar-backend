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
* Create the 'collection' table
```
CREATE TABLE collection (
  id INT NOT NULL AUTO_INCREMENT,
  origtxt TEXT,
  srctxt TEXT,
  srcmd5 VARCHAR(100) GENERATED ALWAYS AS (MD5(LOWER(LTRIM(RTRIM(srctxt))))) VIRTUAL,
  psrcmd5 VARCHAR(250) DEFAULT NULL COMMENT 'gsrcmd5',
  multipart VARCHAR(10) NOT NULL DEFAULT 'no',
  part INT NOT NULL DEFAULT 0,
  domainname VARCHAR(100) NOT NULL DEFAULT 'foscos',
  alternates TEXT,
  lastmodified TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY srcmd5 (srcmd5)
) ENGINE=InnoDB AUTO_INCREMENT=4178 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

* Create the 'content' table
```
CREATE TABLE content (
  id INT NOT NULL AUTO_INCREMENT,
  srctxt TEXT,
  srcmd5 VARCHAR(100) GENERATED ALWAYS AS (MD5(LOWER(LTRIM(RTRIM(srctxt))))) VIRTUAL,
  tgttxt TEXT,
  psrcmd5 VARCHAR(250) DEFAULT NULL COMMENT 'gsrcmd5',
  multipart VARCHAR(1) DEFAULT 'n',
  part INT NOT NULL DEFAULT 0,
  domainname VARCHAR(100) NOT NULL DEFAULT 'foscos',
  alternates TEXT,
  lastmodified TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY srcmd5 (srcmd5)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```
* Create the 'translation' table
```
CREATE TABLE translation (
  id INT NOT NULL AUTO_INCREMENT,
  srctxt TEXT,
  srcmd5 VARCHAR(100) GENERATED ALWAYS AS (MD5(LOWER(LTRIM(RTRIM(srctxt))))) VIRTUAL,
  tgttxt TEXT,
  psrcmd5 VARCHAR(250) DEFAULT NULL,
  multipart VARCHAR(1) DEFAULT 'n',
  part INT NOT NULL DEFAULT 0,
  domainname VARCHAR(100) NOT NULL DEFAULT 'foscos',
  alternates TEXT,
  lastmodified TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY srcmd5 (srcmd5)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```
#### Run the below query for inserting temp data:
``` Insert Query for "collection" Table: For testing```
```
INSERT INTO collection (origtxt, srctxt, multipart, part, domainname, alternates)
VALUES ('Original Text 1', 'Source Text 1', 'no', 1, 'domain1', 'Alternates 1'),
       ('Original Text 2', 'Source Text 2', 'yes', 2, 'domain2', 'Alternates 2'),
       ('Original Text 3', 'Source Text 3', 'no', 3, 'domain1', 'Alternates 3'),
       ('Original Text 4', 'Source Text 4', 'yes', 4, 'domain2', 'Alternates 4'),
       ('Original Text 5', 'Source Text 5', 'no', 5, 'domain1', 'Alternates 5'),
       ('Original Text 6', 'Source Text 6', 'yes', 6, 'domain2', 'Alternates 6'),
       ('Original Text 7', 'Source Text 7', 'no', 7, 'domain1', 'Alternates 7'),
       ('Original Text 8', 'Source Text 8', 'yes', 8, 'domain2', 'Alternates 8'),
       ('Original Text 9', 'Source Text 9', 'no', 9, 'domain1', 'Alternates 9'),
       ('Original Text 10', 'Source Text 10', 'yes', 10, 'domain2', 'Alternates 10');
```
``` Insert Query for "content" Table: For testing```
```
INSERT INTO content (srctxt, tgttxt, multipart, part, domainname, alternates)
VALUES ('Source Text 1', 'Target Text 1', 'n', 1, 'domain1', 'Alternates 1'),
       ('Source Text 2', 'Target Text 2', 'y', 2, 'domain2', 'Alternates 2'),
       ('Source Text 3', 'Target Text 3', 'n', 3, 'domain1', 'Alternates 3'),
       ('Source Text 4', 'Target Text 4', 'y', 4, 'domain2', 'Alternates 4'),
       ('Source Text 5', 'Target Text 5', 'n', 5, 'domain1', 'Alternates 5'),
       ('Source Text 6', 'Target Text 6', 'y', 6, 'domain2', 'Alternates 6'),
       ('Source Text 7', 'Target Text 7', 'n', 7, 'domain1', 'Alternates 7'),
       ('Source Text 8', 'Target Text 8', 'y', 8, 'domain2', 'Alternates 8'),
       ('Source Text 9', 'Target Text 9', 'n', 9, 'domain1', 'Alternates 9'),
       ('Source Text 10', 'Target Text 10', 'y', 10, 'domain2', 'Alternates 10');
```

``` Insert Query for "translation" Table: For testing```
```
INSERT INTO translation (srctxt, tgttxt, multipart, part, domainname, alternates)
VALUES ('Source Text 1', 'Translation Text 1', 'n', 1, 'domain1', 'Alternates 1'),
       ('Source Text 2', 'Translation Text 2', 'y', 2, 'domain2', 'Alternates 2'),
       ('Source Text 3', 'Translation Text 3', 'n', 3, 'domain1', 'Alternates 3'),
       ('Source Text 4', 'Translation Text 4', 'y', 4, 'domain2', 'Alternates 4'),
       ('Source Text 5', 'Translation Text 5', 'n', 5, 'domain1', 'Alternates 5'),
       ('Source Text 6', 'Translation Text 6', 'y', 6, 'domain2', 'Alternates 6'),
       ('Source Text 7', 'Translation Text 7', 'n', 7, 'domain1', 'Alternates 7'),
       ('Source Text 8', 'Translation Text 8', 'y', 8, 'domain2', 'Alternates 8'),
       ('Source Text 9', 'Translation Text 9', 'n', 9, 'domain1', 'Alternates 9'),
       ('Source Text 10', 'Translation Text 10', 'y', 10, 'domain2', 'Alternates 10');
```



---

Document written and maintain by [Vilal Ali](https://vilal-ali.github.io/my-profile/index.html)

