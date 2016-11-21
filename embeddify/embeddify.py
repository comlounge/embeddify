"""

embeddify
=========

Library for converting links into embed codes

"""

import urlparse
import cgi
import urllib
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

    def do_request(self, parts, config):
        """run the request and return the data"""
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
        return json.loads(res.text)

    def __call__(self, parts, config = {}):
        """call the oembed endpoint and return the result"""
        data = self.do_request(parts, config)
        if data is None:
            return None
        otype = data.get("type", None)
        if otype == "video":
            return data['html']
        elif otype == "rich":
            return data['html']
        elif otype == "photo":
            # for flickr (or maybe in general) we also check if html is provided and use this.
            # this make sure we link back properly to flickr and use the correct image
            if "html" in data:
                return data['html']
            return """<img src="%(url)s" width="%(width)s" height="%(height)s">""" %data
        return None


class YouTube(OEmbedPlugin):
    """converts youtube links into embeds
    """

    api_url = "https://www.youtube.com/oembed"

    def test(self, parts):
        """test if the plugin is able to convert that link"""
        return "youtube.com" in parts.netloc or "youtu.be" in parts.netloc

class Flickr(OEmbedPlugin):
    """converts flickr links into embeds
    """

    api_url = "https://www.flickr.com/services/oembed"

    def test(self, parts):
        """test if the plugin is able to convert that link"""
        return "flickr.com" in parts.netloc

    def __call__(self, parts, config = {}):
        """special case for flickr so that we can avoid the iframe which html produces"""

        data = self.do_request(parts, config)
        if data is None:
            return None
        otype = data.get("type", None)
        if otype != "photo":
            return None # no photo, nothing to do here

        new_data = {
            'url' : data['web_page'],
            'src' : data['url'],
            'title' : cgi.escape(data['title']),
            'width' : data['width'],
            'height' : data['height'],
        }

        return """<a target="flickr" href="%(url)s"><img src="%(src)s" class="flickr-embed-img" alt="%(title)s" width="%(width)s" height="%(height)s"></a>""" %new_data

class Vimeo(OEmbedPlugin):
    """converts vimeo links into embeds
    """

    api_url = "https://vimeo.com/api/oembed.json"

    def test(self, parts):
        """test if the plugin is able to convert that link"""
        return "vimeo.com" in parts.netloc

class Slideshare(OEmbedPlugin):
    """converts slideshare links into embeds
    """

    api_url = "https://de.slideshare.net/api/oembed/2"

    def test(self, parts):
        """test if the plugin is able to convert that link"""
        return "slideshare.net" in parts.netloc or "slideshare.com" in parts.netloc


class FacebookVideos(OEmbedPlugin):
    """converts facebook video links into embeds
    """

    api_url = "https://www.facebook.com/plugins/video/oembed.json/"

    def test(self, parts):
        """test if the plugin is able to convert that link"""
        if "facebook.com" in parts.netloc:
            path_parts = parts.path.split('/')
            if len(path_parts) > 2 and path_parts[2] == 'videos':
                return True
            if len(path_parts) > 1 and path_parts[1] == 'video.php':
                return True
        return False


STANDARD_PLUGINS = [YouTube(), Slideshare(), Flickr(), Vimeo(), FacebookVideos()]


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

        :param url: the url to get the embed code for
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
            
