from app.youtube.scraper import PublicYouTubeProvider

SAMPLE_RSS_XML = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns:yt="http://www.youtube.com/xml/schemas/2015" xmlns:media="http://search.yahoo.com/mrss/" xmlns="http://www.w3.org/2005/Atom">
 <link rel="self" href="http://www.youtube.com/feeds/videos.xml?channel_id=UCtest123"/>
 <id>yt:channel:UCtest123</id>
 <yt:channelId>UCtest123</yt:channelId>
 <title>Tech Master Channel</title>
 <entry>
  <id>yt:video:vid_001</id>
  <yt:videoId>vid_001</yt:videoId>
  <yt:channelId>UCtest123</yt:channelId>
  <title>How to Master YouTube SEO in 2026</title>
  <link rel="alternate" href="https://www.youtube.com/watch?v=vid_001"/>
  <author>
   <name>Tech Master</name>
   <uri>https://www.youtube.com/channel/UCtest123</uri>
  </author>
  <published>2026-05-10T12:00:00+00:00</published>
  <updated>2026-05-10T12:00:00+00:00</updated>
  <media:group>
   <media:title>How to Master YouTube SEO in 2026</media:title>
   <media:thumbnail url="https://i1.ytimg.com/vi/vid_001/hqdefault.jpg" width="480" height="360"/>
   <media:description>In this video we reveal step by step SEO.\\n00:00 - Intro\\n02:30 - Strategy</media:description>
   <media:community>
    <media:statistics views="45890"/>
   </media:community>
  </media:group>
 </entry>
 <entry>
  <id>yt:video:vid_002</id>
  <yt:videoId>vid_002</yt:videoId>
  <yt:channelId>UCtest123</yt:channelId>
  <title>Top 5 Video Editing Tools</title>
  <link rel="alternate" href="https://www.youtube.com/watch?v=vid_002"/>
  <author>
   <name>Tech Master</name>
  </author>
  <published>2026-05-01T10:00:00+00:00</published>
  <media:group>
   <media:title>Top 5 Video Editing Tools</media:title>
   <media:thumbnail url="https://i1.ytimg.com/vi/vid_002/hqdefault.jpg"/>
   <media:description>Overview of best tools</media:description>
   <media:community>
    <media:statistics views="12450"/>
   </media:community>
  </media:group>
 </entry>
</feed>
"""

def test_parse_rss_entries():
    scraper = PublicYouTubeProvider()
    videos = scraper._parse_rss_entries(SAMPLE_RSS_XML, channel_id="UCtest123")
    assert len(videos) == 2
    
    v1 = videos[0]
    assert v1.video_id == "vid_001"
    assert v1.title == "How to Master YouTube SEO in 2026"
    assert v1.views_count == 45890
    assert v1.channel_id == "UCtest123"
    assert v1.channel_name == "Tech Master"
    assert v1.published_date == "2026-05-10"
    assert v1.has_chapters is True
    assert "i1.ytimg.com" in (v1.thumbnail_url or "")

    v2 = videos[1]
    assert v2.video_id == "vid_002"
    assert v2.views_count == 12450
