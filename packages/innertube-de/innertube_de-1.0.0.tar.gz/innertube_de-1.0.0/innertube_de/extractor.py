import logging
from datetime import time
from datetime import date
from typing import Optional
from typing import Union
from typing import List
from typing import Dict
from typing import Callable
from typing import Any
from innertube_de.endpoints import Endpoint
from innertube_de.endpoints import BrowseEndpoint
from innertube_de.endpoints import WatchEndpoint
from innertube_de.endpoints import UrlEndpoint
from innertube_de.endpoints import SearchEndpoint
from innertube_de.containers import CardShelf
from innertube_de.containers import Shelf
from innertube_de.containers import Container
from innertube_de.items import Item
from innertube_de.items import AlbumItem
from innertube_de.items import VideoItem
from innertube_de.items import ArtistItem
from innertube_de.items import PlaylistItem
from innertube_de.items import SongItem
from innertube_de.items import SingleItem
from innertube_de.items import EPItem
from innertube_de.items import PodcastItem
from innertube_de.items import ProfileItem
from innertube_de.items import EpisodeItem
from innertube_de.types import EndpointType
from innertube_de.types import ContinuationStrucType
from innertube_de.types import ItemStructType
from innertube_de.types import ShelfStructType
from innertube_de.types import ResultStructType
from innertube_de.types import ItemType
from innertube_de.utils import get_item_type
from innertube_de.utils import get
from innertube_de.utils import to_int
from innertube_de.utils import clc_length
from innertube_de.utils import clc_publication_date
from innertube_de.utils import clc_int


log = logging.getLogger(__name__)


class ExtractorError(Exception):
    """ """


class Extractor:
    def __init__(self, log_errors: bool = True, enable_exceptions: bool = True) -> None:
        self.log_errors = log_errors
        self.enable_exceptions = enable_exceptions

    def extract(self, data: Dict) -> Container:
        if not isinstance(data, Dict):
            raise TypeError(
                f"Invalid input type: {type(data)}. "
                "Expected input type: Dict"
            )

        try:
            header_data = self._get(data, "header", opt=True)
            if header_data is None:
                header = None
            else:
                header = self._extract_item(header_data)

            data_contents = self._extract_contents(data)

            container = Container(header=header, contents=None)
            if data_contents is None:
                return container

            contents: List[Shelf] = []

            for entry in data_contents:
                shelf = self._extract_shelf(entry)
                if shelf is not None:
                    contents.append(shelf)

            container.contents = contents
            return container

        except (KeyError, IndexError, TypeError, ValueError):
            raise ExtractorError(
                "An error occurred during the data extraction process. "
                "Please open an issue at https://github.com/g3nsy/innertube-de/issues"
                " and reports this log message."
            )

    def _extract_contents(self, data: Dict) -> Optional[Union[Dict, List]]:
        if ContinuationStrucType.CONTINUATION.value in data:
            key = ContinuationStrucType.CONTINUATION.value
            tmp = self._get(data, key, opt=True) 
            if tmp is not None:
                if ContinuationStrucType.SECTION_LIST.value in tmp:
                    return self._get(data, key, ContinuationStrucType.SECTION_LIST.value, "contents")
                elif ContinuationStrucType.MUSIC_PLAYLIST_SHELF.value in data[key]:
                    return [{ShelfStructType.MUSIC_SHELF.value: self._get(data, key, ContinuationStrucType.MUSIC_PLAYLIST_SHELF.value)}]
                elif ContinuationStrucType.MUSIC_SHELF.value in data[key]:
                    return [{ShelfStructType.MUSIC_SHELF.value: self._get(data, key, ContinuationStrucType.MUSIC_SHELF.value)}]
                else:
                    return None
            else:
                return None

        data = self._get(data, "contents", opt=True)  # type: ignore
        if data is None:
            return None

        if ResultStructType.TWO_COLUMN_BROWSE_RESULT.value in data:
            return self._get(data, ResultStructType.TWO_COLUMN_BROWSE_RESULT.value, "secondaryContents", "sectionListRenderer", "contents")

        elif ResultStructType.SINGLE_COLUMN_BROWSE_RESULTS.value in data:
            tmp1 = self._get(data, ResultStructType.SINGLE_COLUMN_BROWSE_RESULTS.value, "tabs", 0, "tabRenderer", "content", "sectionListRenderer", opt=True)

            if tmp1 is not None:
                tmp2 = self._get(tmp1, "contents", 0, opt=True)
                if tmp2 is not None:
                    if ShelfStructType.GRID.value in tmp2:
                        return self._get(tmp1, "contents")
                    elif ShelfStructType.MUSIC_PLAYLIST_SHELF.value in tmp2:
                        return self._get(tmp1, "contents", 0, "musicPlaylistShelfRenderer", "contents")
                    elif ShelfStructType.MUSIC_CAROUSEL_SHELF.value in tmp2:
                        return self._get(tmp1, "contents")
                    elif ShelfStructType.MUSIC_SHELF.value in tmp2:
                        return self._get(tmp1, "contents")
                    else:
                        return None
                else:
                    return None
            else:
                return None

        elif ResultStructType.TABBED_SEARCH_RESULTS.value in data:
            return self._get(data, ResultStructType.TABBED_SEARCH_RESULTS.value, "tabs", 0, "tabRenderer", "content", "sectionListRenderer", "contents")

        elif ResultStructType.SINGLE_COLUMN_MUSIC_WATCH_NEXT_RESULT.value in data:
            return [{ShelfStructType.PLAYLIST_PANEL.value: self._get(
                data, ResultStructType.SINGLE_COLUMN_MUSIC_WATCH_NEXT_RESULT.value, "tabbedRenderer", "watchNextTabbedResultsRenderer", 
                "tabs", 0, "tabRenderer", "content", "musicQueueRenderer", "content", ShelfStructType.PLAYLIST_PANEL.value, opt=True
            )}]

        else:
            return None

    def _extract_shelf(self, entry: Dict) -> Optional[Shelf]:
        shelf, contents = None, None

        if ShelfStructType.MUSIC_SHELF.value in entry:
            key = ShelfStructType.MUSIC_SHELF.value
            name = self._get(entry, key, "title", "runs", 0, "text", opt=True)
            contents = self._get(entry, key, "contents")
            endpoint = self._extract_endpoint(self._get(entry, key, "bottomEndpoint", opt=True))
            shelf = Shelf(name=name, endpoint=endpoint)

        elif ShelfStructType.MUSIC_CAROUSEL_SHELF.value in entry:
            key = ShelfStructType.MUSIC_CAROUSEL_SHELF.value
            contents = self._get(entry, key, "contents")
            name = self._get(entry, key, "header", "musicCarouselShelfBasicHeaderRenderer", "title", "runs", 0, "text")
            endpoint = self._extract_endpoint(self._get(entry, key, "header", "musicCarouselShelfBasicHeaderRenderer", "title", "runs", 0, "navigationEndpoint", opt=True))
            shelf = Shelf(name=name, endpoint=endpoint, continuation=None)

        elif ShelfStructType.MUSIC_CARD_SHELF.value in entry:
            key = ShelfStructType.MUSIC_CARD_SHELF.value
            contents = self._get(entry, key, "contents", opt=True)
            item = self._extract_item(entry)
            if item is not None:
                shelf = CardShelf(item=item)

        elif ShelfStructType.PLAYLIST_PANEL.value in entry:
            key = ShelfStructType.PLAYLIST_PANEL.value
            name = self._get(entry, key, "title", opt=True)
            contents = self._get(entry, key, "contents")
            shelf = Shelf(name=name, endpoint=None, continuation=None)

        elif ShelfStructType.GRID.value in entry:
            key = ShelfStructType.GRID.value
            shelf = Shelf()
            contents = self._get(entry, key, "items")

        if shelf is not None:
            item_type = get_item_type(shelf.name) if shelf.name else None
            if contents is not None:
                for entry_item in contents:
                    item = self._extract_item(entry_item, item_type)
                    if item is not None:
                        shelf.append(item)
        return shelf

    def _extract_item(self, entry_item: Dict, item_type: Optional[ItemType] = None) -> Optional[Item]:
        if ShelfStructType.MUSIC_CARD_SHELF.value in entry_item:
            key = ShelfStructType.MUSIC_CARD_SHELF.value
            ds = self._get(entry_item, key)
            if ds is None:
                return None
            try:
                tmp = self._get(entry_item, key, "subtitle", "runs", 0, "text")
                item_type = ItemType(tmp)
            except ValueError:
                return None
            name = self._get(ds, "title", "runs", 0, "text")
            endpoint = self._extract_endpoint(self._get(ds, "title", "runs", 0, "navigationEndpoint"))
            thumbnail_url = self._get(ds, "thumbnail", "musicThumbnailRenderer", "thumbnail", "thumbnails", -1, "url")

            match item_type:
                case ItemType.ALBUM:
                    item = AlbumItem(name=name, endpoint=endpoint, thumbnail_url=thumbnail_url)

                case ItemType.ARTIST:
                    subscribers = self._clc_int(self._get(ds, "subtitle", "runs", -1, "text"))
                    item = ArtistItem(name=name, endpoint=endpoint, thumbnail_url=thumbnail_url, subscribers=subscribers)

                case ItemType.VIDEO:
                    views = self._clc_int(self._get(ds, "subtitle", "runs", -3, "text"))
                    length = self._clc_length(self._get(ds, "subtitle", "runs", -1, "text"))
                    item = VideoItem(name=name, endpoint=endpoint, thumbnail_url=thumbnail_url, views=views, length=length)

                case ItemType.EP:
                    item = EPItem(name=name, endpoint=endpoint, thumbnail_url=thumbnail_url)

                case ItemType.SONG:     
                    length = self._clc_length(self._get(ds, "subtitle", "runs", -1, "text"))
                    album_name = self._get(ds, "subtitle", "runs", -3, "text")
                    album_endpoint = self._extract_endpoint(self._get(ds, "subtitle", "runs", -3, "navigationEndpoint"))
                    album_item = AlbumItem(name=album_name, thumbnail_url=thumbnail_url, endpoint=album_endpoint)
                    item = SongItem(name=name, endpoint=endpoint, thumbnail_url=thumbnail_url, length=length, album_item=album_item)

                case ItemType.EPISODE:
                    publication_date = self._clc_publication_date(self._get(ds, "subtitle", "runs", 2))
                    item = EpisodeItem(name=name, endpoint=endpoint, thumbnail_url=thumbnail_url, publication_date=publication_date)

                case _:
                    return None

        elif ItemStructType.MUSIC_RESPONSIVE_LIST_ITEM.value in entry_item:
            key = ItemStructType.MUSIC_RESPONSIVE_LIST_ITEM.value
            ds = self._get(entry_item, key)
            if ds is None:
                return None
            thumbnail_url = self._get(ds, "thumbnail", "musicThumbnailRenderer", "thumbnail", "thumbnails", -1, "url", opt=True)
            name = self._get(ds, "flexColumns", 0, "musicResponsiveListItemFlexColumnRenderer", "text", "runs", 0, "text")
            if item_type is None:
                try:
                    item_type = ItemType(self._get(ds, "flexColumns", 1, "musicResponsiveListItemFlexColumnRenderer", "text", "runs", 0, "text", opt=True))
                except ValueError:
                    item_type = ItemType.SONG

            match item_type:
                case ItemType.ARTIST:
                    subscribers = self._clc_int(self._get(ds, "flexColumns", 1, "musicResponsiveListItemFlexColumnRenderer", "text", "runs", -1, "text", opt=True), opt=True)
                    endpoint = self._extract_endpoint(self._get(ds, "navigationEndpoint"))
                    item = ArtistItem(name=name, endpoint=endpoint, thumbnail_url=thumbnail_url, subscribers=subscribers)

                case ItemType.ALBUM:
                    # artist items in (flexColumns, -1, musicResponsiveListItemFlexColumnRenderer, text, runs)
                    release_year = to_int(self._get(ds, "flexColumns", 1, "musicResponsiveListItemFlexColumnRenderer", "text", "runs", -1, "text"))
                    endpoint = self._extract_endpoint(self._get(ds, "navigationEndpoint"))
                    item = AlbumItem(name=name, endpoint=endpoint, thumbnail_url=thumbnail_url, release_year=release_year, artist_items=None)

                case ItemType.VIDEO:
                    # artist items in (flexColumns, -1, musicResponsiveListItemFlexColumnRenderer, text, runs) Tra 1 e - 5
                    length = self._clc_length(self._get(ds, "flexColumns", 1, "musicResponsiveListItemFlexColumnRenderer", "text", "runs", -1, "text"))
                    views = self._clc_int(self._get(ds, "flexColumns", 1, "musicResponsiveListItemFlexColumnRenderer", "text", "runs", -3, "text"))
                    endpoint = self._extract_endpoint(self._get(ds, "flexColumns", 0, "musicResponsiveListItemFlexColumnRenderer", "text", "runs", -1, "navigationEndpoint"))
                    item = VideoItem(name=name, endpoint=endpoint, thumbnail_url=thumbnail_url, length=length, views=views)

                case ItemType.PLAYLIST:
                    tracks_num = to_int(self._get(ds, "flexColumns", 1, "musicResponsiveListItemFlexColumnRenderer", "text", "runs", -1, "text", opt=True))
                    views = self._clc_int(self._get(ds, "flexColumns", 1, "musicResponsiveListItemFlexColumnRenderer", "text", "runs", -1, "text", opt=True), opt=True)
                    endpoint = self._extract_endpoint(self._get(ds, "navigationEndpoint"))
                    item = PlaylistItem(name=name, endpoint=endpoint, thumbnail_url=thumbnail_url, tracks_num=tracks_num, views=views)

                case ItemType.SINGLE:
                    release_year = to_int(self._get(ds, "flexColumns", 1, "musicResponsiveListItemFlexColumnRenderer", "text", "runs", -1, "text", opt=True))
                    endpoint = self._extract_endpoint(self._get(ds, "navigationEndpoint"))
                    item = SingleItem(name=name, endpoint=endpoint, thumbnail_url=thumbnail_url, release_year=release_year)

                case ItemType.SONG:
                    length = self._clc_length(self._get(ds, "flexColumns", 1, "musicResponsiveListItemFlexColumnRenderer", "text", "runs", -1, "text", opt=True), opt=True)

                    attempt1 = self._clc_int(self._get(ds, "flexColumns", -1, "musicResponsiveListItemFlexColumnRenderer", "text", "runs", -1, "text", opt=True), opt=True)
                    if attempt1 is None:
                        attempt2 = self._clc_int(self._get(ds, "flexColumns", -2, "musicResponsiveListItemFlexColumnRenderer", "text", "runs", -1, "text", opt=True), opt=True)
                        reproductions = attempt2
                    else:
                        reproductions = attempt1

                    endpoint = self._extract_endpoint(self._get(ds, "flexColumns", 0, "musicResponsiveListItemFlexColumnRenderer", "text", "runs", -1, "navigationEndpoint", opt=True))
                    item = SongItem(name=name, endpoint=endpoint, thumbnail_url=thumbnail_url, length=length, reproductions=reproductions, album_item=None)

                case ItemType.EPISODE:
                    endpoint = self._extract_endpoint(self._get(ds, "flexColumns", 0, "musicResponsiveListItemFlexColumnRenderer", "text", "runs", -1, "navigationEndpoint"))
                    item = EpisodeItem(name=name, endpoint=endpoint, thumbnail_url=thumbnail_url)

                case ItemType.PODCAST:
                    endpoint = self._extract_endpoint(self._get(ds, "navigationEndpoint"))
                    item = PodcastItem(name=name, endpoint=endpoint, thumbnail_url=thumbnail_url)

                case ItemType.PROFILE:
                    item_handle = self._get(ds, "flexColumns", 1, "musicResponsiveListItemFlexColumnRenderer", "text", "runs", -1, "text")
                    item = ProfileItem(name=name, thumbnail_url=thumbnail_url, handle=item_handle)

                case ItemType.EP:
                    endpoint = self._extract_endpoint(self._get(ds, "navigationEndpoint"))
                    item = EPItem(name=name, endpoint=endpoint, thumbnail_url=thumbnail_url)

                case _:
                    return None

        elif ItemStructType.MUSIC_TWO_ROW_ITEM.value in entry_item:
            key = ItemStructType.MUSIC_TWO_ROW_ITEM.value
            ds = self._get(entry_item, key)
            if ds is None:
                return None
            thumbnail_url = self._get(ds, "thumbnailRenderer", "musicThumbnailRenderer", "thumbnail", "thumbnails", -1, "url")
            name = self._get(ds, "title", "runs", 0, "text")
            endpoint = self._extract_endpoint(self._get(ds, "navigationEndpoint"))
            if item_type is None:
                try:
                    item_type = ItemType(self._get(ds, "flexColumns", 1, "musicResponsiveListItemFlexColumnRenderer", "text", "runs", 0, "text", opt=True))
                except ValueError:
                    item_type = None

            match item_type:

                case ItemType.ARTIST:
                    subscribers = self._clc_int(self._get(ds, "subtitle", "runs", 0, "text"))
                    item = ArtistItem(name=name, endpoint=endpoint, thumbnail_url=thumbnail_url, subscribers=subscribers)

                case ItemType.ALBUM:
                    release_year = to_int(self._get(get, args=[ds, "subtitle", "runs", -1, "text"], opt=True))
                    item = AlbumItem(name=name, endpoint=endpoint, thumbnail_url=thumbnail_url, release_year=release_year)

                case ItemType.EP:
                    release_year = to_int(self._get(get, args=[ds, "subtitle", "runs", -1, "text"], opt=True))
                    item = EPItem(name=name, endpoint=endpoint, thumbnail_url=thumbnail_url, release_year=release_year)

                case ItemType.VIDEO:
                    views = self._clc_int(self._get(ds, "subtitle", "runs", -1, "text"))
                    item = VideoItem(name=name, endpoint=endpoint, thumbnail_url=thumbnail_url, views=views)

                case ItemType.PLAYLIST:
                    item = PlaylistItem(name=name, endpoint=endpoint, thumbnail_url=thumbnail_url)

                case ItemType.SINGLE:
                    release_year = to_int(self._get(ds, "subtitle", "runs", -1, "text", opt=True))
                    item = SingleItem(name=name, endpoint=endpoint, thumbnail_url=thumbnail_url, release_year=release_year)

                case ItemType.SONG:
                    item = SongItem(name=name, endpoint=endpoint, thumbnail_url=thumbnail_url)

                case ItemType.EPISODE | ItemType.PODCAST | ItemType.PROFILE:
                    return None

                case _:
                    item = Item(name=name, endpoint=endpoint, thumbnail_url=thumbnail_url)

        elif ItemStructType.PLAYLIST_PANEL_VIDEO.value in entry_item:
            key = ItemStructType.PLAYLIST_PANEL_VIDEO.value
            ds = self._get(entry_item, key)
            if ds is None:
                return None
            name = self._get(ds, "title", "runs", -1, "text")
            endpoint = self._extract_endpoint(self._get(ds, "navigationEndpoint"))
            length = self._clc_length(self._get(ds, "lengthText", "runs", -1, "text"))
            thumbnail_url = self._get(ds, "thumbnail", "thumbnails", -1, "url")

            tmp = self._get(ds, "thumbnail", "thumbnails", -1)
            width = self._get(tmp, "width")
            height = self._get(tmp, "height")
            if width / height == 1:
                item = SongItem(name=name, endpoint=endpoint, thumbnail_url=thumbnail_url, length=length, album_item=None)
            else:
                views = self._clc_int(self._get(ds, "longBylineText", "runs", -3, "text", opt=True), opt=True)
                item = VideoItem(name=name, endpoint=endpoint, thumbnail_url=thumbnail_url, length=length, views=views)

        elif ItemStructType.MUSIC_IMMERSIVE_HEADER.value in entry_item:
            key = ItemStructType.MUSIC_IMMERSIVE_HEADER.value
            description = self._get(entry_item, key, "description", "runs", 0, "text", opt=True)
            name = self._get(entry_item, key, "title", "runs", 0, "text")
            thumbnail_url = self._get(entry_item, key, "thumbnail", "musicThumbnailRenderer", "thumbnail", "thumbnails", -1, "url")
            subscribers = self._get(entry_item, key, "subscriptionButton", "subscribeButtonRenderer", "subscriberCountText", "runs", 0, "text")
            item = ArtistItem(name=name, subscribers=subscribers, description=description, thumbnail_url=thumbnail_url, endpoint=None)

        elif ItemStructType.MUSIC_DETAIL_HEADER.value in entry_item:
            key = ItemStructType.MUSIC_DETAIL_HEADER.value
            ds = self._get(entry_item, key)
            if ds is None:
                return None

            try:
                item_type = ItemType(self._get(ds, "subtitle", "runs", 0, "text"))
            except ValueError:
                return None

            name = self._get(ds, "title", "runs", 0, "text")
            thumbnail_url = self._get(ds, "thumbnail", "croppedSquareThumbnailRenderer", "thumbnail", "thumbnails", -1, "url")
            release_year = to_int(self._get(ds, "subtitle", "runs", -1, "text", opt=True))

            if item_type is ItemType.PLAYLIST:
                tracks_num = to_int(self._get(ds, "secondSubtitle", "runs", 2, "text"))
            else:
                tracks_num = to_int(self._get(ds, "secondSubtitle", "runs", 0, "text"))

            match item_type:
                case ItemType.ALBUM:
                    item = AlbumItem(name=name, endpoint=None, thumbnail_url=thumbnail_url, tracks_num=tracks_num, release_year=release_year)

                case ItemType.EP:
                    item = EPItem(name=name, endpoint=None, thumbnail_url=thumbnail_url, tracks_num=tracks_num, release_year=release_year)

                case ItemType.SINGLE:
                    item = SingleItem(name=name, endpoint=None, thumbnail_url=thumbnail_url, tracks_num=tracks_num, release_year=release_year)

                case ItemType.PLAYLIST:
                    views = self._clc_int(self._get(ds, "secondSubtitle", "runs", 0, "text"))
                    item = PlaylistItem(name=name, endpoint=None, thumbnail_url=thumbnail_url, tracks_num=tracks_num, release_year=release_year, views=views)

                case _:
                    return None

        elif ItemStructType.MUSIC_VISUAL_HEADER.value in entry_item:
            key = ItemStructType.MUSIC_VISUAL_HEADER.value
            name = self._get(entry_item, key, "title", "runs", -1, "text")
            thumbnail_url = self._get(entry_item, key, "thumbnail", "musicThumbnailRenderer", "thumbnail", "thumbnails", -1, "url")
            item = Item(name=name, thumbnail_url=thumbnail_url)

        elif ItemStructType.MUSIC_MULTI_ROW_LIST_ITEM.value in entry_item:
            key = ItemStructType.MUSIC_MULTI_ROW_LIST_ITEM.value
            name = self._get(entry_item, key, "title", "runs", 0, "text")
            thumbnail_url = self._get(entry_item, key, "thumbnail", "musicThumbnailRenderer", "thumbnail", "thumbnails", -1, "url")
            endpoint = self._extract_endpoint(self._get(entry_item, key, "title", "runs", 0, "navigationEndpoint"))
            item = Item(name=name, thumbnail_url=thumbnail_url, endpoint=endpoint)

        else:
            return None

        return item

    def _extract_endpoint(self, data: Optional[Dict]) -> Optional[Endpoint]:
        if data is None:
            return None

        elif EndpointType.BROWSE.value in data:
            browse_id = self._get(data, "browseEndpoint", "browseId")
            params = self._get(data, "browseEndpoint", "params", opt=True)
            endpoint = BrowseEndpoint(browse_id, params)

        elif EndpointType.WATCH.value in data:
            video_id = self._get(data, "watchEndpoint", "videoId")
            playlist_id = self._get(data, "watchEndpoint", "playlistId", opt=True)
            params = self._get(data, "watchEndpoint", "params", opt=True)
            endpoint = WatchEndpoint(video_id, playlist_id, params)

        elif EndpointType.SEARCH.value in data:
            query = self._get(data, "searchEndpoint", "query")
            params = self._get(data, "searchEndpoint", "params", opt=True)
            endpoint = SearchEndpoint(query, params)

        elif EndpointType.URL in data:
            url = self._get(data, "urlEndpoint", "url")
            params = self._get(data, "urlEndpoint", "params", opt=True)
            endpoint = UrlEndpoint(url, params)

        else:
            return None

        return endpoint

    @staticmethod
    def _handle_exception(func: Callable) -> Callable:
        def _inner_function(*args, opt: bool = False, **kwargs) -> Optional[Any]:
            if not isinstance(args[0], Extractor):
                raise RuntimeError(
                    f"Invalid input type: {type(args[0])}. "
                    "Expected input type: Extractor"
                )
            try:
                return func(*args, **kwargs)
            except Exception as error:
                if opt is False:
                    if args[0].log_errors:
                        log.exception(f"Executing function {func.__name__} caused an exception:")
                    if args[0].enable_exceptions:
                        raise error
                return None
        return _inner_function
    
    @_handle_exception
    def _clc_length(self, string: Optional[str]) -> Optional[time]:
        if string is None:
            return None
        return clc_length(string)

    @_handle_exception
    def _clc_publication_date(self, string: Optional[str]) -> Optional[date]:
        if string is None:
            return None
        return clc_publication_date(string)

    @_handle_exception
    def _clc_int(self, string: Optional[str]) -> Optional[int]:
        if string is None:
            return None
        return clc_int(string) 

    @_handle_exception
    def _get(self, ds: Dict, *keys) -> Optional[Any]:
        return get(ds, *keys)
