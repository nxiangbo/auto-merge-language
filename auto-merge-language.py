# -*- coding: UTF-8 -*-

from xml.etree.ElementTree import ElementTree, Element
import xml.etree.ElementTree as ET
import config
import os
import logging.config

# --------------------
# Log config
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(name)s - %(message)s",
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'simple'
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'logging.log',
            'level': 'DEBUG',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'root': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'standard': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        }
    }
}
logging.config.dictConfig(LOGGING)
logger = logging.getLogger('standard')

success_count = 0
error_count = 0


# ------------------------------
# keep comments
class CommentedTreeBuilder(ET.TreeBuilder):
    def __init__(self, *args, **kwargs):
        super(CommentedTreeBuilder, self).__init__(*args, **kwargs)

    def comment(self, data):
        self.start(ET.Comment, {})
        self.data(data)
        self.end(ET.Comment)


# -------------------------------
# parser xml file and replace

def replace(tree, new_tree):
    for elem in new_tree.iter(tag='string'):
        old_elem = find_node(tree, elem.get("name"))
        if old_elem is not None:
            old_elem.text = elem.text
        else:
            new_elem = create_node(elem.attrib, elem.text)
            tree.getroot().append(new_elem)


def find_node(tree, attribute_value):
    for elem in tree.iter(tag='string'):
        if elem.get("name") == attribute_value:
            return elem
    return None


def create_node(attribute_map, text):
    elem = Element('string', attribute_map)
    elem.text = text
    return elem


def read_xml(path):
    tree = ElementTree()
    ET.register_namespace("tools", "http://schemas.android.com/tools")
    ET.register_namespace("xliff", "urn:oasis:names:tc:xliff:document:1.2")
    parser = ET.XMLParser(target=CommentedTreeBuilder())
    tree.parse(path, parser)

    return tree


def write_xml(tree, path):
    tree.write(path, encoding='utf-8', xml_declaration=True)


def indent(elem, level=0):
    i = "\n" + level * "    "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "    "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def execute():
    src_dir_names = get_src_dir_names(config.src_prefix)
    for key in src_dir_names:
        if key in config.dict:
            target = config.dict.get(key)
            execute2(target, key)
        else:
            logger.error("%s is not in config.dict", key)
            global error_count
            error_count = error_count + 1


def execute2(target, src):
    target_path = config.target_prefix + target + config.target_suffix
    src_path = config.src_prefix + src + config.src_suffix
    if os.path.isfile(target_path) and os.path.isfile(src_path):
        processor(target_path, src_path)
        logger.info("Replace successfully " + target + ": " + src)
        global success_count
        success_count = success_count + 1
    elif not os.path.isfile(target_path):
        logger.warn("Can not find target file %s.", target_path)
    else:
        logger.warn("Can not find src file %s.", src_path)


def processor(target_path, src_path):
    target_tree = read_xml(target_path)
    src_tree = read_xml(src_path)
    replace(target_tree, src_tree)
    indent(target_tree.getroot())
    write_xml(target_tree, target_path)


def get_src_dir_names(prefix):
    src_dir_names = []
    for dirpath, dirnames, files in os.walk(prefix):
        src_dir_names.extend(dirnames)
    return src_dir_names


if __name__ == '__main__':
    logger.info("***************Start replacing******************")
    execute()
    logger.info("Success count %d", success_count)
    logger.error("Error count %d", error_count)