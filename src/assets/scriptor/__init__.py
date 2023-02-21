import asyncio

from .utils import get_json_object



from .network import Request
from .viur import viur
from .csvwriter import MemoryCsvWriter, FileSystemCsvWriter
from .logger import Logging as logging
from .module import ListModule, SingletonModule, TreeModule

from .writer import DirectoryPickerWriter, FilePickerWriter, MemoryWriter
from .readers import FilePickerReader

try:
	from js import console
except ModuleNotFoundError:
	pass


import json
import copy


def print(*args, **kwargs):
	logging.info(*args, **kwargs)


class prototypes:
	list = ListModule
	singleton = SingletonModule
	tree = TreeModule


viur.prototypes = prototypes()

try:
	viur.modules
except AttributeError:
	viur.modules = []

async def init():
	resp = await viur.request.get("/config", renderer="vi")
	viur.modules = resp["modules"]
	console.log("response = ", resp)
