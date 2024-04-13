"""
A python implementation of the JsonCanvas format: https://github.com/obsidianmd/jsoncanvas/blob/main/spec/1.0.md
It allows you to read and write JsonCanvas files in Python, as well as create them from scratch.
"""

import pydantic, pydantic.alias_generators, typing, pprint, functools, collections.abc

__version__: str = '2.0.2'
__spec_version__: str = '1.0'

class CanvasData(pydantic.BaseModel, collections.abc.MutableMapping):
    
    """Base class for all canvas data classes."""
    
    def __len__(self) -> int:
        return len(self.__dict__)

    def __contains__(self, key: str) -> bool:
        return key in self.__dict__

    def __iter__(self) -> typing.Iterator[str]:
        return iter(self.__dict__)
    
    def __getitem__(self, key: str) -> typing.Any:
        return getattr(self, key)
    
    def __setitem__(self, key: str, value: typing.Any) -> None:
        setattr(self, key, value)
        
    def __delitem__(self, key: str) -> None:
        delattr(self, key)

    class Config:
        validate_assignment = True
        validate_default = True
        extra = 'allow'
        

class Node(CanvasData):

    """Base class for all node classes."""

    id: str
    type: str
    x: int
    y: int
    width: int = 100
    height: int = 100
    color: typing.Optional[str] = None


class TextNode(Node):
    """A node that contains text."""
    
    text: str
    type: str = 'text'


class FileNode(Node):
    """A node that contains a file."""
    file: str
    type: str = 'file'
    subpath: typing.Optional[str] = None


class LinkNode(Node):
    """A node that contains a link."""
    url: str
    type: str = 'link'


class GroupNode(Node):
    """A node that contains other nodes."""
    type: str = 'group'
    label: typing.Optional[str] = None
    background: typing.Optional[str] = None
    backgroundStyle: typing.Optional[str] = None


class Edge(CanvasData):
    """An edge between two nodes."""
    id: str
    fromNode: str
    toNode: str
    fromSide: typing.Optional[typing.Literal['top', 'right', 'bottom', 'left']] = None
    toSide: typing.Optional[typing.Literal['top', 'right', 'bottom', 'left']] = None
    fromEnd: typing.Optional[typing.Literal['none', 'arrow']] = None
    toEnd: typing.Optional[typing.Literal['none', 'arrow']] = None
    color: typing.Optional[str] = None
    label: typing.Optional[str] = None


class Canvas(CanvasData):
    nodes: list[Node] = pydantic.Field(default_factory=list)
    edges: list[Edge] = pydantic.Field(default_factory=list)
    
    def _add(self, prop, obj):
        getattr(self, prop).append(obj)
        return self

    def _create(self, type, prop, **kwargs):
        self._add(prop, type(**kwargs))
        
    add_node = functools.partialmethod(_add, 'nodes')
    add_edge = functools.partialmethod(_add, 'edges')

    create_text_node = functools.partialmethod(_create, TextNode, 'nodes')
    create_file_node = functools.partialmethod(_create, FileNode, 'nodes')
    create_link_node = functools.partialmethod(_create, LinkNode, 'nodes')
    create_group_node = functools.partialmethod(_create, GroupNode, 'nodes')
    
    create_edge = functools.partialmethod(_create, Edge, 'edges')
    
    def to_file(self, path: str):
        with open(path, 'w') as f:
            f.write(self.model_dump_json())
            
    @classmethod
    def from_file(cls, path: str):
        return cls.parse_file(path)
    
    
if __name__ == '__main__':
    canvas = Canvas()
    canvas.create_text_node(id='1', x=0, y=0, width=100, height=100, text='Hello, World!')
    canvas.create_file_node(id='2', x=100, y=100, width=100, height=100, file='example.md')
    canvas.create_link_node(id='3', x=200, y=200, width=100, height=100, url='https://example.com')
    canvas.create_group_node(id='4', x=300, y=300, width=100, height=100)
    canvas.create_edge(id='5', fromNode='1', toNode='2', fromEnd='arrow', toEnd='arrow', color='red', label='Edge')
    
    canvas.to_file('example.canvas')
    pprint.pprint(Canvas.from_file('example.canvas').dict())