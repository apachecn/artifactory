from pyquery import PyQuery as pq

def get_article(html, url):
    root = pq(html)
    title = root('#activity-name').eq(0).text().strip()
    
    el_co = root('#js_content')
    el_audios = el_co.find('mpvoice')
    for i in range(len(el_audios)):
        el_audio = el_audios.eq(i)
        name = '🔈 ' + el_audio.attr('name')
        mid = el_audio.attr('voice_encode_fileid')
        link = f'https://res.wx.qq.com/voice/getvoice?mediaid={mid}'
        el_p = root(f'<p><a href="{link}">{name}</a></p>')
        el_audio.parent().replace_with(el_p)
    
    el_iframes = el_co.find('iframe')
    for i in range(len(el_iframes)):
        el_iframe = el_iframes.eq(i)
        link = el_iframe.attr('data-src')
        el_p = el_iframe.parent()
        el_p.html(f'📹 <a href="{link}">{link}</a>')
        el_p.attr('style', '')
    
    co = el_co.html()
    co = f'''
        <blockquote>原文：<a href="{url}">{url}</a></blockquote>{co}
    '''
    return {'title': title, 'content': co}