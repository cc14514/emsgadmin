# /usr/bin/env python
# coding=utf8

import pycurl, json

appid = 'sara'
appkey = 'sara'


class Storage:
    def __init__(self):
        self.contents = ''

    def store(self, buf):
        self.contents = "%s%s" % (self.contents, buf)

    def __str__(self):
        return self.contents


def upload(file_path=None, file_type='image', url=None):
    retrieved_body = Storage()
    retrieved_headers = Storage()
    c = pycurl.Curl()
    c.setopt(c.URL, 'http://fileserver.lczybj.com/fileserver/upload/')

    opts = [
        ('appid', (c.FORM_CONTENTS, appid)),
        ('appkey', (c.FORM_CONTENTS, appkey)),
        ('watermark', (c.FORM_CONTENTS, 'false')),
        ('file_type', (c.FORM_CONTENTS, file_type)),
    ]
    if file_path:
        opts.append(('file', (c.FORM_FILE, file_path)))

    if url:
        opts.append(('url', (c.FORM_CONTENTS, url)))

    c.setopt(pycurl.HTTPPOST, opts)

    c.setopt(c.WRITEFUNCTION, retrieved_body.store)
    c.setopt(c.HEADERFUNCTION, retrieved_headers.store)
    c.perform()
    c.close()
    rtn = '%s' % retrieved_body
    return json.loads(rtn)


def get_file_url(file_id):
    return 'http://fileserver.lczybj.com/fileserver/get/%s' % file_id


if __name__ == '__main__':
    success = upload('/mgr/sara.png')
    print success
    print type(success)

'''
上传地址 http://fileserver.lczybj.com/fileserver/upload/

下载地址 http://fileserver.lczybj.com/fileserver/get/文件id?token=xxx  如果是需要鉴权的资源则必须填写token参数

索引信息 http://fileserver.lczybj.com/fileserver/info/文件id

获取token http://fileserver.lczybj.com/fileserver/token/ 只接收post请求，参数 appid、appkey

删除地址 http://fileserver.lczybj.com/fileserver/del/ 只接收post请求，参数 id、appid、appkey ，如果是需要鉴权的资源则必须填写token参数并忽略appid、appkey
    不需要鉴权时，post 传递参数 id、appid、appkey 完成删除
    需要鉴权时，post 传递参数 id、token 完成删除


在程序中模拟以下表单，即可完成附件上传，参数名与含义参见表单内注释
<form action="http://fileserver.lczybj.com/fileserver/upload/" method="POST" enctype="multipart/form-data" >
        <!-- 应用名,由后台注册提供 -->
        <p>appid:<input type="text" name="appid" value="test"/></p>
        <!-- 应用名对应的开发者许可,由后台注册提供-->
        <p>appkey:<input type="text" name="appkey" value="test"/></p>
        <!-- 如果需要更新附件，则需指明id，新增时此参数为空即可 -->
        <p>id:<input type="text" name="id" value="" /></p>
        <!-- 附件类型，file / image 文件或 image，默认 image -->
        <p>file_type:<input type="text" name="file_type" value="image" /></p>
        <!-- # 是否加水印, 如果 file_type=image 则默认 true,可选值 true / false -->
        <p>watermark:<input type="text" name="watermark" value="true" /></p>
        <!-- # 下载和删除资源时是否需要鉴权，auth=true 鉴权，auth=false 不鉴权，默认 false -->
        <p>auth:<input type="text" name="auth" value="false" /></p>
        <!-- # 根据 url 来抓去图片,优先级高于 file  -->
        <p>url:<input type="text" name="url" value="" /></p>
        <!-- 附件 -->
        <p>file:<input type="file" name="file" /></p>
        <button type="submit">submit</button>
</form>

上传成功时返回：{"success":true,"entity":{"id":"文件id"}}
上传失败时返回：{"success":false,"entity":{"reason":"..."}}

文件id需要业务系统自行保存，读取和删除文件时需要使用此id

下载成功时直接返回文件流到请求端(content_type='text/plain;charset=utf8'),其中文件大小在 Content-Length 属性中返回；
下载失败时返回：not_found 等字符串

'''
