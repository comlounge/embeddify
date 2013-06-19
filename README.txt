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
        'slideshare': {'width' : 400},
    }
    embedder = Embedder(plugin_config = plugin_config)

The plugin specific configuration overwrites the generic configuration.

Chosing which plugins to use
----------------------------

If you don't want all the plugins to be active you can choose which ones you want to use by providing a list
of plugins to use like this::
   
    import embeddify
    plugins = [embeddify.YouTube(), embeddify.Vimeo()] # only video
    embedder = Embedder(plugins = plugins)
    

Creating your own plugins
=========================

In order to extend the functionality with additional services you can create your own plugins. Depending on
the service and whether it provides an `oEmbed endpoint <http://www.oembed.com/>`_ or not you can one of two base classes.










