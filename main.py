import re

from bs4 import BeautifulSoup
from dataclasses import dataclass
from urllib import request, error, parse


@dataclass
class DeepWebAnalyzer:
    root: str
    max_depth: int

    def start(self):
        if type(self.max_depth) is str:
            self.max_depth = int(self.max_depth)
        print("*** Fetching external links for " + self.root)
        page1, page_title = self._get_page(self.root)
        if page_title is None:
            return "Forbidden"
        page_title = re.sub("[!@#$']", '', page_title)
        external_links = self._get_external(page1, self.root)
        crawled = {}
        crawldepth = {}
        crawled[page_title] = {'parent': 'root'}
        num_of = len(external_links)
        print(f" *** {num_of} external links found on root")
        for ext_link in external_links:
            if ext_link != "":
                domain = self._get_domain(ext_link)
            else:
                continue

            filter_domain = [domain]
            tocrawl = [[ext_link, 1]]  # set domain and depth

            while tocrawl:
                crawl_element = tocrawl.pop()
                link = crawl_element[0]
                depth = crawl_element[1]

                if link not in crawled.keys():
                    if link is not None and link[:1] != '#' and \
                       link[:1] != '/' and link[:1] != '?' and \
                       link[:2] != '//':
                        print("*** Fetching data from " + link)
                    content, title = self._get_page(link)

                    if title is type(str):
                        title = re.sub("[!@#$']", '', title)

                    if content is None:
                        continue
                    else:
                        crawldepth[depth] = title
                    host = self._get_domain(link)

                    if depth < self.max_depth and host in filter_domain:

                        outlinks = self._get_all_links(content, link)
                        num_of_outlinks = len(outlinks)
                        print(f"*** {num_of_outlinks} link(s) found on {link}")

                        self._add_to_tocrawl(
                            crawled.keys(), tocrawl,
                            outlinks, depth + 1
                        )

                    if depth == 1:
                        crawled[title] = {'parent': page_title}
                    else:
                        crawled[title] = {'parent': crawldepth[depth - 1]}

        return crawled

    def _add_to_tocrawl(self, crawled, tocrawl, newlinks, depth):
        for link in newlinks:
            if link not in tocrawl and link not in crawled:
                tocrawl.append([link, depth])

    def _is_external(self, root, host):
        if len(host) > 0:
            if host[0] == '/' or host[0] == '#' or host[0] == '?':
                return False

        host = parse.urlparse(host).hostname
        hostname = parse.urlparse(root).hostname
        if host is None:
            return False
        return host is not hostname and host.find(hostname) == -1

    def _get_external(self, soup, url):
        return [
            l.get('href')
            for l in soup.findAll('a')
            if self._is_external(url, l.get('href'))
        ]

    def _get_domain(self, url):
        hostname = parse.urlparse(url).hostname

        if len(re.findall(r'[0-9]+(?:\.[0-9]+){3}', hostname)) > 0:
            return hostname
        elif len(hostname.split('.')) == 0:
            hostname
        elif hostname.find('www.') != -1:
            return hostname.split('.')[0]
        else:
            return hostname.split('.')[1]

    def _get_page(self, url):
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

    def _get_all_links(self, page, parent):
        return [l.get('href') for l in page.findAll('a')]


dwa = DeepWebAnalyzer("https://www.cnn.com", 1)
print(dwa.start())
