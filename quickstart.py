import httplib2 
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials	

CREDENTIALS_FILE = 'credentials.json'  # Имя файла с закрытым ключом, вы должны подставить свое

# Читаем ключи из файла
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])

httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API 


# spreadsheet = service.spreadsheets().create(body = {
#     'properties': {'title': 'Parse_facebook', 'locale': 'ru_RU'},
#     'sheets': [{'properties': {'sheetType': 'GRID',
#                                'sheetId': 0,
#                                'title': 'Sheet1',
#                                'gridProperties': {'rowCount': 100, 'columnCount': 15}}}]
# }).execute()
# spreadsheetId = spreadsheet['spreadsheetId'] # сохраняем идентификатор файла
def gh_insert(data, num):
    spreadsheetId = '164e27z144yhgVLlG38VmVDM3mywuruo_V7CWnwh1ANw' # сохраняем идентификатор файла

    driveService = apiclient.discovery.build('drive', 'v3', http = httpAuth) # Выбираем работу с Google Drive и 3 версию API
    access = driveService.permissions().create(
        fileId = spreadsheetId,
        body = {'type': 'user', 'role': 'writer', 'emailAddress': 'Wotdimas@gmail.com'},  # Открываем доступ на редактирование
        fields = 'id'
    ).execute()

    results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
        "valueInputOption": "USER_ENTERED", # Данные воспринимаются, как вводимые пользователем (считается значение формул)
        "data": [
            {"range": f"Sheet1!A{num}:K{num}",
             "majorDimension": "ROWS",     # Сначала заполнять строки, затем столбцы
             "values": data
             }
        ]
    }).execute()

    print('https://docs.google.com/spreadsheets/d/' + spreadsheetId)

def get_product(from_, to_):
    spreadsheetId = '164e27z144yhgVLlG38VmVDM3mywuruo_V7CWnwh1ANw'  # сохраняем идентификатор файла

    driveService = apiclient.discovery.build('drive', 'v3',
                                             http=httpAuth)  # Выбираем работу с Google Drive и 3 версию API
    access = driveService.permissions().create(
        fileId=spreadsheetId,
        body={'type': 'user', 'role': 'writer', 'emailAddress': 'Wotdimas@gmail.com'},
        # Открываем доступ на редактирование
        fields='id'
    ).execute()

    ranges = [f"Sheet1!{from_}:{to_}"]  #

    results = service.spreadsheets().values().batchGet(spreadsheetId=spreadsheetId,
                                                       ranges=ranges,
                                                       valueRenderOption='FORMATTED_VALUE',
                                                       dateTimeRenderOption='FORMATTED_STRING').execute()
    sheet_values = results['valueRanges'][0]['values']
    print(sheet_values)
    return sheet_values
# gh_insert([['sdfgsdg', 'sdgdfg'], ['sdgdsfg', 'srfdgdfg'], ['dfgf'], ['dfg'], ['sdfgsdg', 'sdgdfg'], ['sdgdsfg', 'srfdgdfg'], ['dfgf'], ['dfg']])