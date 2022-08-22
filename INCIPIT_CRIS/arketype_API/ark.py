import urllib.request
import base64
import os

class Ark:
    """
    A class that is used to make the calls to the ARKetype API

    Attributes
    ----------
    server : str
        String containing the url of the arketype api
    username : str
        String containing the username of the account in ARKetype managing the ARKs
    password : str
        String containing the password of the account in ARKetype managing the ARKs
    shoulder : str
        String containing the shoulder of the ARKs

    Methods
    -------
    mint(target, who, what, when)
        Creates a random ark based on the given parameters
    view(ark)
        Gets identifier metadata
    update(ark, target, who, what, when)
        Updates the metadata of the identifier
    create(ark, target, who, what, when)
        Creates a defined ark based on the given parameters
    """

    server = 'https://www.arketype.ch/'
    username = os.environ['username_ark']
    password = os.environ['password_ark']
    shoulder = os.environ['shoulder']

    def mint(self, target, who, what, when):
        """
        Creates a random ark based on the given parameters

        Parameters
        ----------
        target : str
            The url containing the element
        who : str
            The name of an entity (person, organization, or service) responsible for creating 
            the content or making it available
        what : str
            A name or other human-oriented identifier given to the resource
        when : str
            A point or period of time important in the lifecycle of the resource, 
            often when it was created, modified, or made available

        Returns
        -------
        str
            String containing the ARK minted

        Raises
        ------
        urlib.error.HTTPError
            If there is an error when doing the request
        Exception
            If there is an exception when doing the request
        """
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
        """
        Request the metadata of a given ARK

        Parameters
        ----------
        ark : str
            A string containing the ARK for which the function will request the metadata

        Returns
        -------
        str
            The metadata of the given ARK

        Raises
        ------
        urlib.error.HTTPError
            If there is an error when doing the request
        Exception
            If there is an exception when doing the request
        """
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
        """
        Updates the given ARK with the given parameters

        Parameters
        ----------
        ark : str
            A string that contain the ARK
        target : str
            The url containing the element
        who : str
            The name of an entity (person, organization, or service) responsible for creating 
            the content or making it available
        what : str
            A name or other human-oriented identifier given to the resource
        when : str
            A point or period of time important in the lifecycle of the resource, 
            often when it was created, modified, or made available

        Returns
        -------
        str
            String containing the ARK minted

        Raises
        ------
        urlib.error.HTTPError
            If there is an error when doing the request
        Exception
            If there is an exception when doing the request
        """
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
        """
        Creates an ARK based on the given parameters

        Parameters
        ----------
        ark : str
            A string that contain the ARK
        target : str
            The url containing the element
        who : str
            The name of an entity (person, organization, or service) responsible for creating 
            the content or making it available
        what : str
            A name or other human-oriented identifier given to the resource
        when : str
            A point or period of time important in the lifecycle of the resource, 
            often when it was created, modified, or made available

        Returns
        -------
        str
            String containing the ARK minted

        Raises
        ------
        urlib.error.HTTPError
            If there is an error when doing the request
        Exception
            If there is an exception when doing the request
        """
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
