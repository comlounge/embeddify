
def test_youtube(embedder):
    assert embedder("https://www.youtube.com/watch?v=SC93q4tZeNI") == """<iframe width="560" height="315" src="https://www.youtube.com/embed/SC93q4tZeNI?feature=oembed" frameborder="0" allowfullscreen></iframe>"""


def test_slideshare(embedder):
    assert embedder("http://de.slideshare.net/mrtopf/open-government-vortrag-aachen").startswith("""<iframe src="https://www.slideshare.net/slideshow/embed_code/key/3wGhGoN6QUw5lR" width="427" height="356" """)


def test_flickr(embedder):
    assert embedder("http://www.flickr.com/photos/mrtopf/7780673842/") == """<img src="https://farm9.staticflickr.com/8297/7780673842_a57b60cd16_n.jpg" width="320" height="250">"""


def test_vimeo(embedder):
    assert embedder("http://vimeo.com/6791752").startswith("""<iframe src="https://player.vimeo.com/video/6791752" width="420" height="315" """)
    
def test_unknown_site(embedder):
    assert embedder("http://heise.de") == """http://heise.de"""
    
def test_youtube_not_found(embedder):
    assert embedder("https://www.youtube.com/watch?v=nothinghere") == "https://www.youtube.com/watch?v=nothinghere"
    
def test_slideshare_not_found(embedder):
    assert embedder("http://slideshare.net") == "http://slideshare.net"
    
def test_no_url(embedder):
    assert embedder("nourl") == "nourl"
