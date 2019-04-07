from GrabzIt import GrabzItClient
from GrabzIt import GrabzItImageOptions

import http.cookiejar as cookielib
import imgkit
import re
import yaml

def load_yaml(fname):
    with open(fname, "r") as f:
        return yaml.safe_load(f)

# First approach at saving LWP cookies
def save_cookies_lwp(cookiejar, filename):
    lwp_cookiejar = cookielib.LWPCookieJar()
    for c in cookiejar:
        args = dict(vars(c).items())
        args['rest'] = args['_rest']
        del args['_rest']
        c = cookielib.Cookie(**args)
        lwp_cookiejar.set_cookie(c)
    lwp_cookiejar.save(filename, ignore_discard=True)

# First approach at loading LWP cookies
def load_cookies_from_lwp(filename):
    # lwp_cookiejar = cookielib.LWPCookieJar()
    # lwp_cookiejar.load(filename, ignore_discard=True)
    lwp_cookiejar = cookielib.MozillaCookieJar(filename)
    lwp_cookiejar.load()
    return lwp_cookiejar

# Using Grabzit propietary software but you can try with open source libsself.
# I played for a while with this but everything good about it is behind a paywall
def as_image(source, output):
    key = self.credentials['credentials']['grabzit_key']
    secret = self.credentials['credentials']['grabzit_secret']
    grabzIt = GrabzItClient.GrabzItClient(key, secret)
    options = GrabzItImageOptions.GrabzItImageOptions()
    options.browserHeight = -1
    options.width = -1
    options.height = -1
    options.format = 'png'
    options.quality = 100
    grabzIt.FileToImage(source, options)
    grabzIt.SaveTo(output)  # (!) synchonous call to Grabzit API

# Extract 1 field from the argument pattern and string
# A valid python regex is expected as pattern
def extract_one(str, pattern):
    match = re.search(pattern,str)
    if match:
        return match.group(1)
    return None

# Extract 2 fields from the argument pattern and string
def extract_two(str, pattern):
    match = re.search(pattern,str)
    if match:
        return match.group(1), match.group(2)
    return None, None

# Extract the current and max thread page range
def thread_pages_range(thread, next_page_patt):
    current, max = extract_two(thread, next_page_patt)
    if current == None or max == None:
        return 1,1
    return int(current), int(max)
