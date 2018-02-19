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
        source: {
            index: {
                web_name: 資料來源網站名,
                web_url: 來源網站網址
            }
        }
    }
}

### 2018/02/19 選用前端技術
[https://lavas.baidu.com/](lavas 官方文件)

### 2018/02/19 api流程釐清

* auth
    1. /api/register
    2. /api/login
    3. /api/logout
    4. /api/user
    5. /api/forget (暫時不用做)
    6. /api/reset  (暫時不用做)

* novel
    1. /api/novel/{id}      #輸出文章
    2. /api/novel/search    #搜尋書籍
    3. /api/novel/download  #下載書籍 (暫時不用做)
    4. /api/bookmark/       #新增書籤 put
    5. /api/bookmark/       #書籤列表 get
    6. /api/bookmark/       #刪除書籤 delete
    7. /api/bookmark/       #更新書籤 post
    8. /api/bookmark/search #搜尋書籤 (暫時不用做)