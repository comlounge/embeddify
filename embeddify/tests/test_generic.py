
def test_youtube(embedder):
    result = embedder("https://www.youtube.com/watch?v=SC93q4tZeNI")
    assert '<iframe' in result
    assert 'src="https://www.youtube.com/embed/SC93q4tZeNI' in result
    assert 'width="560"' in result
    assert 'height="315"' in result
    assert result.data['thumbnail_url'] == u'https://i.ytimg.com/vi/SC93q4tZeNI/hqdefault.jpg'
    assert isinstance(result, embedder.OEmbedMarkup)
    result = embedder("https://youtu.be/SC93q4tZeNI")
    assert '<iframe' in result
    assert 'src="https://www.youtube.com/embed/SC93q4tZeNI' in result
    assert 'width="560"' in result
    assert 'height="315"' in result
    assert result.data['thumbnail_url'] == u'https://i.ytimg.com/vi/SC93q4tZeNI/hqdefault.jpg'
    assert isinstance(result, embedder.OEmbedMarkup)


def test_slideshare(embedder):
    result = embedder("http://de.slideshare.net/mrtopf/open-government-vortrag-aachen")
    assert '<iframe' in result
    assert 'src="https://www.slideshare.net/slideshow/embed_code/key/3wGhGoN6QUw5lR' in result
    assert 'width="427"' in result
    assert 'height="356"' in result
    assert result.data['thumbnail_url'].startswith(u'https://cdn.slidesharecdn.com/ss_thumbnails/opengov-aachen-120619124815-phpapp02-thumbnail.jpg')
    assert isinstance(result, embedder.OEmbedMarkup)


def test_flickr(embedder):
    result = embedder("http://www.flickr.com/photos/mrtopf/7780673842/")
    assert result == """<a target="flickr" href="https://www.flickr.com/photos/mrtopf/7780673842/"><img src="https://live.staticflickr.com/8297/7780673842_a57b60cd16_n.jpg" class="flickr-embed-img" alt="professionelle politische Kommunikation" width="320" height="250"></a>"""
    assert result.data['thumbnail_url'] == u'https://live.staticflickr.com/8297/7780673842_a57b60cd16_q.jpg'
    assert isinstance(result, embedder.OEmbedMarkup)


def test_vimeo(embedder):
    result = embedder("http://vimeo.com/6791752")
    assert 'src="https://player.vimeo.com/video/6791752' in result
    assert 'width="420"' in result
    assert 'height="315"' in result
    assert u'https://i.vimeocdn.com/video/27011558' in result.data['thumbnail_url']
    assert u'295x166' in result.data['thumbnail_url']
    assert isinstance(result, embedder.OEmbedMarkup)


def skip_facebook(embedder):  # disabled the test, because an access token is required
    result = embedder("https://www.facebook.com/facebook/videos/10153231379946729/")
    assert 'data-href="https://www.facebook.com/facebook/videos/10153231379946729/"' in result
    assert 'thumbnail_url' not in result.data
    assert isinstance(result, embedder.OEmbedMarkup)
    result = embedder("https://www.facebook.com/video.php?v=10153231379946729")
    assert 'data-href="https://www.facebook.com/video.php?v=10153231379946729"' in result
    assert 'thumbnail_url' not in result.data
    assert isinstance(result, embedder.OEmbedMarkup)


def test_unknown_site(embedder):
    result = embedder("http://heise.de")
    assert result == """http://heise.de"""
    assert not isinstance(result, embedder.OEmbedMarkup)


def test_youtube_not_found(embedder):
    result = embedder("https://www.youtube.com/watch?v=nothinghere")
    assert result == "https://www.youtube.com/watch?v=nothinghere"
    assert not isinstance(result, embedder.OEmbedMarkup)


def test_slideshare_not_found(embedder):
    result = embedder("http://slideshare.net")
    assert result == "http://slideshare.net"
    assert not isinstance(result, embedder.OEmbedMarkup)


def test_no_url(embedder):
    result = embedder("nourl")
    assert result == "nourl"
    assert not isinstance(result, embedder.OEmbedMarkup)
