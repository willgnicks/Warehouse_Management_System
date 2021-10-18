## gnicks
Django仓库系统
> 模块
  - 用户模块
  - 项目管理模块
  - 供应商管理模块
  - 产品管理模块
  - 采购模块
  - 入库模块
  - 出库模块
  - 借测模块
  - 领用模块
  - Dashboard模块
------
> 各模块均包含各自模型的增删改查，并且在后端除多对多复杂情况之外均使用utils中的函数方法来进行增删改查








    server {
        listen 80;
        server_name localhost;
        charset     utf-8;
        access_log      /data/destiny/nginx_access.log;
        error_log       /data/destiny/nginx_error.log;
        client_max_body_size 75M;
    
    
        location /static {
            alias /data/test/ware/static;
        }
    
        location / {
            include     /etc/nginx/conf/uwsgi_params;
            uwsgi_pass  127.0.0.1:8000;
        }
    }
