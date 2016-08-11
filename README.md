SDN 从入门到放弃

其实没什么意思的...

### 介绍
2016年, 全国SDN创新...大赛决赛作品

### 模块简介
./Node.py, ./Link.py 只是定义了数据类型
./Topo.py 从 Mininet + Floodlight 中获取拓扑信息
./Network.py 利用 ./Topo.py 中获取的信息进行网络图论方面的处理
./Server.py 是采用 B/S 架构来实现 WEB 对运行的服务器的访问

./links_switch
./hosts
./switchs 三个文件是第一次运行 Mininet + Floodlight 后获取的拓扑信息,保存到本地,不用以后每次都打开控制器了

### 运行
./Server.py 监听 5000 端口, 因为采用了 Flask 框架
