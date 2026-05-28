import time

from cssinj.utils.dom import Attribute, Element


def test_attribute_assigns_incrementing_ids() -> None:
    a, b = Attribute(name='x', value='1'), Attribute(name='y', value='2')
    assert b.id > a.id


def test_element_assigns_incrementing_ids() -> None:
    a, b = Element(name='div'), Element(name='span')
    assert b.id > a.id


def test_element_last_seen_is_fresh_for_each_instance() -> None:
    e1 = Element(name='div')
    time.sleep(0.005)
    e2 = Element(name='div')
    assert e2.last_seen > e1.last_seen, 'last_seen must be set per-instance, not at import time'


def test_element_parent_link_appends_self_to_children() -> None:
    root = Element(name='html')
    child = Element(name='body', parent=root)
    assert child in root.children
    assert child.parent is root


def test_element_without_parent_does_not_explode() -> None:
    e = Element(name='div')
    assert e.parent is None
    assert e.children == []


def test_default_attributes_list_is_not_shared() -> None:
    e1, e2 = Element(name='div'), Element(name='div')
    e1.attributes.append(Attribute(name='x', value='1'))
    assert e2.attributes == [], 'default_factory must give each instance its own list'
