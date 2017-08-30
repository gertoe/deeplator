import requests

from .jsonrpc import JSONRPCBuilder

POST_URL = "https://www.deepl.com/jsonrpc"
HEADERS = {"content-type": "application/json"}
VALID_LANGS = ["EN", "DE", "FR", "ES", "IT", "NL", "PL"]


class Translator():
    def __init__(self, src_lang, dst_lang):
        self.src_lang = src_lang.upper()
        self.dst_lang = dst_lang.upper()

        if self.src_lang not in VALID_LANGS:
            raise ValueError("Input language not supported.")
        if self.dst_lang not in VALID_LANGS:
            raise ValueError("Output language not supported.")

    def split_into_sentences(self, text):
        method = "LMT_split_into_sentences"
        params = {
            "texts": [text.strip()],
            "lang": {
                "lang_user_selected": self.src_lang
            }
        }
        rpc = JSONRPCBuilder(method, params)
        resp = requests.post(POST_URL, data=rpc.dumps(), headers=HEADERS)
        return resp.json()["result"]["splitted_texts"][0]

    def translate_sentences(self, sentences):
        jobs = [{"kind": "default", "raw_en_sentence": s} for s in sentences]
        method = "LMT_handle_jobs"
        params = {
            "jobs": jobs,
            "lang": {
                "source_lang": self.src_lang,
                "target_lang": self.dst_lang
            }
        }
        rpc = JSONRPCBuilder(method, params)
        resp = requests.post(POST_URL, data=rpc.dumps(), headers=HEADERS)
        translations = resp.json()["result"]["translations"]
        extract = lambda obj: obj["beams"][0]["postprocessed_sentence"]
        return [extract(obj) for obj in translations]