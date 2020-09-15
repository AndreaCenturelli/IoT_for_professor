import cherrypy
import json
import os
from cherrypy.lib.static import serve_file
dir_path = os.path.dirname(os.path.realpath(__file__))
cr_path = os.path.join(dir_path, 'Plots')



class Root:
    @cherrypy.expose
    def Plots(self, name):
    	return serve_file(os.path.join(cr_path, '%s.png' % name),
                              content_type='image/png')
    @cherrypy.expose
    def GPS(self, name):
    	return serve_file(os.path.join(cr_path, '%s.html' % name),
                              content_type='text/html')

if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Set up site-wide config first so we get a log if errors occur.
    cherrypy.config.update({'environment': 'production',
                            'log.error_file': 'site.log',
                            'log.screen': True})
    cherrypy.config.update({'server.socket_host':'127.0.0.1'})
    cherrypy.config.update({'server.socket_port': 1350})
    cherrypy.quickstart(Root(), '/')
