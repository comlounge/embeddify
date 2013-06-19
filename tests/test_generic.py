
def test_youtube(embedder):
    assert embedder("https://www.youtube.com/watch?v=SC93q4tZeNI") == """<iframe width="560" height="315" src="http://www.youtube.com/embed/SC93q4tZeNI?feature=oembed" frameborder="0" allowfullscreen></iframe>"""


def test_slideshare(embedder):
    assert embedder("http://de.slideshare.net/mrtopf/open-government-vortrag-aachen") == """<iframe src="http://www.slideshare.net/slideshow/embed_code/13382702" width="427" height="356" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC;border-width:1px 1px 0;margin-bottom:5px" allowfullscreen webkitallowfullscreen mozallowfullscreen> </iframe> <div style="margin-bottom:5px"> <strong> <a href="http://www.slideshare.net/mrtopf/open-government-vortrag-aachen" title="OPen Government Vortrag Aachen" target="_blank">OPen Government Vortrag Aachen</a> </strong> from <strong><a href="http://www.slideshare.net/mrtopf" target="_blank">Christian Scholz</a></strong> </div>"""


def test_flickr(embedder):
    assert embedder("http://www.flickr.com/photos/mrtopf/7780673842/") == """<img src="http://farm9.staticflickr.com/8297/7780673842_a57b60cd16_n.jpg" width="320" height="250">"""


def test_vimeo(embedder):
    assert embedder("http://vimeo.com/6791752") == """<iframe src="http://player.vimeo.com/video/6791752" width="420" height="315" frameborder="0" webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe>"""
    
def test_unknown_site(embedder):
    assert embedder("http://heise.de") == """http://heise.de"""
    
def test_youtube_not_found(embedder):
    assert embedder("https://www.youtube.com/watch?v=nothinghere") == "https://www.youtube.com/watch?v=nothinghere"
    
def test_slideshare_not_found(embedder):
    assert embedder("http://slideshare.net") == "http://slideshare.net"
    
def test_no_url(embedder):
    assert embedder("nourl") == "nourl"
