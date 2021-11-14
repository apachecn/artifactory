from pyquery import PyQuery as pq
from urllib.parse import urljoin

def html_enco(s):
    return s.replace('<', '&lt;') \
            .replace('>', '&gt;') \
            .replace("'", '&apos;') \
            .replace('"', '&quot;')

def get_article(html, base):
    root = pq(html)
    el_links = root('a')
    for i in range(len(el_links)):
        el_link = el_links.eq(i)
        url = urljoin(base, el_link.attr('href'))
        el_link.attr('href', url)
    
    title = '-'.join(root('nav .text-muted').eq(0).text().strip().split('-')[1:])
    title = html_enco(title)
    content = f'''
        <blockquote>来源：<a href="{base}">{base}</a></blockquote>
    '''.strip()
    content += '<p>' + root('#DescAndDownloadLeftPart>div').html() + '</p>'
    el_dl_table = root('#DescAndDownloadRightPart table')
    if len(el_dl_table) != 0:
        content += str(el_dl_table.eq(0))
        
    el_video = root('#knowledgeVideo')
    if len(el_video) != 0:
        video = el_video.eq(0).attr('thefile2') or \
                el_video.eq(0).attr('thefile1')
        content += f'<p><a href="{video}">{video}</a></p>'
    
    el_hdrs = root('.panel-heading h2')
    hdrs = [
        f'{i+1}：' + html_enco(el_hdrs.eq(i).text().strip())
        for i in range(len(el_hdrs))
    ]
    
    el_bodies = root('.stepbody')
    secs = []
    
    for i in range(len(el_bodies)):
        el_body = el_bodies.eq(i)
        sec = '<h2>' + hdrs[i] + '</h2>'
        el_text = el_body.find('.interviewAnswer')
        if len(el_text) != 0:
            text = str(el_text.eq(0))
            sec += text
        el_pic = el_body.find('fieldset img')
        if len(el_pic) != 0:
            pic = '<p>' + str(el_pic.eq(0)) + '</p>'
            sec += pic
        el_code = el_body.find('.stepCodeTipsDiv pre')
        if len(el_code) != 0:
            code = str(el_code.eq(0))
            sec += code
        el_video = el_body.find('video.video4step')
        if len(el_video) != 0:
            video = el_video.eq(0).attr('thefile2') or \
                el_video.eq(0).attr('thefile1')
            sec += f'<p><a href="{video}">{video}</a></p>'
        secs.append(sec)
        
    
    content += '\n'.join(secs)
    return {'title': title, 'content': content}
