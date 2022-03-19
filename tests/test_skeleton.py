from brokenurls.skeleton import getURLs, isImage

def test_getURLs():
    """API Tests"""
    assert getURLs("<html></html>","href","a[href]") == []
    assert getURLs("<html><body><a href='test' /></body></html>", "href", "a[href]") == ['test']
    assert getURLs("<html><body><a name='test' /></body></html>", "href", "a[href]") != ['test']
    assert getURLs("<html><body><img src='test' /></body></html>", "src", "img[src]") == ['test']
    assert getURLs("<html><body><img src='test' /></body></html>", "href", "a[href]") != ['test']

def test_isImage():
    """API Tests"""
    assert isImage("https://mysite/resource.png") == True
    assert isImage("https://mysite/resource.jpeg") == True
    assert isImage("https://mysite/resource.jpg") == True
    assert isImage("https://mysite/resource.svg") == True
    assert isImage("https://mysite/resource.html") == False
    assert isImage("https://mysite.html") == False