def get_pdf(base_url, base_dir):
    #!/usr/bin/env python

    """
    Download all the pdfs linked on a given webpage
    Usage -
        python grab_pdfs.py url <path/to/directory>
            url is required
            path is optional. Path needs to be absolute
            will save in the current directory if no path is given
            will save in the current directory if given path does not exist
    Requires - requests >= 1.0.4
               beautifulsoup >= 4.0.0
    Download and install using
        pip install requests
        pip install beautifulsoup4
    """

    __author__ = 'elssar <elssar@altrawcode.com>'
    __license__ = 'MIT'
    __version__ = '1.0.0'

    from requests import get
    from urllib.parse import urljoin
    from os import path, getcwd
    from bs4 import BeautifulSoup as soup
    import sys
    import logging

    logging.basicConfig(filename=path.join(base_dir, 'downloads_log.log'), level=logging.INFO,
                        format='%(asctime)s %(message)s')

    # if __name__ == '__main__':
    #     # if len(argv) not in (2, 3):
    #     if len(sys.argv)!=2:
    #         print("This is the name of the script: ", sys.argv[0])
    #         print("Number of arguments: ", len(sys.argv))
    #         print("The arguments are: ", str(sys.argv))
    #         print('Error! Invalid arguments')
    #         print(__doc__)
    #         exit(-1)
    #     arg = ''
    #     url = sys.argv[1]
    #     if len(sys.argv) == 3:
    #         arg = sys.argv[2]
    #     base_dir = [getcwd(), arg][path.isdir(arg)]
    #     try:
    #         get_pdf(base_dir)
    #     except Exception as e:
    #         print(e)
    #         exit(-1)

    def get_page(base_url):
        req = get(base_url)
        if req.status_code == 200:
            return req.text
        logging.warning('http status_code: ' + req.status_code)
        raise Exception('Error {0}'.format(req.status_code))


    def get_all_links(html):
        bs = soup(html, 'html.parser')  # MISSING 'html.parser'
        links = bs.findAll('a')
        return links

    logging.info('------------------------------------------------------------------------------------------')
    logging.info('')
    logging.info('')
    logging.info('Starting')
    logging.info('base_url: ' + base_url)
    logging.info('base_dir: ' + base_dir)

    html = get_page(base_url)  #MISSING ARGUMENT
    links = get_all_links(html)
    if len(links) == 0:
        logging.warning('No links found on the webpage.')
        raise Exception('No links found on the webpage')

    n_pdfs = 0
    n_saved_pdfs = 0

    for link in links:
        current_link = link.get('href') #This line and the line below
        if current_link.endswith('pdf'):
            # if link['href'][-4:] == '.pdf':
            weblink = urljoin(base_url, link['href'])
            logging.info('pdf file found at ' + weblink)
            print('pdf file found:', weblink)

            n_pdfs += 1

            file_address = path.join(base_dir, str(current_link).split('/')[-1]) #It is not necessary to add .pdf to the end of the filename

            # print('base_dir',base_dir)
            # print('file_address',file_address)
            # print(path.exists(file_address))

            if path.exists(file_address) == False:
                content = get(weblink, stream=True)  #https://stackoverflow.com/a/44299915/2449724
                #stream=True means when function returns, only the response header is downloaded, response body is not.

                if content.status_code == 200 and content.headers['content-type'] == 'application/pdf': #status to status_code
                    print('File size(mb)', round(float(content.headers['Content-length']) / 1000000), 2, sep=',')
                    with open(file_address, 'wb') as pdf:
                        logging.info('Saving pdf to ' + file_address)
                        print('Saving pdf to', file_address)

                        pdf.write(content.content)

                        logging.info('COMPLETE')
                        print('COMPLETE')

                        n_saved_pdfs +=1
                        logging.info('Number of save pdfs is ' + str(n_saved_pdfs))
                        print()
                else:
                    logging.info('content.status_code: ' + str(content.status_code))
                    logging.info('''content.headers['content-type']:''' + content.headers['content-type'])
                    print('content.status_code:', content.status_code)
                    print('''content.headers['content-type']:''', content.headers['content-type'])
                    print()

            else:
                logging.info('Already saved.')
                print('Already saved')
                n_saved_pdfs += 1
                print()
        if n_pdfs == 0:
            logging.info('No pdfs found on the page.')
            raise Exception('No pdfs found on the page')

        logging.info("{0} pdfs found, {1} saved in {2}".format(n_pdfs, n_saved_pdfs, base_dir))
        print("{0} pdfs found, {1} saved in {2}".format(n_pdfs, n_saved_pdfs, base_dir))

base_url = 'https://www.ontariosheep.org/weekly-market-summaries'
base_dir = './' #example r'C:\User'

if base_dir or base_url:
    print('Please, assign values to base_url and base_dir.')

get_pdf(base_url,base_dir)
