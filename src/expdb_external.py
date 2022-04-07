from pyquery import PyQuery as pq


def get_article(html, url):
    rt = pq(html)
    title = rt('h1.card-title').text().strip()
    el_props = rt('h6.stats-title')
    eid = el_props.eq(0).html()
    cve = el_props.eq(1).html()
    au = el_props.eq(2).html()
    tp = el_props.eq(3).html()
    plat = el_props.eq(4).html()
    dt = el_props.eq(5).html()
    code = str(rt('.card-body>pre'))
    
    co = f'''
        <ul>
        <li>EDB-ID: <a href="{url}">{eid}</a></li>
        <li>CVE: {cve}</li>
        <li>Author: {au}</li>
        <li>Type: {tp}</li>
        <li>Platform: {plat}</li>
        <li>Date: {dt}</li>
        </ul>
        {code}
    '''
    
    return {'title': title, 'content': co}