"""

embeddify
=========

Library for converting links into embed codes

"""

import urlparse
import copy
import json
import requests


class Plugin(object):
    """base plugin to be used for converting one type of link into an embed"""

    default = {
        'width' : "560",
        'height' : "315"
    }


    def __init__(self, **kw):
        """initialize a plugin and do some base configuration. We at least give a width
        and height in 1 16:9 aspect ratio as the default"""

        self.config = copy.copy(self.default)
        self.config.update(kw)

    def configure(self, config):
        """configure a plugin from the embedder class"""
        self.config.update(config)

    def __call__(self, parts):
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

    def __call__(self, parts):
        """call the oembed endpoint and return the result"""
        if not self.test(parts): 
            return
        c = self.config
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
        config.update(kw)
        self.config = config

        # update the plugin specific configuration
        for plugin in plugins:
            plugin_name = plugin.__class__.__name__.lower()
            self.plugin_config[plugin_name] = copy.copy(config)
            self.plugin_config[plugin_name].update(plugin_config.get(plugin_name, {}))
            plugin.configure(self.plugin_config[plugin_name]) # configure the plugin


    def __call__(self, link):
        """parse the link and either return the link as is or an embed code in case we found a match"""
        
        parts = urlparse.urlparse(link)

        for plugin in self.plugins:
            res = plugin(parts)
            if res is not None:
                return res

        # if nothing matches simply return the link
        return link
            


if __name__ == "__main__":
    embedder = Embedder()
    print embedder("https://www.youtube.com/watch?v=2wii8hfNkzE")
    print embedder("http://de.slideshare.net/mrtopf/open-government-vortrag-aachen")
    print embedder("http://www.flickr.com/photos/mrtopf/7780673842/")
    print embedder("http://vimeo.com/68608567")

