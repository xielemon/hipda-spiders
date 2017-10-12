class ProxyMiddleware(object):
    def process_request(self,request,spider):
        request.meta['proxy']='https://59.42.41.98:9797'