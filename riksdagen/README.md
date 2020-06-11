# riksdagen-scraper

Downloads debates from [Riksdagen.se](https://riksdagen.se/sv/webb-tv).

## Prerequisites
* python3
* bs4

## Usage
```
python3 riksdagen-scraper.py <url_prefix> <start page> <end page>
```
Sample output
```
$ python3 riksdagen-scraper.py "https://riksdagen.se/sv/webb-tv/?riksmote=2015/16&p=" 85 90
==== Page 85 URL https://riksdagen.se/sv/webb-tv/?riksmote=2015/16&p=85  ====
/sv/webb-tv/video/debatt-om-forslag/forebygga-forhindra-och-forsvara---den-svenska_H301JuU7
/sv/webb-tv/video/debatt-om-forslag/utgiftsomrade-17-kultur-medier-trossamfund-och_H301KrU1
/sv/webb-tv/video/debatt-om-forslag/utgiftsomrade-11-ekonomisk-trygghet-vid-alderdom_H301SfU2
/sv/webb-tv/video/debatt-om-forslag/utgiftsomrade-18-samhallsplanering_H301CU1
/sv/webb-tv/video/interpellationsdebatt/regeringens-ambitioner-for-kultur--och-musikskolan_H310220
/sv/webb-tv/video/interpellationsdebatt/regeringens-syn-pa-fatah-och-den-palestinska_H310219
/sv/webb-tv/video/interpellationsdebatt/moderata-krafter-i-palestina-_H310156
/sv/webb-tv/video/interpellationsdebatt/fordomanden-av-attacker-mot-civila-israeler_H310150
/sv/webb-tv/video/interpellationsdebatt/kabinettssekreterarens-besok-i-moskva-_H310147
/sv/webb-tv/video/debatt-om-forslag/vissa-fragor-pa-omradet-for-indirekta-skatter_H301SkU13
/sv/webb-tv/video/debatt-om-forslag/beskattning-av-sakerhetsreserv_H301SkU8
/sv/webb-tv/video/debatt-om-forslag/starkta-rattigheter-for-kollektivtrafikresenarer_H301CU9
==== Page 86 URL https://riksdagen.se/sv/webb-tv/?riksmote=2015/16&p=86  ====
/sv/webb-tv/video/beslut/beslut_H3C320151203SfU4
/sv/webb-tv/video/beslut/beslut_H3C320151203SkU9
```

Possible URL prefixes, check "Riksmöte / årtal" for more.
```
https://riksdagen.se/sv/webb-tv/?riksmote=2019/20&p=
https://riksdagen.se/sv/webb-tv/?riksmote=2018/19&p=
https://riksdagen.se/sv/webb-tv/?riksmote=2017/18&p=
https://riksdagen.se/sv/webb-tv/?riksmote=2016/17&p=
https://riksdagen.se/sv/webb-tv/?riksmote=2015/16&p=
https://riksdagen.se/sv/webb-tv/?riksmote=2014/15&p=
https://riksdagen.se/sv/webb-tv/?riksmote=2013/14&p=
https://riksdagen.se/sv/webb-tv/?riksmote=2012/13&p=
https://riksdagen.se/sv/webb-tv/?riksmote=2011/12&p=
https://riksdagen.se/sv/webb-tv/?riksmote=2010/11&p=
https://riksdagen.se/sv/webb-tv/?riksmote=2009/10&p=
https://riksdagen.se/sv/webb-tv/?riksmote=2008/09&p=
https://riksdagen.se/sv/webb-tv/?riksmote=2007/08&p=
https://riksdagen.se/sv/webb-tv/?riksmote=2006/07&p=
https://riksdagen.se/sv/webb-tv/?riksmote=2005/06&p=
https://riksdagen.se/sv/webb-tv/?riksmote=2004/05&p=
https://riksdagen.se/sv/webb-tv/?riksmote=2003/04&p=
https://riksdagen.se/sv/webb-tv/?riksmote=2002/03&p=
https://riksdagen.se/sv/webb-tv/?riksmote=2001/02&p=
https://riksdagen.se/sv/webb-tv/?riksmote=2000/01&p=
```


