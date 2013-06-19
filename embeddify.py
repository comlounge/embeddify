"""

embeddify
=========

Library for converting links into embed codes

"""

import urlparse
import copy
import json
import requests

__all__ = ['Plugin', 'OEmbedPlugin', 'YouTube', 'Vimeo', 'Slideshare', 'Flickr', 'Embedder']

class Plugin(object):
    """base plugin to be used for converting one type of link into an embed"""

    default = {
        'width' : "560",
        'height' : "315"
    }

    def get_config(self, config):
        """prepares the configuration on a per call basis by combining the default
        with the generic config and the plugin specific one (the latter two coming
        from the ``Embedder`` class.
        """
        c = copy.copy(self.default)
        c.update(config)
        return c

    def __call__(self, parts, config = {}):
        """this method needs to be implemented by a plugin author and check the url parts
        for a match. If a match was detected, return the embed as string, if not return None
        so the next plugin will try to match
        """
        return None

class OEmbedPlugin(Plugin):
    """base class for all oembed enabled services"""

    api_url = ""

    def test(self, parts):
        """test if the plugin is able to convert that link"""
        return False

    def __call__(self, parts, config = {}):
        """call the oembed endpoint and return the result"""
        c = self.get_config(config)
        if not self.test(parts): 
            return
        params = {
            "maxwidth"  : c['width'],
            "maxheight" : c['height'],
            "format"    : 'json',
            "url"       : urlparse.urlunparse(parts),
        }
        res = requests.get(self.api_url, params = params)
        if res.status_code != 200:
            return None
        data = json.loads(res.text)
        otype = data.get("type", None)
        if otype == "video":
            return data['html']
        elif otype == "rich":
            return data['html']
        elif otype == "photo":
            return """<img src="%(url)s" width="%(width)s" height="%(height)s">""" %data
        return None


class YouTube(OEmbedPlugin):
    """converts youtube links into embeds
    """

    api_url = "http://www.youtube.com/oembed"

    def test(self, parts):
        """test if the plugin is able to convert that link"""
        return "youtube.com" in parts.netloc

class Flickr(OEmbedPlugin):
    """converts flickr links into embeds
    """

    api_url = "http://www.flickr.com/services/oembed"

    def test(self, parts):
        """test if the plugin is able to convert that link"""
        return "flickr.com" in parts.netloc

class Vimeo(OEmbedPlugin):
    """converts vimeo links into embeds
    """

    api_url = "http://vimeo.com/api/oembed.json"

    def test(self, parts):
        """test if the plugin is able to convert that link"""
        return "vimeo.com" in parts.netloc

class Slideshare(OEmbedPlugin):
    """converts slideshare links into embeds
    """

    api_url = "http://de.slideshare.net/api/oembed/2"

    def test(self, parts):
        """test if the plugin is able to convert that link"""
        return "slideshare.net" in parts.netloc or "slideshare.com" in parts.netloc


STANDARD_PLUGINS = [YouTube(), Slideshare(), Flickr(), Vimeo()]

class Embedder(object):
    """converts media links into embeds"""

    def __init__(self, plugins = STANDARD_PLUGINS, plugin_config = {}, config = {}, **kw):
        """initialize the Embedder class with a list of plugins to be used and optional configuration

        :param plugins: list of plugins to be used by the embedding mechanism
        :param plugin_config: a dictionary containing configuration on a per plugin basis. You need to
            give the lowercase name of the plugin as key and a dictionary containing configuration such as 
            ``width`` as the value.
        :param config: generic configuration to be used by all plugins. Will be overriden by the plugin
            specific configuration
        :param **kw: keyword arguments being added to the ``config`` dictionary, eventually overriding values.
        """

        self.plugins = plugins
        self.plugin_config = {}
        config = copy.copy(config)
        config.update(kw)
        self.config = config

        # update the plugin specific configuration
        for plugin in plugins:
            plugin_name = plugin.__class__.__name__.lower()
            self.plugin_config[plugin_name] = copy.copy(config)
            self.plugin_config[plugin_name].update(plugin_config.get(plugin_name, {}))


    def __call__(self, url, **kw):
        """parse the link and either return the link as is or an embed code in case we found a match

        :param link: the url to get the embed code for
        :param **kw: optional keyword arguments overwriting configuration on a by call basis
        """
        
        parts = urlparse.urlparse(url)

        for plugin in self.plugins:
            name = plugin.__class__.__name__.lower()
            config = self.plugin_config[name]
            config.update(kw)
            res = plugin(parts, config = config)
            if res is not None:
                return res

        # if nothing matches simply return the link
        return url
            
