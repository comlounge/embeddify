=========
embeddify
=========

Turns links into embed codes. Useful for any system accepting user inputs which wants to make
it easier for the user to add rich content and safer for the platform at the same time by
not allowing any direct iframe tags.

Usage
=====


Here is a quick example::

    >>> from embeddify import Embedder
    >>> embedder = Embedder()
    >>> embedder("https://www.youtube.com/watch?v=2wii8hfNkzE")
    <iframe width="560" height="315" src="http://www.youtube.com/embed/2wii8hfNkzE?feature=oembed" frameborder="0" allowfullscreen></iframe>

This works right now for

* youtube.com (plugin name: ``youtube``)
* vimeo.com (plugin name: ``vimeo``)
* flickr.com (plugin name: ``flickr``)
* slideshare.net (plugin name: ``slideshare``)
* facebook.com videos (plugin name: ``facebookvideos``)

The raw OEmbed data can be accessed via the ``data`` attribute of the result if the result is an ``OEmbedMarkup`` instance::

    >>> result = embedder("https://www.youtube.com/watch?v=2wii8hfNkzE")
    >>> isinstance(result, embedder.OEmbedMarkup)
    True
    >>> result.data['thumbnail_url']
    https://i.ytimg.com/vi/2wii8hfNkzE/hqdefault.jpg

If a link can not be converted then the link will be returned.


Configuration
=============

You can configure the embedding tool by giving it a width and height to be used. This is given as maximum width/height to the
oEmbed endpoints of the services and thus the resulting object might be smaller.

You can configure this for all embed plugins generically like this::
    
    embedder = Embedder(width=100, height=100)

You can also configure it on a per plugin basis using the plugin name mentioned above like this::
   
    plugin_config = {
        'youtube': {'width' : 200},
        'slideshare': {'width' : 500},
    }
    embedder = Embedder(plugin_config = plugin_config)

The plugin specific configuration overwrites the generic configuration.

You can also pass in arguments on a call by call basis like this::

    embedder = Embedder()
    embedder("https://www.youtube.com/watch?v=2wii8hfNkzE", width=200)

Autoplay
--------

Some providers support autoplay. You can use it with the autoplay setting::

    embedder = Embedder(autoplay=True)

Normally YouTube wouldn't support this setting, but the YouTube plugin handles
it by rewriting the returned HTML code. This may break if YouTube ever changes
the HTML code.

Additional parameters
---------------------

Some OEmbed providers allow additional parameters. For example Vimeo allows
autoplay::

    >>> embedder('https://player.vimeo.com/video/6791752', params=dict(autoplay=True))
    <iframe src="https://player.vimeo.com/video/6791752?autoplay=1" width="420" height="315" frameborder="0" title="Intro Presentation for the Open Platforms Panel at the Community &amp; Marketing Summit" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>


Choosing which plugins to use
-----------------------------

If you don't want all the plugins to be active you can choose which ones you want to use by providing a list
of plugins to use like this::
   
    import embeddify
    plugins = [embeddify.YouTube(), embeddify.Vimeo()] # only video
    embedder = Embedder(plugins = plugins)
    

Creating your own plugins
=========================

In order to extend the functionality with additional services you can create your own plugins. Depending on
the service and whether it provides an `oEmbed endpoint <http://www.oembed.com/>`_ or not you can one of two base classes, 
``Plugin`` or ``OEmbedPlugin``.

Using an oEmbed endpoint
------------------------

In order to write a plugin for an oEmbed enabled service you need to know it's endpoint. For instance the YouTube implementation
simply looks like this::


    from embeddify import OEmbedPlugin

    class YouTube(OEmbedPlugin):
        """converts youtube links into embeds
        """

        api_url = "http://www.youtube.com/oembed"

        def test(self, parts):
            """test if the plugin is able to convert that link"""
            return "youtube.com" in parts.netloc


So you simply need to put in the URL of the endpoint and a ``test()`` method. This gets the result of the
``urlparse.urlparse()`` call as input and usually simply checks the ``netloc`` attribute for the right domain.
If it returns ``False`` the next plugin will be tried, if it returns ``True`` the endpoint will be called and
in case that call was successful, the embed code will be returned. Otherwise again the next plugin will be tried.

Using a plain plugin
--------------------

If there is no oEmbed endpoint available or you want to create a plugin without an external call, you can derive from the
``Plugin`` class like so::

    from embeddify import Plugin

    class ExamplePlugin(Plugin):
       
        default = {
            'width' : 200,
            'height' : 300,
        }
        
        def __call__(self, parts, config = {}):
            if "example.org" in parts.netloc:
                return """<iframe src="something" width="%(width)s"></iframe>""" %config['width']
            return None

Again you get the results of ``urlparse.urlparse()`` passed into the plugin as well as a ``config`` dictionary. You then
have to test whether your plugin knows about this service and if you do, just return a string with the embed code.
If your plugin is not responsible or something else went wrong, simply return ``None``. Then the next plugin will be tried.

In order to accept configuration, simply create a ``default`` dictionary in the class. This will be copied to your config
and updated with plugin specific configuration and call by call configuration and then passed in as ``config`` parameter.
So you shouldn't have to do any modifications on it, just make sure you provide some default value.


License
=======

This package is released under the BSD license.


Author
======

embeddify is written by Christian 'mrtopf' Scholz, COM.lounge GmbH. 


Contributors
============

Florian Schulze (fschulze)


Source Code
===========

The source code can be found on `github <http://www.github.com/comlounge/embeddify>`_.



Changelog
=========

0.3.2 (2025-06-17)
------------------

- Support python 3.13 by using `html.escape` instead of deprecated `cgi.escape` [fschulze]

0.3.1 (2017-08-28)
------------------

- Fix for unicode in markup for Python 2.7 [fschulze]


0.3.0 (2017-07-31)
------------------

- Support autoplay setting and add a workaround in the YouTube plugin [fschulze]

- Allow sending of additional parameters via ``params`` keyword [fschulze]

- Don't let calling Embedder with keywords overwrite the plugin
  configuration [fschulze]

- The dictionary with raw OEmbed data can by accessed via the ``data``
  attribute of the result if it comes from an OEmbed plugin [fschulze]

- Python 3.x compatibility [fschulze]


0.2.0 (2016-11-21)
------------------

- support youtu.be links [fschulze]

- support facebook.com videos [fschulze]

- use https endpoints for all services [fschulze]

- changed flickr oembed to return a linked image instead of just an image. [mrtopf]
    
- added class `flickr-embed-img` to flickr image for better styling [mrtopf]
   
- split ``__call__()`` on plugins into two methods, ``do_request()`` for
  performing the actual request and ``__call__()`` will do the actual
  processing [mrtopf]


0.1.1 (2016-10-27)
------------------

- fix tests and packaging


0.1.0.2 (2014-03-30)
--------------------

- fixed tests


0.1.0.1 (2013-06-20)
--------------------

- initial release










