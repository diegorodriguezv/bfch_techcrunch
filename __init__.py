from chanutils import get_doc, select_all, select_one, get_attr, get_text
from playitem import PlayItem, PlayItemList

_SEARCH_URL = "https://techcrunch.com/"

_FEEDLIST = [
  {'title':'Bullish', 'url':'http://techcrunch.com/video/bullish/'},
  {'title':'Crunch Report', 'url':'http://techcrunch.com/video/crunchreport/'},
  {'title':'CrunchWeek', 'url':'http://techcrunch.com/video/crunchweek/'},
  {'title':'Fly or Die', 'url':'http://techcrunch.com/video/fly-or-die/'},
  {'title':'Tc Cribs', 'url':'http://techcrunch.com/video/tc-cribs/'},
  {'title':'TC Gadgets', 'url':'http://techcrunch.com/video/techcrunch-gadgets/'},
  {'title':'TC Interviews', 'url':'http://techcrunch.com/video/interviews/'},
  {'title':'TCTV News', 'url':'http://techcrunch.com/video/tctv-news/'},
  

]
def name():
  return 'Tech Crunch'

def image():
  return 'icon.png'

def description():
  return "Tech Crunch (<a target='_blank' href='https://techcrunch.com'>https://techcrunch.com/a>)."

def feedlist():
  return _FEEDLIST

def feed(idx):
  doc = get_doc(_FEEDLIST[idx]['url'])
  rtree = select_all(doc, 'ul.g li.gi')
  results = PlayItemList()
  i = 0
  for l in rtree:
    if i > 11:
        break
    i+=1
    el = select_one(l, 'a')
    url = get_attr(el, 'href')
    el = select_one(l, 'img')
    img = get_attr(el, 'src')
    el = select_one(l, 'h4.talk-link__speaker')
    subtitle = get_text(el)
    el = select_one(l, 'div.block-title h3')
    title = get_text(el)
    results.add(PlayItem(title, img, url, subtitle))
  return results

def search(q):
  data = get_json(_SEARCH_URL, params={'q':q}, proxy=True)
  if not 'list' in data:
    return []
  rtree = data['list']
  results = PlayItemList()
  for r in rtree:
    cat = r['category']
    if not (cat in _CAT_WHITELIST):
      continue
    title = replace_entity(r['title'])
    subs = None
    if cat == 'Movies':
      subs = movie_title_year(title)
    elif cat == 'TV':
      subs = series_season_episode(title)
    img = '/img/icons/film.svg'
    if cat == 'Music':
      img = '/img/icons/music.svg'
    size = byte_size(r['size'])
    subtitle = chanutils.torrent.subtitle(size, r['seeds'], r['peers'])
    url = r['torrentLink']
    results.add(TorrentPlayItem(title, img, url, subtitle, subs=subs))
  return results

