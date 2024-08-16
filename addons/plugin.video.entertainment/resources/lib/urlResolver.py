import xbmcgui

def check_hosted_media(vid_url, subs=False):
    from resolveurl import HostedMediaFile
    return HostedMediaFile(url=vid_url, subs=subs)

def resolve_url(url, subs=False):
    hmf = check_hosted_media(url, subs)
    if not hmf:
        # xbmcgui.Dialog().ok('Indirect hoster_url not supported by smr: {0}'.format(url), 'Resolve URL')
        return False

    try:
        if subs:
            resp = hmf.resolve()
            stream_url = resp.get('url')
        else:
            stream_url = hmf.resolve()
    except Exception as e:
        try:
            msg = str(e)
        except:
            msg = url
        # xbmcgui.Dialog().notification(msg, 'Resolve URL', 5000)
        return False

    if subs:
        return resp
    return stream_url