from embeddify import Embedder, YouTube

def test_generic_youtube():
    embedder = Embedder(width=200)
    assert embedder("https://www.youtube.com/watch?v=2wii8hfNkzE") == """<iframe width="200" height="113" src="http://www.youtube.com/embed/2wii8hfNkzE?feature=oembed" frameborder="0" allowfullscreen></iframe>"""

def test_generic_slideshare():
    embedder = Embedder(width=200)
    assert embedder("http://de.slideshare.net/mrtopf/open-government-vortrag-aachen") == """<iframe src="http://www.slideshare.net/slideshow/embed_code/13382702" width="202" height="316" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC;border-width:1px 1px 0;margin-bottom:5px" allowfullscreen webkitallowfullscreen mozallowfullscreen> </iframe> <div style="margin-bottom:5px"> <strong> <a href="http://www.slideshare.net/mrtopf/open-government-vortrag-aachen" title="OPen Government Vortrag Aachen" target="_blank">OPen Government Vortrag Aachen</a> </strong> from <strong><a href="http://www.slideshare.net/mrtopf" target="_blank">Christian Scholz</a></strong> </div>"""

def test_plugin_specific_config():
    cfg = {
        'youtube' : {'width' : 200 },
        'slideshare' : {'width' : 500 }
    }
    embedder = Embedder(plugin_config=cfg)
    assert embedder("https://www.youtube.com/watch?v=2wii8hfNkzE") == """<iframe width="200" height="113" src="http://www.youtube.com/embed/2wii8hfNkzE?feature=oembed" frameborder="0" allowfullscreen></iframe>"""

    assert embedder("http://de.slideshare.net/mrtopf/open-government-vortrag-aachen") == """<iframe src="http://www.slideshare.net/slideshow/embed_code/13382702" width="427" height="356" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC;border-width:1px 1px 0;margin-bottom:5px" allowfullscreen webkitallowfullscreen mozallowfullscreen> </iframe> <div style="margin-bottom:5px"> <strong> <a href="http://www.slideshare.net/mrtopf/open-government-vortrag-aachen" title="OPen Government Vortrag Aachen" target="_blank">OPen Government Vortrag Aachen</a> </strong> from <strong><a href="http://www.slideshare.net/mrtopf" target="_blank">Christian Scholz</a></strong> </div>"""

def test_plugin_selection():
    """only use youtube"""
    embedder = Embedder(plugins = [YouTube()])
    assert embedder("https://www.youtube.com/watch?v=2wii8hfNkzE") == """<iframe width="560" height="315" src="http://www.youtube.com/embed/2wii8hfNkzE?feature=oembed" frameborder="0" allowfullscreen></iframe>"""
    assert embedder("http://de.slideshare.net/mrtopf/open-government-vortrag-aachen") == "http://de.slideshare.net/mrtopf/open-government-vortrag-aachen"

def test_by_call_configuration():
    embedder = Embedder()
    assert embedder("https://www.youtube.com/watch?v=2wii8hfNkzE", width=200) == """<iframe width="200" height="113" src="http://www.youtube.com/embed/2wii8hfNkzE?feature=oembed" frameborder="0" allowfullscreen></iframe>"""
