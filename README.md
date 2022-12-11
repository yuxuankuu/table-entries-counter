# table-entries-counter
Count the specific tables and record with csv file

1. 目的: 紀錄特定資料表，在不同條件下的資料筆數結果，透過定期排程的執行，觀察資料筆數增長情況。
2. 使用方式: 在 config.ini 設定 database 連線資訊、帳號密碼和輸出路徑。(帳號須有足夠權限執行特定sql command)
3. 執行後將會逐行執行sql file，並寫入csv file。
