from enum import Enum


class ResultStructType(Enum):
    TABBED_SEARCH_RESULTS = "tabbedSearchResultsRenderer"
    SINGLE_COLUMN_BROWSE_RESULTS = "singleColumnBrowseResultsRenderer"
    SINGLE_COLUMN_MUSIC_WATCH_NEXT_RESULT = "singleColumnMusicWatchNextResultsRenderer"
    TWO_COLUMN_BROWSE_RESULT = "twoColumnBrowseResultsRenderer"


class ContinuationStrucType(Enum):
    CONTINUATION = "continuationContents"
    MUSIC_SHELF = "musicShelfContinuation"
    MUSIC_PLAYLIST_SHELF = "musicPlaylistShelfContinuation"
    SECTION_LIST = "sectionListContinuation"


class ShelfStructType(Enum):
    GRID = "gridRenderer"
    MUSIC_SHELF = "musicShelfRenderer"
    MUSIC_CARD_SHELF = "musicCardShelfRenderer"
    MUSIC_CAROUSEL_SHELF = "musicCarouselShelfRenderer"
    MUSIC_DESCRIPTION_SHELF = "musicDescriptionShelfRenderer"
    MUSIC_PLAYLIST_SHELF = "musicPlaylistShelfRenderer"
    ITEM_SECTION = "itemSectionRenderer"
    PLAYLIST_PANEL = "playlistPanelRenderer"


class ItemStructType(Enum):
    MUSIC_TWO_ROW_ITEM = "musicTwoRowItemRenderer"
    MUSIC_VISUAL_HEADER = "musicVisualHeaderRenderer"
    MUSIC_RESPONSIVE_LIST_ITEM = "musicResponsiveListItemRenderer"
    MUSIC_DETAIL_HEADER = "musicDetailHeaderRenderer"
    MUSIC_IMMERSIVE_HEADER = "musicImmersiveHeaderRenderer"
    MUSIC_MULTI_ROW_LIST_ITEM = "musicMultiRowListItemRenderer"
    PLAYLIST_PANEL_VIDEO = "playlistPanelVideoRenderer"
    PLAYLIST_EXPANDABLE_MESSAGE = "playlistExpandableMessageRenderer"
    AUTOMIX_PREVIEW_VIDEO = "automixPreviewVideoRenderer"
    MESSAGE = "messageRenderer"


class ItemType(Enum):
    SONG = "Song"
    SINGLE = "Single"
    VIDEO = "Video"
    PLAYLIST = "Playlist"
    ALBUM = "Album"
    EP = "EP"
    ARTIST = "Artist"
    EPISODE = "Episode"
    PROFILE = "Profile"
    PODCAST = "Podcast"

    def __repr__(self) -> str:
        return f"itde.ItemType.{str(self)}"

    def __str__(self) -> str:
        return self.value


class ShelfType(Enum):
    SHELF = "Shelf"
    CARD_SHELF = "CardShelf"

    def __repr__(self) -> str:
        return f"itde.ShelfType.{str(self)}"

    def __str__(self) -> str:
        return self.value


class EndpointType(Enum):
    WATCH = "watchEndpoint"
    BROWSE = "browseEndpoint"
    SEARCH = "searchEndpoint"
    URL = "urlEndpoint"

    def __repr__(self) -> str:
        return f"itde.EndpointType.{str(self)}"

    def __str__(self) -> str:
        return self.value


class TextDivisorType(Enum):
    BULLET_POINT = "\u2022"
