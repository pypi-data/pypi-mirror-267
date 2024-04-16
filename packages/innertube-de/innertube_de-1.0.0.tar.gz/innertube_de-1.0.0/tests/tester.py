# type: ignore
import os
import json
import sys
import shutil
import traceback
import argparse
import subprocess
import logging
from rich import console
from httpx import ConnectError
from innertube import InnerTube  # type: ignore
from innertube.errors import RequestError
from typing import Any
from typing import Dict
from typing import Callable
from typing import List
from typing import Optional

TEST_PATH = os.path.dirname(__file__)
TEST_DATA = os.path.join(TEST_PATH, "test_data.json")
TEST_INNT = os.path.join(TEST_PATH, "innertube")
TEST_ERRS = os.path.join(TEST_PATH, "errors")
TEST_DUMP = os.path.join(TEST_PATH, "dumps")
ITDE_PATH = os.path.dirname(TEST_PATH)
sys.path.insert(0, ITDE_PATH)

from innertube_de import Extractor        
from innertube_de import Container        
from innertube_de import ExtractorError   
from innertube_de import Item
from innertube_de import AlbumItem 
from innertube_de import ArtistItem 
from innertube_de import EPItem
from innertube_de import CardShelf 
from innertube_de import Shelf
from innertube_de import BrowseEndpoint 
from innertube_de import SearchEndpoint 
from innertube_de import WatchEndpoint
from innertube_de import PlaylistItem 
from innertube_de import SingleItem 
from innertube_de import SongItem
from innertube_de import Endpoint
from innertube_de import BrowseEndpoint   
from innertube_de import SearchEndpoint   
from innertube_de import WatchEndpoint    
from innertube_de import ProfileItem


def clear(path: str) -> None:
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)


clear(TEST_INNT)
clear(TEST_DUMP)
clear(TEST_ERRS)

logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s %(levelname)s in %(module)s]: %(message)s")
cs = console.Console()


class Tester:

    def __init__(self, verbose: bool = False, save_data: bool = True) -> None:
        self.__innertube_client = InnerTube("WEB_REMIX")
        self.__extractor = Extractor(log_errors=True, enable_exceptions=True)

        self.ext_log: List[str] = []  # extraction log
        self.ser_log: List[str] = []  # serialization log
        self.des_log: List[str] = []  # deserialization log
        self.dai_log: List[str] = []  # data integrity log

        self.ext_containers: Dict[str, Optional[Container]] = {}
        self.ser_containers: Dict[str, Optional[Dict]] = {}
        self.des_containers: Dict[str, Optional[Container]] = {}

        self.save_data = save_data
        self.verbose = verbose

        with open(TEST_DATA, mode="r") as file:
            test_data = json.loads(file.read())

        self.__test_sear = test_data["sear"]  # search tests
        self.__test_brow = test_data["brow"]  # browse tests
        self.__test_next = test_data["next"]  # next tests

    def test_search_extraction(self) -> None:
        for test in self.__test_sear:
            self.__do_extraction_test__(
                func=lambda: self.__innertube_client.search(
                    query=test["query"],
                    params=test["params"],
                    continuation=test["continuation"],
                ),
                test_type="sear",
                test_name=test["name"],
            )

    def test_browse_extraction(self) -> None:
        for test in self.__test_brow:
            self.__do_extraction_test__(
                func=lambda: self.__innertube_client.browse(
                    browse_id=test["browse_id"],
                    params=test["params"],
                    continuation=test["continuation"],
                ),
                test_type="brow",
                test_name=test["name"],
            )

    def test_next_extraction(self) -> None:
        for test in self.__test_next:
            self.__do_extraction_test__(
                func=lambda: self.__innertube_client.next(
                    video_id=test["video_id"],
                    playlist_id=test["playlist_id"],
                    params=test["params"],
                    index=test["index"],
                    continuation=test["continuation"],
                ),
                test_type="next",
                test_name=test["name"],
            )

    def test_serialization(self) -> None:
        for name, container in self.ext_containers.items():
            if container is not None:
                try:
                    dump = container.dump()
                    self.ser_containers[name] = dump

                    if self.save_data: 
                        with open(os.path.join(TEST_DUMP, f"{name}.json"), mode="w") as file: 
                            json.dump(dump, file, indent=4) 
                    self.ser_log.append(f"{name} [green][OK][/green]")

                except Exception:
                    traceback.print_exc()
                    self.ser_log.append(f"{name} [red][ER][/red]")

            else:
                self.ser_containers[name] = None
                self.ser_log.append(f"{name} [yellow][NE][/yellow]")

    def test_deserialization(self) -> None:
        for name, container_data in self.ser_containers.items():
            if container_data is not None:
                container = Container()
                container.load(container_data)
                self.des_containers[name] = container
                self.des_log.append(f"{name} [green][OK][/green]")
            else:
                self.des_containers[name] = None
                self.des_log.append(f"{name} [yellow][NE][/yellow]")
        
        # for filename in os.listdir(TEST_DUMP):
        #
        #     with open(os.path.join(TEST_DUMP, filename), mode="r") as file:
        #         name = filename.split(".")[0]
        #         try:
        #             data = json.loads(file.read())
        #             container = Container()
        #             container.load(data)
        #             self.des_containers[name] = container
        #             self.des_log.append(f"{name} [OK]")
        #         except BaseException:
        #             traceback.print_exc()
        #             self.des_log.append(f"{name} [ER]")

    def test_data_integrity(self) -> None:
        for name, container in self.des_containers.items():
            if container is None and self.ext_containers[name] is None:
                self.dai_log.append(f"{name} [yellow][NE][/yellow]")
            elif self.ext_containers[name] == container:
                self.dai_log.append(f"{name} [green][OK][/green]")
            else:
                self.dai_log.append(f"{name} [red][ER][/red]")
                try:
                    compare_container(container, self.ext_containers[name])
                except AssertionError as error:
                    cs.print(name)
                    cs.print(f"{error.args[0]}")
                    cs.print_exception()


    def __do_extraction_test__(self, func: Callable, test_type: str, test_name: str) -> None:
        name = f"{test_type}_{test_name}"
        try:
            innertube_data = func()
            ext_container = self.__extractor.extract(innertube_data)

        except (ExtractorError, RequestError, ConnectError) as error:
            traceback.print_exc()
            self.ext_log.append(f"{name} [red][ER][/red]")
            self.ext_containers[name] = None

            if isinstance(error, ExtractorError) and self.save_data:
                with open(os.path.join(TEST_ERRS, f"{name}.json"), mode="w") as file:
                    json.dump(innertube_data, file, indent=4)  # noqa # type: ignore

        else: 
            self.ext_log.append(f"{name} [green][OK][/green]")
            self.ext_containers[name] = ext_container
            if self.verbose:
                cs.print("---------------------")
                cs.print(f"[blue]{name}[/blue]")
                log_containers(ext_container)
            if self.save_data:
                with open(os.path.join(TEST_INNT, f"{name}.json"), mode="w") as file:
                    json.dump(innertube_data, file, indent=4)

    def print_logs(self) -> None:
        def p(log: List,  index: int) -> None:
            try:
                return log[index]
            except IndexError:
                return None
        cs.print()
        cs.print("+------------------+------------------+------------------+------------------+")
        cs.print("| [blue]EXTRACTION[/blue]       | [blue]SERIALIZATION[/blue]    | [blue]DESERIALIZATION[/blue]  | [blue]DATA INTEGRITY[/blue]   |")
        cs.print("+------------------+------------------+------------------+------------------+")
        for i in range(max(map(len, [self.des_log, self.ser_log, self.dai_log, self.ext_log]))):
            cs.print(f"| {p(self.ext_log, i)} | {p(self.ser_log, i)} | {p(self.des_log, i)} | {p(self.dai_log, i)} |")
        cs.print("+------------------+------------------+------------------+------------------+")


def log_containers(container: Optional[Container]) -> None:
    terminal_dim = get_terminal_dimensions()
    if terminal_dim is None:
        end = 1000
    else:
        end = terminal_dim[1]
    if container is not None:
        for shelf in container.contents:
            cs.print(f"[blue]{shelf.name}[/blue]")
            for item in shelf:
                cs.print(f"{str(item)[:end]}")


def compare_container(a: Container, b: Container) -> None:  
    if type(a) != type(b):
        cs.print(f"Type mismatch. A={type(a)}, B={type(b)}")
        return

    compare_items(a.header, b.header)

    a = a.contents
    b = b.contents

    assert len(a) == len(b)

    for i in range(len(a)):
        shelf_a = a[i]
        shelf_b = b[i]
        compare_shelves(shelf_a, shelf_b)


def compare_inputs_type(func: Callable) -> Callable:
    def _inner(a: Any, b: Any) -> None:
        assert type(a) == type(b), f"Type mismatch. A={type(a)}, B={type(b)}"
        if a is None:
            return
        func(a, b)
    return _inner


@compare_inputs_type
def compare_shelves(a: Shelf, b: Shelf) -> None:
    if isinstance(a, CardShelf):
        compare_items(a.item, b.item)

    compare_endpoints(a.endpoint, b.endpoint)
    assert a.name == b.name
    assert a.continuation == b.continuation

    assert len(a) == len(b)

    for i in range(len(a)):
        item_a = a[i]
        item_b = b[i]

        compare_items(item_a, item_b)


@compare_inputs_type
def compare_items(a: Item, b: Item) -> None:
    compare_endpoints(a.endpoint, b.endpoint)
    assert a.name == b.name
    assert a.thumbnail_url == b.thumbnail_url
    assert a.description == b.description

    if isinstance(a, ArtistItem):
        assert a.subscribers == b.subscribers

    if isinstance(a, AlbumItem) or isinstance(a, EPItem) or isinstance(a, SingleItem):
        assert a.release_year == b.release_year
        assert a.length == b.length
        assert a.description == b.description
        assert len(a.artist_items) == len(b.artist_items)
        for i in range(len(a.artist_items)):
            compare_items(a.artist_items[i], b.artist_items[i])
    
    if isinstance(a, PlaylistItem):
        assert a.views == b.views

    if isinstance(a, SongItem):
        assert a.length == b.length
        assert a.reproductions == b.reproductions
        compare_items(a.album_item, b.album_item)
        # skip artist items

    if isinstance(a, ProfileItem):
        assert a.handle == b.handle


@compare_inputs_type
def compare_endpoints(a: Endpoint, b: Endpoint) -> None:
    # common attributes
    assert a.params == b.params
    assert a.continuation == b.continuation

    if isinstance(a, BrowseEndpoint):
        assert a.browse_id == b.browse_id

    elif isinstance(a, SearchEndpoint):
        assert a.query == b.query

    elif isinstance(a, WatchEndpoint):
        assert a.video_id == b.video_id
        assert a.playlist_id == b.playlist_id
        assert a.index == b.index

    elif isinstance(a, UrlEndpoint):
        assert a.url == b.url
                

def get_terminal_dimensions() -> Optional[List[int]]:
    try:
        dimensions = subprocess.check_output(["stty", "size"]).split()
        return list(map(int, dimensions))
    except subprocess.CalledProcessError:
        return None


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action='store_true')
    parser.add_argument('--save-data', '-s', action='store_true')
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    tester = Tester(
        verbose=args.verbose,
        save_data=args.save_data
    )

    tester.test_search_extraction()
    tester.test_browse_extraction()
    tester.test_next_extraction()

    tester.test_serialization()
    tester.test_deserialization()
    tester.test_data_integrity()

    tester.print_logs()


if __name__ == "__main__":
    main()
