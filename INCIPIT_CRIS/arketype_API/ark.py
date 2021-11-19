import urllib.request
import base64
import os

class Ark:

    server = 'https://www.arketype.ch/'
    username = os.environ['username_ark']
    password = os.environ['password_ark']
    shoulder = os.environ['shoulder']

    def mint(self, target, who, what, when):
        print('{}, {}, {}, {}'.format(target, who, what, when))
        r = urllib.request.Request("{}shoulder/{}".format(self.server, self.shoulder))
        r.get_method = lambda: 'POST'
    
        s = '_target: {}\nerc.who: {}\nerc.what: {}\nerc.when: {}'.format(target, who, what, when).encode("UTF-8")
        r.data = s
        r.add_header('Content-Type', 'text/plain; charset=UTF-8')
        r.add_header('Content-Length', str(len(s)))

        r.add_header('Authorization', 'Basic ' + base64.b64encode((self.username + ':' + self.password).encode('utf-8')).decode('utf-8'))

        c = None
        try:
            c = urllib.request.urlopen(r)
            s = c.read().decode('UTF-8')
            assert s.startswith('success:'), s
            return s[8:].split()[0]
        except urllib.error.HTTPError as e:
            raise urllib.error.HTTPError()
            '''if e.fp != None:
                s = e.fp.read().decode('UTF-8')
                if not s.startswith('error:'): s = 'error: ' + s
                return (id, s)
            else:
                return (id, 'error: %d %s' % (e.code, e.msg))'''
        except Exception as e:
            raise Exception()
            #return (id, 'error: ' + str(e))
        finally:
            if c != None: c.close()

    
    def view(self, ark):
        r = urllib.request.Request('{}id/{}'.format(self.server, ark))
        r.get_method = lambda: 'GET'

        c = None
        try:
            c = urllib.request.urlopen(r)
            s = c.read().decode('UTF-8')
            assert s.startswith('success:'), s
            return s
        except urllib.error.HTTPError as e:
            raise urllib.error.HTTPError
            '''if e.fp != None:
                s = e.fp.read().decode('UTF-8')
                if not s.startswith('error:'): s = 'error: ' + s
                return (id, s)
            else:
                return (id, 'error: %d %s' % (e.code, e.msg))'''
        except Exception as e:
            raise Exception()
            #return (id, 'error: ' + str(e))
        finally:
            if c != None: c.close()


    def update(self, ark, target, who, what, when):
        r = urllib.request.Request("{}id/{}".format(self.server, ark))
        r.get_method = lambda: 'POST'
    
        s = '_target: {}\nerc.who: {}\nerc.what: {}\nerc.when: {}'.format(target, who, what, when).encode("UTF-8")
        r.data = s
        r.add_header('Content-Type', 'text/plain; charset=UTF-8')
        r.add_header('Content-Length', str(len(s)))

        r.add_header('Authorization', 'Basic ' + base64.b64encode((self.username + ':' + self.password).encode('utf-8')).decode('utf-8'))

        c = None
        try:
            c = urllib.request.urlopen(r)
            s = c.read().decode('UTF-8')
            assert s.startswith('success:'), s
            return s[8:].split()[0]
        except urllib.error.HTTPError as e:
            raise urllib.error.HTTPError()
            '''if e.fp != None:
                s = e.fp.read().decode('UTF-8')
                if not s.startswith('error:'): s = 'error: ' + s
                return (id, s)
            else:
                return (id, 'error: %d %s' % (e.code, e.msg))'''
        except Exception as e:
            raise Exception()
            #return (id, 'error: ' + str(e))
        finally:
            if c != None: c.close()


    def create(self, ark, target, who, what, when):
        r = urllib.request.Request("{}id/{}".format(self.server, ark))
        r.get_method = lambda: 'PUT'
    
        s = '_target: {}\nerc.who: {}\nerc.what: {}\nerc.when: {}'.format(target, who, what, when).encode("UTF-8")
        r.data = s
        r.add_header('Content-Type', 'text/plain; charset=UTF-8')
        r.add_header('Content-Length', str(len(s)))

        r.add_header('Authorization', 'Basic ' + base64.b64encode((self.username + ':' + self.password).encode('utf-8')).decode('utf-8'))

        c = None
        try:
            c = urllib.request.urlopen(r)
            s = c.read().decode('UTF-8')
            assert s.startswith('success:'), s
            return s[8:].split()[0]
        except urllib.error.HTTPError as e:
            raise urllib.error.HTTPError()
            '''if e.fp != None:
                s = e.fp.read().decode('UTF-8')
                if not s.startswith('error:'): s = 'error: ' + s
                return (id, s)
            else:
                return (id, 'error: %d %s' % (e.code, e.msg))'''
        except Exception as e:
            raise Exception()
            #return (id, 'error: ' + str(e))
        finally:
            if c != None: c.close()
