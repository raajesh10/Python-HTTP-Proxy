from html.parser import HTMLParser
from pathlib import Path
import socket
import _thread
import os
import os.path
import sys
import time
import datetime
access_right = 0o777
sys.argv
port = int ( sys.argv[1] )
cache_time_limit = int( sys.argv[2] )
host_name = socket.gethostname()
host = socket.gethostbyname( host_name )
print ('Current server location:' + host_name + ':' + host )
print(' HTTP proxy has started....................................................')
path01 = 'C:/Users/Admin/Desktop/PA/PA_3/Cache_folder'
http_echo = 'HTTP/1.0 200 Document Follows\r\nContent-Type:text/html\r\nContent-Length:'
header = '\r\n\r\n<html><h1></h1>\n</html>'
http_error = 'HTTP/1.0 500 Internal Server Error \r\nContent-Type:text/html\r\nContent-Length:42\r\n\r\n<html><h1>Error 500: Internal Server Error</h1>\n</html>'
http_block = 'HTTP/1.0 500 Internal Server Error \r\nContent-Type:text/html\r\nContent-Length:146\r\n\r\n<html><h1>Error 500: Internal Server Error</h1><p>Sorry........ Proxy restricts the requested content........  Sorry for inconvinience............</p>\n</html>'
http_timeout = 'HTTP/1.0 500 Internal Server Error \r\nContent-Type:text/html\r\nContent-Length:98\r\n\r\n<html><h1>Error 500: Internal Server Error</h1><p>Sorry........... Server takes too long to respond</p>\n</html>'
mover = '\r\n\r\n'
prefetch_request = 'Host: netsys.cs.colorado.edu\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\nAccept-Language: en-US,en;q=0.5\nAccept-Encoding: gzip, deflate\nReferer: http://netsys.cs.colorado.edu/\nConnection: keep-alive\nUpgrade-Insecure-Requests: 1'

class Parser(HTMLParser):
  # method to append the start tag to the list start_tags.
  def handle_starttag(self, tag, attrs):
    #global start_tags
    global start_tag_attribute
    if (tag == 'a'):
        start_tag_attribute.append(attrs)
        #start_tags.append(tag)

start_tag_attribute = []
parser = Parser()
def cache_sender( file_path , client_sock , addr ):
    print('\n\n\n\n\n Inside Cache_sender ......................................\n\n')
    try:
        cache_file = open( file_path , 'rb' )
        output_cache_data = cache_file.read(1024)
        while( output_cache_data ):
            if( client_sock.send( output_cache_data )):
                output_cache_data = cache_file.read(1024)
        cache_file.close()
        return('1')
    except:
        print( '\n\nUnable to open file in cache.....................')
        return('0')

def cache_store( data , file_path ):
    print('\n\n\n\n\n\n Inside Cache_store ......................................\n\n')
    try:
        cache_file = open( file_path , 'wb' )
        cache_file.write( data )
        cache_file.close()
        print ( '\n\nData successfully cached..................')
        return
    except:
        print('\n\nUnable to cache the data..............')
        return
      
def cache_status_check( file_path ):
    print('\n\n\n\n\n Inside Cache_ time_checker..............................................\n\n')
    present_time = int( time.time())
    last_modified_time = int( os.stat( file_path ).st_mtime )
    Diff = int( present_time - last_modified_time )
    if (Diff < cache_time_limit ):
        print('\n\n\n Cached data still active................................')
        return('1')
    else:
        print('\n\n\n Cached data expired.....................................')
        return('0')
    
def crawler( x1 , data_link , host ):
    server_host = host
    server_port = 80
    prefetch_proxy_sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    prefetch_http_request = str( 'GET' + ' ' + data_link + ' ' + 'HTTP/1.0' + '\n' + prefetch_request )
    print('\n\n Entering crawler...........\n\n')
    print('\n\nComplete prefetch http request.......')
    print( prefetch_http_request + '\n\n')
    try:
        prefetch_proxy_sock.connect( (server_host , server_port) )
        prefetch_proxy_sock.send( prefetch_http_request.encode('utf-8'))
        try:
            http_prefetch_response = prefetch_proxy_sock.recv(4000000)
            print('\n\nPrefetching..........' + data_link + '\n\n')
            prefetch_proxy_sock.close()
            prefetch_file = str( path01 + '/' + host + '/' + x1 )
            prefetch_file_path = Path( prefetch_file )
            x2 = x1.split('/')
            n2 = int (len(x2) - 1)
            x3 = str( '/' + x2[n2] )
            x4 = x1.replace( x3 , '')
            prefetch_dir = str( path01 + '/' + host + '/' + x4 )
            prefetch_dir_path = Path( prefetch_dir )
            if (os.path.isdir( prefetch_dir_path )):
                print('\n\nDirectory already exists for the prefetched data.........')
                cache_store( http_prefetch_response , prefetch_file_path )
                return('1')
            else:
                print('\n\nDirectory for prefetched data, absent........\nCreating required directories.........')
                try:
                    os.makedirs( prefetch_dir_path , access_right )
                    print('\n\n Directory for the prefetched data created successfully..........')
                    cache_store( http_prefetch_response , prefetch_file_path )
                    return('1')
                except:
                    print('\n\n Sorry, Unable to create the required directory for the prefetched data')
                    return('0')
        except:
            print('\n\n Prefetching failed at level 02 returning to spider from crawler...........\n\n')
            return('0')
    
    except:
        print('\n\n Prefetching failed at level 01 returning to spider from crawler...........\n\n')
        return('0')
    
def spider( request , host , client_sock , addr ):
    server_host = host
    server_port = 80
    proxy_sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    check01 = request.split()
    print('\n\nEntering spider.......................\n\n')
    #proxy_sock.settimeout(100)
    #proxy_sock.connect( (server_host , server_port) )
    #proxy_sock.send( request.encode('utf-8'))
    try:
        proxy_sock.connect( (server_host , server_port) )
        proxy_sock.send( request.encode('utf-8'))
        try:
            http_response = proxy_sock.recv(4000000)
            print('\n\nReceiving http_response from the server..............................\n\n')
            #http_response_data = http_response
            client_sock.send(http_response)
            proxy_sock.close()
            http_response_data = http_response.decode()
            print('\n\n $$$$$ Storing the data to cache.............$$$$$\n')
            url = check01[1]
            y = url.replace('http:/' , '' )
            a = y.split('/')
            n = len(a) - 1
            if (a[2] == '') :
                print ( '\n\nThe requested file is index.html........\n\n' )
                print('\n Caching index.html.............\n\n')
                index_file = str ( path01 + y + 'index.html' )
                index_file_path = Path ( index_file )
                index_dir = str ( path01 + '/' + host )
                index_dir_path = Path ( index_dir )
                if ( os.path.isdir( index_dir_path )):
                    print( '\n\n Directory already exists..............................')
                    cache_store( http_response , index_file_path )
                    
                else:
                    print( '\n\n Directory not found.......................... Creating new directory......................')
                    try:
                        os.mkdir( index_dir_path , access_right )
                        print('\n\n Directory created successfully..................')
                        cache_store( http_response , index_file_path )
                        
                    except:
                        print('\n\nSorry Unable to create the directory.................')
                    
                if ( host == 'netsys.cs.colorado.edu' ):
                    start_tag_attribute[ : ] = []
                    parser.feed( http_response_data )
                    n1 = len( start_tag_attribute )
                    for i in range ( 0,n1 ):
                        a1 = start_tag_attribute[i]
                        b1 = a1[0]
                        c1 = list(b1)
                        if len(c1) < 3:
                            d1 = c1[1]
                            if ('.gif' in d1) or ('.jpg' in d1) or ('.png' in d1) or ('.txt' in d1) :
                                if ('http' not in d1) and ('html' not in d1 ):
                                    e1 = str( 'http://' + host + '/' + d1)
                                    f1 = crawler( d1 , e1 , host )
                                    if f1 == '0':
                                        print('/n/n Prefetching failed............')
                                    else:
                                        print('/n/n Prefetching successful..........')
                    print('\n\n Done with prefetching.............')
                    #return
                else:
                    print('Host unknown.............Prefetching aborted............')
                    #return
            else:
                print( '\n\nThe requested file is not an index file................\n\n')
                print('\n Caching the file.....\n\n')
                cache_file = str ( path01 + y )
                cache_file_path = Path ( cache_file )
                cut = '/' + a[n]
                cache_dir = str( path01 + y.replace( cut , '' ) )
                cache_dir_path = Path ( cache_dir )
                if ( os.path.isdir( cache_dir_path )):
                    print( '\n\n Directory already exists...............................')
                    cache_store( http_response , cache_file_path )
                    #return
                else:
                    print( '\n\n Directory not found........................... Creating new directory........................')
                    try:
                        os.makedirs( cache_dir_path , access_right )
                        print('\n\n Directory created successfully...................')
                        cache_store( http_response , cache_file_path )
                        #return
                    except:
                        print('\n\n Sorry Unable to create the directory.......................')
                        #return

            #client_sock.send(http_response)
            print('\n\nSending http_response to the client browser..........\n\n')
            print('\n returning to the handler............\n\n')
            return
            

        except:
            print('\n\nTimeout error.............................\n\n')
            #client_sock.send(http_timeout.encode('utf-8'))
            proxy_sock.close()
            return
    except:
        print('\n\n\nError: Unable to connect with the host..................................\n\n\n')
        client_sock.send(http_error.encode('utf-8'))
        return
        
        
        
    
def handler( client_sock , addr ):
  
    while True:
        try:
            http_request = client_sock.recv(1024)
            if not http_request: break
            request = http_request.decode('utf-8')
            check01 = request.split()
            if (check01[0] == 'GET'):
                print( ' \n\n\n\n\nProper GET method.................')
                print('\n \n Complete HTTP request from the client............................')
                print( request )
                host = check01[4]
                url = check01[1]
                print('\n\n\n\n\n The Host is : \n' + host + '\n\n\n\n\n')
                black_list_path = 'C:\\Users\\Admin\\Desktop\\PA\\PA_3\\Black_list.txt'
                black_list_file = open ( black_list_path , 'r')
                black_list_data = black_list_file.read()
                black_list_file.close()
                print('The restricted webhosts are:')
                print('\n\n' + black_list_data )
                if host not in black_list_data:
                    print('\n \n Requested site is not blocked by proxy.............')
                    print( ' The requested server host from client ..............................')
                    print( '=>' + host )
                    a = url.replace('http:/' , '' )
                    b = a.split( '/' )
                    if (b[2] == ''):
                        print('\n\n The requested file is index.html')
                        c = str ( path01 + a + 'index.html' )
                        d = Path ( c )
                        if ( os.path.isfile( d ) ):
                            print('\n\n Requested index.html file already in cache..........')
                            print('\n\n Checking expiration status of the existing cache...........')
                            expired01 = cache_status_check( d )
                            if (expired01 == '0'):
                                print('\n\n Cache expired, fetching fresh data.................')
                                spider( request , host , client_sock , addr )
                            else:
                                val = cache_sender( d , client_sock , addr )
                                if ( val == '0' ):
                                    print( '\n\n Some problem in cached file....................Moving to spider..........\n')
                                    spider( request , host , client_sock , addr )
                                else:
                                    print('\n ................................Caching works successfully.........................')
                        else:
                            print('\n\n Requested index.html file not cached.........')
                            spider( request , host , client_sock , addr )
                    else:
                        print('\n\n The requested file is not index.html')
                        e = str ( path01 + a )
                        f = Path ( e )
                        if ( os.path.isfile( f ) ):
                            print('\n\n Requested file already in cache..........')
                            print('\n\n Checking the expiration status of the requested file...............')
                            expired02 = cache_status_check( f )
                            if ( expired02 == '0' ):
                                print('Cache expired, fetching fresh data........................')
                                spider ( request , host , client_sock , addr )
                            else:
                                val = cache_sender( f , client_sock , addr )
                                if ( val == '0' ):
                                    print( '\n\n Some problem in cached file.........................Moving to spider............\n')
                                    spider( request , host , client_sock , addr )
                                else:
                                    print( '\n ..........................Caching works successfully...........................')
                        else:
                            print('\n\n Requested file not yet cached...............')
                            spider( request , host , client_sock , addr )
                elif ('pokemon' in host):
                    print('\n Sorry all http sites related to POKEMON were blocked by the proxy............')
                    client_sock.send(http_block.encode('utf-8'))
                else:
                    print('\n Requested site is specified in the black list...................')
                    client_sock.send(http_block.encode('utf-8'))

            else:
                print( ' Invalid method from the client......................')
                #print(' \n \n Sending the error message to the client.....................................')
                client_sock.send(http_error.encode('utf-8'))

        except:
            pass
          
            
        
        




server_sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
server_sock.setsockopt(socket.SOL_SOCKET , socket.SO_REUSEADDR , 1)
server_sock.bind(( host , port ))
server_sock.listen(10)
while True:
    ( client_sock , addr ) = server_sock.accept()
    _thread.start_new_thread(handler , ( client_sock , addr ))
