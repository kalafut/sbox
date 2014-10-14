import crypto
import py
import requests

class Net:
    def __init__(self, server_url):
        self.server_url = server_url

    def get(self, name):
        ctr = 7
        response = requests.get("{url}/object/{name}?ctr={ctr}&auth={auth}".format(url=self.server_url, name=name.basename, ctr=ctr, auth=crypto.calc_auth("key", ctr)), proxies = {'http':''})

        if not response.ok:
            return
            # Something went wrong

        with name.open(mode="wb", ensure=True) as handle:
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)
