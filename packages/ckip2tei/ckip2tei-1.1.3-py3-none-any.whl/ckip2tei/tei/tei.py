import asyncio
from xml.dom import minidom
import xml.etree.ElementTree as ET

from .tags.body import create_body_tags
from .tags.head import create_header_tag
from .utils import get_year

PostData = dict[str, str | dict[str, int] | list[dict[str, str]]]


async def create_tags(root: ET.Element, post_data: PostData, media: str) -> None:
    """The create_tags function creates TEI XML tags and add them to the root.

    Args:
        root (xml.etree.ElementTree.Element): the root element of the TEI XML tree
        post_data (PostData): the post data
        media (Media): a Taiwan social media name
    """
    meta_data = {
        "media": media,
        "id": post_data.get("id"),
        "author": post_data.get("author"),
        "year": get_year(post_data.get("created_at")),
        "board": post_data.get("board"),
        "title": post_data.get("title"),
    }
    content = (
        post_data.get("title"),
        post_data.get("content"),
        post_data.get("comments"),
    )

    task1 = asyncio.create_task(create_header_tag(root, meta_data))
    task2 = asyncio.create_task(create_body_tags(root, content, meta_data["author"]))
    await asyncio.gather(task1, task2)


def generate_tei_xml(post_data: PostData, media: str) -> str:
    """The generate_tei_xml function generates TEI XML string.

    Args:
        post_data (PostData): the post data
        media (str): a Taiwan social media name
    """

    if not post_data:
        raise ValueError("post_data cannot be empty")

    root = ET.Element("TEI.2")
    asyncio.run(create_tags(root, post_data, media))

    xml_str = minidom.parseString(ET.tostring(root)).childNodes[0]
    return xml_str.toprettyxml(indent="   ")


async def generate_tei_xml_async(post_data: PostData, media: str) -> str:
    """The generate_tei_xml_async function generates TEI XML string asynchronously.

    Args:
        post_data (PostData): the post data
        media (str): a Taiwan social media name
    """

    if not post_data:
        raise ValueError("post_data cannot be empty")

    root = ET.Element("TEI.2")
    await create_tags(root, post_data, media)

    xml_str = minidom.parseString(ET.tostring(root)).childNodes[0]
    return xml_str.toprettyxml(indent="   ")
