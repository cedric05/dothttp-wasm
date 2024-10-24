from dothttp.models.computed import Config
from dothttp.parse import HttpDefBase
import json
import base64

class content_override(HttpDefBase):
    def __init__(self, config: Config, **kwargs):
        self.extra_kwargs = kwargs
        super().__init__(config)

    def load_content(self):
        self.original_content = self.content = self.extra_kwargs['content']

    def load_properties_n_headers(self):
        self.property_util.add_env_property_from_dict(env=self.extra_kwargs.get("env", {}))

    def load_command_line_props(self):
        for key, value in self.extra_kwargs.get("properties", {}).items():
            self.property_util.add_command_property(key, value)

def main(content, target):
    # content = base64.b64decode(content).decode('utf-8')
    out = content_override(
        Config(target=target, no_cookie=True, property_file=None, experimental=False, format=False,
            stdout=False, debug=False, info=False, curl=False, env=[], file="", properties=[]),
        env={},
        content=content,
    )
    out.load()
    out.load_def()
    print(out.httpdef)
    headers = {}
    for header in out.httpdef.headers:
        headers[header] = out.httpdef.headers[header]
    out.httpdef.headers = headers
    return out.httpdef
def getTargets(content):
    content = base64.b64decode(content).decode('utf-8')
    print(content)
    out = content_override(
        Config(target="1", no_cookie=True, property_file=None, experimental=False, format=False,
            stdout=False, debug=False, info=False, curl=False, env=[], file="", properties=[]),
        env={},
        content=content,
    )
    out.load_model()
    all_names = []
    all_urls = []
    for index, http in enumerate(out.model.allhttps):
        if http.namewrap:
            name = http.namewrap.name if http.namewrap else str(index)
            start = http.namewrap._tx_position
            end = http._tx_position_end
        else:
            start = http.urlwrap._tx_position
            end = http._tx_position_end
            name = str(index + 1)
        name = {
            'name': name,
            'method': http.urlwrap.method,
            'start': start,
            'end': end
        }
        url = {
            'url': http.urlwrap.url,
            'method': http.urlwrap.method or 'GET',
            'start': http.urlwrap._tx_position,
            'end': http.urlwrap._tx_position_end,
        }
        all_names.append(name)
        all_urls.append(url)
    data = {"all_urls": all_urls, "all_names": all_names }
    return json.dumps(data)
globals()['main']=  main
globals()['targets'] = getTargets

main('GET "https://httpbin.org/get"',0)