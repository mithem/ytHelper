from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse as parse
from fileloghelper import Logger
from download import download_list
from utils import removeExtension, get_extension, get_filetype

logger = Logger("server.log", "ytHelperServer", True, True)
logger.header(True, True, "THE YT SERVER", 8)


class ytHelperHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        logger.debug("GET - " + self.path)
        parsed_url = parse.urlparse(self.path)
        if parsed_url.path == "/":
            content = open("index.html", "r").read()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-Length", len(content))
            self.end_headers()
            self.wfile.write(bytes(content, "utf-8"))
            return True
        elif parsed_url.path == "/get":
            token = parse.parse_qs(parsed_url.query).get("token", "")[0]
            with open("config.json", "r") as f:
                config = json.loads(f.read())
            urls = config["urls"]
            try:
                tokendict = urls[token]
            except KeyError:
                tokendict = {"filename": "notvalid.mp4"}
            if tokendict.get("filename") != "notvalid.mp4":
                with open("serverfiles/" + config["urls"].get(token).get("filename"), "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-type", "video/mp4")
                self.end_headers()
                self.wfile.write(content)
        else:
            content = "<html><body><h1>Page not found</h1></body></html>"
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-Length", len(content))
            self.end_headers()
            self.wfile.write(bytes(content, "utf-8"))

    def do_POST(self):
        logger.debug("POST - " + self.path, True)
        data: dict = json.loads(self.rfile.read(
            int(self.headers.get("Content-Length", 0))))
        logger.debug(data)
        response_code = 200
        response_msg = "Success"
        try:
            token: str = data["token"]
            url: str = data["url"]
        except KeyError:
            response_code = 406
            response_msg = "Invalid parameters. Expected token & url"
        with open("config.json", "r") as f:
            config = json.loads(f.read())
        config["urls"][token] = {
            "filename": "",
            "url": url
        }
        with open("config.json", "w") as f:
            f.write(json.dumps(config))
        self.send_response(101)
        self.end_headers()
        download(token, url, logger)
        self.send_response(200)
        self.send_header("Content-type", "video/mp4")
        self.end_headers()
        self.wfile.write(bytes(response_msg, "utf-8"))


def download(filename: str, url: str, logger: Logger):
    """filename as token with extension"""
    download_list([url], {"outtmpl": "serverfiles/" +
                          filename + ".mp4", "format": "mp4"}, logger)
    with open("config.json", "r") as f:
        config = json.loads(f.read())
    config["urls"][filename]["filename"] = filename + ".mp4"
    with open("config.json", "w") as f:
        f.write(json.dumps(config))


if __name__ == "__main__":
    server = HTTPServer(("", 8080), ytHelperHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
