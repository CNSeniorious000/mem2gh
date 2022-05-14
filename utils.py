from functools import cached_property
from cachetools.func import ttl_cache
from loguru import logger


class Space:
    @cached_property
    def config(self):
        from yaml import load, CLoader
        return load(open("config.yaml"), CLoader)

    # noinspection PyPep8Naming
    @cached_property
    def q(self):
        from qiniu import Auth
        AK = self.config["access_key"]
        SK = self.config["secret_key"]
        return Auth(AK, SK)

    @ttl_cache(ttl=3333)
    def get_upload_token(self, key):
        token = self.q.upload_token(self.config["bucket_name"], key)
        logger.success(f"upload token {token} generated.")
        return token

    def upload(self, key, path):
        from qiniu import put_file, etag
        from time import perf_counter
        logger.debug(f"started uploading {path} to {key}")
        t = perf_counter()
        ret, info = put_file(self.get_upload_token(key), key, path, version="v2")
        logger.info(f"uploading finished in {perf_counter() - t:.1f}s")
        assert ret["key"] == key
        assert ret["hash"] == etag(path)
        return info

    @ttl_cache(ttl=3333)
    def get_download_url(self, key):
        url = self.q.private_download_url(f"{self.config['bucket_domain']}/{key}")
        logger.success(f"download url {url} generated.")
        return url

    @ttl_cache(ttl=3333)
    def download(self, key):
        from requests import get
        r = get(self.get_download_url(key))
        r.raise_for_status()
        return r
