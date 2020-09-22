import CloudFlare       #匯入cloudflare模組
 
cf = CloudFlare.CloudFlare(token="hv6Amq71guOUczpQHsCETPmqpTsuVo6d0Vtv9AJn")   #給予cloudflare的class類別token值，賦予它取值&編輯&刪除的權限
zones = cf.zones.get(params={'per_page':100})   #取得帳號下的的zone站台列表，per_page是指取得100個zone站台資訊，不給予per_page預設是20個
 
for zone in sorted(zones, key=lambda v: v['name']):     #將zones列表分別按照name的排序取出值，並將之賦予給zone的區域內(僅在這個for區域)的變數
    zone_name = zone['name']    #將zone內的name資料賦予給zone_name變數(也就是zone站台名稱)
    zone_id = zone['id']        #將zone內的id資料賦予給zone_id變數(也就是zone站台id)
    zone_plan = zone['plan']['name']        #將zone內的plan資料賦予給zone_plan變數(也就是zone站台的商業付費等級)
    if zone_plan != "Enterprise Website":   #判斷該zone的商業付費等級是否符合Enterprise Website等級
        continue    #如果商業等級不等於Enterprise Website則跳出這次的for迴圈，繼續下一個迴圈取新的zone資訊

    print("目前處理", zone_name, "區域")     #顯示目前zone的進度
    page_number = 1                 #設置一個頁面數並給予值，後面用來判斷是否進行迴圈

    while page_number != 0:         #當頁面數不等於0時，會進入迴圈並持續的取值zone下的網域資訊出來
        custom_info_list = cf.zones.custom_hostnames.get(zone_id, params={'page':page_number, 'per_page': 30})      #透過custom_hostname給予zone_id後，拿取域名，每頁30個
        print("目前在第", page_number, "頁")        #顯示頁數資訊
        for hostname_info in custom_info_list:      #將custom_list_info列表中的域名資訊內的data逐一賦予給hostname_info
            hostname = hostname_info['hostname']       #將hostname_info內的hostname資料賦予給hostname
            hostname_id = hostname_info['id']          #將hostname_info內的id資料賦予給hostname_id

            try:
                print("Enable", hostname, "Wildcard設定為開啟(True)")                 #列出要準備刪除的域名與對應的域名ID
                data = {"ssl": {"method": "http", "wildcard": True, "type": "dv"}}   #配置Patch的data，讓Wildcard開啟，data內的參數皆為force必填，可選項要參考官網
                cf.zones.custom_hostnames.patch(zone_id, hostname_id, data=data)     #透過cf帶著token去將給予的zone_id下的hostname配置成給予的data資料(wildcard：True)
            except CloudFlare.exceptions.CloudFlareAPIError as e:       #用except去承接如果有發生錯誤的話
                    exit('api error: %d %s' % (e, e))                       #離開且顯示錯誤的api資訊訊息與錯誤碼


        page_number += 1            #取得本頁資訊後，將頁面數+1跳至下一頁讓迴圈去跑
        if custom_info_list == []:  #如果迴圈取得的當頁面的網域資訊是空的(代表已跑完該zone)，就會進入if區塊內
            break                   #進到if區塊內及代表該zone全數跑完畢，及使用break跳出while迴圈
                

