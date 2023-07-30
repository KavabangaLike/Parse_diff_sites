import json

s = "\\u041a\\u0432\\u0430\\u0440\\u0442\\u0438\\u0440\\u0430', '1 \\u0441\\u043f\\u0430\\u043b\\u044c\\u043d\\u044f \\u00b7 1 \\u0441\\u0430\\u043d\\u0443\\u0437\\u0435".encode('utf-8').decode('unicode-escape')
print(s)