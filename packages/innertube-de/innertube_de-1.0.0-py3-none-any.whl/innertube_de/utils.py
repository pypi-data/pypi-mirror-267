import re
import logging
from datetime import time
from datetime import date
from typing import Optional 
from typing import List 
from typing import Any
from typing import Dict
from innertube_de.items import Item
from innertube_de.items import ArtistItem
from innertube_de.items import VideoItem
from innertube_de.items import AlbumItem
from innertube_de.items import EPItem
from innertube_de.items import PlaylistItem
from innertube_de.items import SingleItem
from innertube_de.items import SongItem
from innertube_de.items import ProfileItem
from innertube_de.items import PodcastItem
from innertube_de.items import EpisodeItem
from innertube_de.types import EndpointType 
from innertube_de.types import ItemType
from innertube_de.endpoints import WatchEndpoint
from innertube_de.endpoints import BrowseEndpoint
from innertube_de.endpoints import UrlEndpoint
from innertube_de.endpoints import SearchEndpoint
from innertube_de.endpoints import Endpoint


log = logging.getLogger(__name__)


def get_month_num(month: str) -> int:
    match month.lower():
        case "jan":
            return 1
        case "feb":
            return 2
        case "mar":
            return 3
        case "apr":
            return 4
        case "may":
            return 5
        case "jun":
            return 6
        case "jul":
            return 7
        case "aug":
            return 8
        case "sep":
            return 9
        case "oct":
            return 10
        case "nov":
            return 11
        case "dec":
            return 12
        case _:
            raise ValueError("Invalid input")


def get_item_type(shelf_name: str) -> Optional[ItemType]:
    if match("song", shelf_name):
        return ItemType.SONG
    if match("single", shelf_name):
        return ItemType.SINGLE
    if match("video", shelf_name):
        return ItemType.VIDEO
    if match("playlist", shelf_name):
        return ItemType.PLAYLIST
    if match("album", shelf_name):
        return ItemType.ALBUM
    if match("artist", shelf_name):
        return ItemType.ARTIST
    if match("episode", shelf_name):
        return ItemType.EPISODE
    if match("profile", shelf_name):
        return ItemType.PROFILE
    if match("podcast", shelf_name):
        return ItemType.PODCAST
    if match("ep", shelf_name):
        return ItemType.EP
    return None


def match(seq: str, title: str) -> bool:
    return re.search(seq, title, re.IGNORECASE) is not None


def get_artist_items(data: List) -> List[ArtistItem]:
    artist_items = []
    for artist_data in data:
        artist_item = ArtistItem()
        artist_item.load(artist_data)
        artist_items.append(artist_item)
    return artist_items


def get_items(data: List) -> List[Item]:
    return [get_item(item_data) for item_data in data]


def get_item(data: Dict) -> Item:
    match data["type"]:
        case ItemType.ARTIST.value:
            item = ArtistItem()
        case ItemType.VIDEO.value:
            item = VideoItem()
        case ItemType.ALBUM.value:
            item = AlbumItem()
        case ItemType.EP.value:
            item = EPItem()
        case ItemType.PLAYLIST.value:
            item = PlaylistItem()
        case ItemType.SINGLE.value:
            item = SingleItem()
        case ItemType.SONG.value:
            item = SongItem()
        case ItemType.PROFILE.value:
            item = ProfileItem()
        case ItemType.PODCAST.value:
            item = PodcastItem()
        case ItemType.EPISODE.value:
            item = EpisodeItem()
        case None:
            item = Item()
        case _:
            raise ValueError("Invalid type")
    item.load(data)
    return item


def get_endpoint(data: Dict) -> Endpoint:
    match data["type"]:
        case EndpointType.URL.value:
            endpoint = UrlEndpoint()
        case EndpointType.BROWSE.value:
            endpoint = BrowseEndpoint()
        case EndpointType.SEARCH.value:
            endpoint = SearchEndpoint()
        case EndpointType.WATCH.value:
            endpoint = WatchEndpoint()
        case _:
            raise ValueError("Invalid type")
    endpoint.load(data)
    return endpoint


def get(ds: Dict, *keys) -> Optional[Any]:
    if len(keys) == 0:
        return ds

    ds = ds[keys[0]]

    return get(ds, *keys[1:])


def clc_int(string: str) -> int:
    _match = re.search(r"(\d+\.\d+|\d+)([BMK])?", string)
    result = _match.group() if _match else ""
    last_char = result[-1]
    if last_char.isupper():
        number = float(result[:-1])
        match last_char:
            case "B":
                factor = 1000000000
            case "M":
                factor = 1000000
            case "K":
                factor = 1000
            case _:
                raise ValueError(f"Unexpected character: {last_char}")
        return int(number * factor)
    else:
        return int(result)


def clc_length(string: str) -> time:
    time_list = list(map(int, [x for x in string.split(":")]))
    match len(time_list):
        case 3:
            return time(hour=time_list[0], minute=time_list[1], second=time_list[2])
        case 2:
            return time(minute=time_list[0], second=time_list[1])
        case _:
            raise ValueError(f"Unexpected time format: {string}")


def clc_publication_date(string: str) -> date:
    month, day, year = string.split()
    return date(month=get_month_num(month), day=int(day[:-1]), year=int(year))


def to_int(el: Optional[str]) -> Optional[int]:
    if isinstance(el, str) and el.isdigit():
        return int(el)
    else:
        return None
