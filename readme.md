### 添加谷歌api key到Path中  
   
 Linux&Mac
 ```bash
 export GOOGLE_APPLICATION_CREDENTIALS="[PATH]"
 ```
 Windows CMD
 ```bash
 set GOOGLE_APPLICATION_CREDENTIALS=[PATH]
 ```
 Windows PowerShell
 ```bash
 $env:GOOGLE_APPLICATION_CREDENTIALS="[PATH]"
 ```
 > 例： `export GOOGLE_APPLICATION_CREDENTIALS="/home/user/Downloads/service-account-file.json"`

### 添加百度api key到Path中  

同上，但环境变量为 BAIDU_API_APPID 和 BAIDU_API_SECRETKEY
