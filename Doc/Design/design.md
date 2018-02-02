# script-爬蟲部份
### 
    * spider
        * set 書名
        * 
    * content_parse
    * data_check

### 流程
1. python3 index.php 指令輸入看要爬啥and 爬的範圍

### 2018/02/01 新的流程想法
1. 依照Data/index.json裡面內容

index.json
{
    index_number: {
        name: 書名,
        data_source: {
            index: {
                web_name: 資料來源網站名,
                web_url: 來源網站網址
            }
        }
    }
}

