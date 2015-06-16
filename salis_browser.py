"""python 3 split urllib2 into urllib.request and urllib.error
I name it like this so that code feels similar to 2.7"""
import urllib.request as urllib2
import http.cookiejar as cookielib
import urllib

class SalisBrowser(object):
    def __init__(self, login, password):
        """ Start up..."""
        self.login = login
        self.password = password

        self.cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(
        urllib2.HTTPRedirectHandler(),
        urllib2.HTTPHandler(),
        urllib2.HTTPSHandler(),
        urllib2.HTTPCookieProcessor(self.cj)
        )

        self.opener.addheaders = [
            ('User-agent', ('Mozilla/4.0 (compatible; MSIE 6.0; '
                           'Windows NT 5.2; .NET CLR 1.1.4322)'))
        ]

        #need twice. once to set cookies, once to log in...
        print(self.loginToSalis())
        print(self.loginToSalis())

    def loginToSalis():
        """Handle login. this should populate cookie jar"""
        login_data  = urllib.urlencode({
            'uname':self.login,
            'pwname':self.password
        })

if __name__ == '__main__':
    browser = SilasBrowser("hi","maybe")
