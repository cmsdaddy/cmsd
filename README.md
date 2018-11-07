#cmsd
自定义基于select方法的循环式简单http服务器.


##支持的功能
* 普通http请求
* http长连接
* websocket
* 扩展TCP通讯
* 兼容django渲染模板


##使用http服务器
###创建视图文件view.py
    import path
    from response import *
    from template import render

    @path.route(path='/', method=['GET'])
    def index(request):
        return render(request, "index.html")
 
    
    @path.route(path='/redir/', method=['GET'])
    def index(request):
        return HttpResponseRedirect("http://www.baidu.com")
    
    
    @path.route(path='/json/', method=['GET'])
    def index(request):
        return {'id': 1, "name": "cmsd"}
    
    
    @path.route(path='/print/<str:msg>/<int:id>', method=['GET', 'POST'])
    def index(request, msg, id):
        return msg + str(id)


    @path.route(path='/live/', method=['GET'])
    def index(request):
        try:
            if request.headers['Upgrade'] != 'websocket':
                raise TypeError
            if request.headers['Connection'] != 'Upgrade':
                raise TypeError
        except:
            return HttpResponseBadRequest()
    
        return HttpResponseWebSocket(request)
###创建测试文件test.py
    from request import HttpRequest
    from httpd import TCPServerBasic

    server = TCPServerBasic('127.0.0.1', 8000, HttpRequest)
    server.run_forever()
