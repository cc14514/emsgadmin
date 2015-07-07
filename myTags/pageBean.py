#/usr/bin/env python
#coding=utf8

from django.core.paginator import Paginator

class PageBean(object):
    '''
    简单分页封装
    '''
    pageSize = None 
    pageNo = None 
    totalCount = None 
    totalPage = None 
    data = None 
    prePage = 1
    nextPage = None

    def __init__(self,dataList,request=None,_pageSize=10,_pageNo=1):
        pageNo,pageSize = None,None 
        if request :
            try : pageSize = int(request.GET.get('pageSize'))
            except : pageSize = _pageSize
            try : pageNo = int(request.GET.get('pageNo'))
            except : pageNo = _pageNo
        else : 
            pageSize = _pageSize 
            pageNo = _pageNo 
        
        p = Paginator(dataList, pageSize)
        page = p.page(pageNo)
        self.pageSize = pageSize
        self.pageNo = pageNo
        self.totalCount = p.count
        self.totalPage = p.num_pages
        self.data = page.object_list
        try:
            self.prePage = page.previous_page_number()
        except:
            self.prePage = 1
        try:
            self.nextPage = page.next_page_number()
        except:
            self.nextPage = p.num_pages 
    
    
