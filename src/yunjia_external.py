from pyquery import PyQuery as pq
from EpubCrawler.config import config

def process_img(root):
    el_imgs = root('.lazy-image-holder')
    for i in range(len(el_imgs)):
        el_img = el_imgs.eq(i)
        el_new_img = pq('<img />')
        el_new_img.attr('src', el_img.attr('dataurl'))
        el_img.replace_with(el_new_img)

def get_article(html, url):
    root = pq(html)
    process_img(root)
    title = root(config['title']).eq(0).text().strip()
    
    el_co = root(config['content'])
    co = el_co.html()
    co = f'''
        <blockquote>原文：<a href="{url}">{url}</a></blockquote>{co}
    '''
    return {'title': title, 'content': co}