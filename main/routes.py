from flask import Flask, make_response, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={
    r"/*": {
       "origins": "*",
        "supports_credentials": True,
        "methods": ["GET", "POST"],
        "headers": ["Content-Type"]
    }
})

#db_config = {'user': 'root', 'password': 'sincostan', 'host': 'localhost', 'database': 'tribedb'}
db_config = {'user': 'root', 'password': 'cohondob', 'host': 'localhost', 'database': 'tribedb'}


def connect_to_database():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except Exception as e:
        raise e

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/dtest', methods=['GET'])
def dtest():
    return jsonify({"message": "api data accessed without db..."})


def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response()

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def update_domain_tbl(mergedsrcmd5, sortedData, cursor):
    for row in sortedData:
        rowId = row['id']
        rowMultipart = row['multipart']
        rowPart = row['part']
        rowDomainname = row['domainname']
        query = "UPDATE content SET psrcmd5 = %s, multipart = %s, part = %s, domainname=%s WHERE id = %s"
        values = (mergedsrcmd5, rowMultipart, rowPart, rowDomainname, rowId)
        cursor.execute(query, values)

# collection tbl data
@app.route('/collectionTableData', methods=['GET'])
def search():
    try:
        connection = connect_to_database()
        cursor = connection.cursor(dictionary=True)
        query = f"SELECT *, DATE_FORMAT(lastmodified, '%e:%m:%Y %H:%i:%s') AS formatted_date FROM collection ORDER BY `id` DESC"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return _corsify_actual_response(jsonify(rows))
    except Exception as e:
        return {"error": str(e)}

# source text transfer in Domain tbl
@app.route('/transferToDomain', methods=['POST'])
def update():
    reqDataUpdate = request.get_json()
    if not reqDataUpdate:
        return jsonify({"message": "No data provided"}), 400
    print(f"transfer data for Domain table : \n {reqDataUpdate}")

    sortedData = sorted(reqDataUpdate, key=lambda item: int(item['id']))
    inserted_entries = []
    duplicate_entries = []

    try:
        connection = connect_to_database()
        cursor = connection.cursor(dictionary=True)
        for row in sortedData:
            srcText = row.get('srctxt', '').strip()
            domainname = row.get('domainname', '').strip()
            if srcText:
                queryForDuplicate = "SELECT COUNT(*) FROM content WHERE srctxt = %s AND domainname=%s"
                cursor.execute(queryForDuplicate, (srcText,domainname,))
                duplicateCount = cursor.fetchone()['COUNT(*)']

                if duplicateCount > 0:
                    print(f"duplicate row : {duplicateCount}")
                    duplicate_entries.append(srcText)
                elif duplicateCount == 0:
                    queryInsert = "INSERT INTO content (srctxt, domainname) VALUES (%s, %s)"
                    cursor.execute(queryInsert, (srcText,domainname,))
                    inserted_entries.append(srcText)

        connection.commit()
        connection.close()

        message = "Data transferred successfully.\n"
        if inserted_entries:
            message += "Inserted:\n" +f"Inserted entries : {len(inserted_entries)}\n" + "\n"
        if duplicate_entries:
            message += "\nDuplicate entries:\n" +f"Duplicate entries : {len(duplicate_entries)}\n"

        return _corsify_actual_response(jsonify({"message": message}))

    except Exception as e:
        return _corsify_actual_response(jsonify({"message": str(e)}))


# source text transfer in Domain tbl
@app.route('/translationToToDomain', methods=['POST'])
def translationToToDomain():
    reqData = request.get_json()
    if not reqData:
        return jsonify({"message": "No data provided"}), 400
    print(f"transfer data for Domain table : \n {reqData}")

    sortedData = sorted(reqData, key=lambda item: int(item['id']))
    update_entries = []

    try:
        connection = connect_to_database()
        cursor = connection.cursor(dictionary=True)
        for row in sortedData:
            tgtText = row.get('tgttxt', '').strip()
            print(tgtText)
            srcTextmd5 = row.get('srcmd5', '').strip()
            print(srcTextmd5)
            domainname = row.get('domainname', '').strip()
            if tgtText:
                queryUpdate = "UPDATE content SET tgttxt = %s WHERE srcmd5=%s AND domainname=%s"
                cursor.execute(queryUpdate, (tgtText, srcTextmd5, domainname,))
                update_entries.append(srcTextmd5)

        connection.commit()
        cursor.close()
        connection.close()

        message = "Data transferred..\n"
        if update_entries:
            message += f"Update entries : {len(update_entries)}\n" + "\n"
        return _corsify_actual_response(jsonify({"message": message}))

    except Exception as e:
        return _corsify_actual_response(jsonify({"message": str(e)}))


#Domain Table fetch data from content table(transfer data table)!
@app.route('/DomainTableData', methods=['GET'])
def content():
    try:
        connection = connect_to_database()
        cursor = connection.cursor(dictionary=True)
        query = f"SELECT *, DATE_FORMAT(lastmodified, '%e:%m:%Y %H:%i:%s') AS formatted_date FROM content ORDER BY `id` DESC"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return _corsify_actual_response(jsonify(rows))
    except Exception as e:
        return _corsify_actual_response({"error": str(e)})
    

#Domain Table fetch data from content table(transfer data table)!
@app.route('/sagigation', methods=['GET', 'POST'])
def sagigation():
    try:
        connection = connect_to_database()
        cursor = connection.cursor(dictionary=True)
        query = f"SELECT *, DATE_FORMAT(lastmodified, '%e:%m:%Y %H:%i:%s') AS formatted_date FROM content ORDER BY `id` ASC"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return _corsify_actual_response(jsonify(rows))
    except Exception as e:
        return _corsify_actual_response({"error": str(e)})

# merged and transfer!
@app.route('/mergedAndTransfer', methods=['POST'])
def merged_transfer():
    reqDataMerge = request.get_json()
    print(f"merged data from table : \n {reqDataMerge} ")
    sorted_data = sorted(reqDataMerge, key=lambda item: int(item['part']))
    mergedItems = ' '.join(item['srctxt'] for item in sorted_data)
    mergedsrcmd5 = '###'.join(item['srcmd5'] for item in sorted_data)
    domainname = sorted_data[0]['domainname']
    Mergedmultipart = sorted_data[0]['multipart']
    print(domainname)
    print(f"meergedsrcmd5 {mergedsrcmd5}")
    connection = connect_to_database()
    cursor = connection.cursor(dictionary=True)
    try:
        if mergedsrcmd5:
            query_check_duplicate = "SELECT COUNT(*) FROM translation WHERE srctxt = %s AND domainname=%s"
            cursor.execute(query_check_duplicate, (mergedItems, domainname,))
            duplicate_count = cursor.fetchone()['COUNT(*)']
            if duplicate_count == 0:
                query = f"INSERT INTO `translation` (srctxt, psrcmd5, multipart) VALUES (%s, %s, %s)"
                values = (mergedItems, mergedsrcmd5, Mergedmultipart)
                
                cursor.execute(query, values)
                update_domain_tbl(mergedsrcmd5, sorted_data, cursor)
                connection.commit()
                return jsonify({"message": f"insert entry : {mergedsrcmd5}"})
            elif duplicate_count > 0:
                message = f"duplicate entry {mergedsrcmd5}"
                return jsonify({"message": message})
    except Exception as e:
        return {"message": str(e)}



# Translation table data from domain table!
@app.route('/translation', methods=['GET'])
def translation():
    try:
        connection = connect_to_database()
        cursor = connection.cursor(dictionary=True)
        query = f"SELECT *, DATE_FORMAT(lastmodified, '%e:%m:%Y %H:%i:%s') AS formatted_date FROM `translation` ORDER BY `lastmodified` DESC"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return _corsify_actual_response(jsonify(rows))
    except Exception as e:
        return _corsify_actual_response({"error": str(e)})

@app.route('/singleTransfer', methods=['GET', 'POST'])
def contentSingleInsert():
    reqDataUpdate = request.get_json()
    flaginsert = 0
    flagNotinsert = 0
    for rowData in reqDataUpdate:
        srcText = rowData['srctxt']
        domainName = rowData['domainname']
        try:
            connection = connect_to_database()
            cursor = connection.cursor(dictionary=True)
            if srcText:
                query_check_duplicate = "SELECT COUNT(*) FROM translation WHERE srctxt = %s AND domainname=%s"
                cursor.execute(query_check_duplicate, (srcText,domainName,))
                duplicate_count = cursor.fetchone()['COUNT(*)']
                if duplicate_count == 0:
                    query = f"INSERT INTO `translation` (srctxt, domainname) VALUES ('{srcText}', '{domainName}')"
                    cursor.execute(query)
                    connection.commit()
                    flaginsert +=1
                elif duplicate_count > 0:
                    flagNotinsert +=1
                    message = f"duplicate entry {srcText}"
        except Exception as e:
            return {"message": str(e)}

    connection.commit()
    connection.close()

    message = "Data inserted information -\n"
    if flaginsert:
        message += f"Inserted entries : {flaginsert}"
    if flagNotinsert:
        message += "\n" + f"Duplicate entries : {flagNotinsert}"

    return _corsify_actual_response(jsonify({"message": message}))
        

@app.route('/fileUploader/v1', methods=['POST'])
def fileUploader():
    if 'file' not in request.files:
        return 'No file was uploaded.', 400
    file = request.files['file']
    if file and allowed_file(file.filename):
        fileName = file.filename
        fileContent = file.read().decode('utf-8')
        print(f"fileContent {fileName}\n {fileContent}")
        lines = fileContent.split("\n")
        for line in lines:
            if line.strip():
                query = "INSERT IGNORE INTO collection (srctxt) VALUES (%s)"
                values = (line,)
                connection = connect_to_database()
                cursor = connection.cursor(dictionary=True)
                cursor.execute(query, values)
                message = connection.commit()
        return 'File uploaded and details inserted into the database.' 
    else:
        return 'Invalid file format.', 400

@app.route('/update/v1/<int:id>', methods=['POST'])
def update1(id):
    try:
        connection = connect_to_database()
        cursor = connection.cursor(dictionary=True)
        query = f"SELECT * FROM content WHERE id = %s"
        cursor.execute(query, (id,))
        data = cursor.fetchone()
        
        if data:
            new_tgttxt = request.json.get('tgttxt')
            print(new_tgttxt)
            query_update = f"UPDATE content SET tgttxt = %s WHERE id = %s"
            cursor.execute(query_update, (new_tgttxt, id))
            connection.commit()
            
            cursor.close()
            connection.close()
            
            return jsonify({"message": "Updated successfully"})
        else:
            cursor.close()
            connection.close()
            return jsonify({'message': 'Data not found'}), 404
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
