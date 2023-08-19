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


'
``` Insert Query for "collection" Table: For testing```
INSERT INTO collection (name) VALUES ('Collection 1');
INSERT INTO collection (name) VALUES ('Collection 2');
INSERT INTO collection (name) VALUES ('Collection 3');
'

'
``` Insert Query for "content" Table: For testing```
INSERT INTO content (srctxt, tgttxt, domainname, psrcmd5, multipart, part) VALUES ('Source Text 1', 'Target Text 1', 'Domain 1', 'psrcmd5_1', 0, 1);
INSERT INTO content (srctxt, tgttxt, domainname, psrcmd5, multipart, part) VALUES ('Source Text 2', 'Target Text 2', 'Domain 2', 'psrcmd5_2', 1, 2);
INSERT INTO content (srctxt, tgttxt, domainname, psrcmd5, multipart, part) VALUES ('Source Text 3', 'Target Text 3', 'Domain 3', 'psrcmd5_3', 0, 1);
'
