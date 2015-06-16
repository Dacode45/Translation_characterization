FOR /f "delims=" %%i IN ('*.xlsx /b') DO ExcelToCSV.vbs "%%i" "%%i.csv"
