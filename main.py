import re

from bs4 import BeautifulSoup
from dataclasses import dataclass
from urllib import request, error, parse

@dataclass
class WebAnalyzer:
    root: str
    max_depth: int

    def start(self):
        if type(self.max_depth) == str:
            self.max_depth = int(self.max_depth)
        print("*** Fetching external links for " + self.root)
        page1, page_title = self.get_page(self.root)
        if page_title is None:
            return "Forbidden"
        page_title = re.sub("[!@#$']", '', page_title)
        external = self.get_external(page1, self.root)
        crawled = {}
        crawldepth = {}
        crawled[page_title]={'parent':'root'}
        num_of = len(external)
        print(f" *** {num_of} external links found on root")
        for check in external:
            if check != "":
                domain = self.get_domain(check)
            else:
                continue

            filter_domain = [domain]
            #set domain and depth
            tocrawl = [[check,1]]

            while tocrawl: 
                crawl_ele = tocrawl.pop()
                link = crawl_ele[0]
                depth = crawl_ele[1]
                
                if link not in crawled.keys():
                    if link is not None and link[:1] != '#' and link[:1] != '/' and \
                        link[:1] != '?' and link[:2] != '//':
                        print("*** Fetching data from " + link)
                    content, title = self.get_page(link)

                    if title == type(str):
                        title = re.sub("[!@#$']", '', title)
                    
                    if content == None:
                        continue
                    else:
                        crawldepth[depth]=title
                    host = self.get_domain(link)
                    
                    if depth < self.max_depth and host in filter_domain :

                        outlinks = self.get_all_links(content, link)
                        num_of_outlinks = len(outlinks)
                        print(f" *** {num_of_outlinks} link(s) found on {link}")
                    
                        self.add_to_tocrawl(crawled.keys(),tocrawl, outlinks, depth+1)
                    
                    if depth == 1:
                        crawled[title]={'parent':page_title}
                    else:
                        crawled[title]={'parent':crawldepth[depth-1]}

        return crawled
    
    def add_to_tocrawl(self, crawled, tocrawl, newlinks, depth):
        for link in newlinks:
            if link not in tocrawl and link not in crawled:
                tocrawl.append([link,depth])
    
    def is_external(self, root, host):
        if len(host) > 0:
            if host[0] == '/' or host[0] == '#' or host[0] == '?':
                return False

        host = parse.urlparse(host).hostname
        hostname = parse.urlparse(root).hostname
        if host == None:
            return False
        return host != hostname and host.find(hostname) == -1

    def get_external(self, soup, url):
        return [l.get('href') for l in soup.findAll('a') if self.is_external(url, l.get('href'))]

    def get_domain(self, url):
        
        hostname = parse.urlparse(url).hostname
        
        if len(re.findall( r'[0-9]+(?:\.[0-9]+){3}', hostname)) > 0:
            return hostname
        elif len(hostname.split('.')) == 0:
            hostname
        elif hostname.find('www.') != -1:
            return hostname.split('.')[0]
        else:
            return hostname.split('.')[1]

    def get_page(self, url):
        try:
            response = request.urlopen(url)
            soup = BeautifulSoup(response, features="html.parser")
            try:
                title_string = soup.title.string
            except Exception as e:
                title_string = "No Name"
            return soup, title_string
        except error.HTTPError as e:
            print(e)
            return None, None
        except error.URLError as e:
            print(e)
            return None, None
        except Exception as e:
            print(e)
            return None, None

    def get_all_links(self, page, parent):
        return [l.get('href') for l in page.findAll('a') ]


# print(analyse_web("https://www.cnn.com", 1))

wa = WebAnalyzer("https://www.cnn.com", 1)
print(wa.start())