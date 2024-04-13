"""A python implementation of the JsonCanvas format: https://github.com/obsidianmd/jsoncanvas/blob/main/spec/1.0.md"""


import pydantic, pydantic.alias_generators, typing, pprint, functools, collections.abc

__version__: str = '2.0.0'
__spec_version__: str = '1.0'

class CanvasData(pydantic.BaseModel, collections.abc.MutableMapping):
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
    id: str
    type: str
    x: int
    y: int
    width: int
    height: int
    color: typing.Optional[str] = None


class TextNode(Node):
    text: str
    type: str = 'text'


class FileNode(Node):
    file: str
    type: str = 'file'
    subpath: typing.Optional[str] = None


class LinkNode(Node):
    url: str
    type: str = 'link'


class GroupNode(Node):
    type: str = 'group'
    label: typing.Optional[str] = None
    background: typing.Optional[str] = None
    backgroundStyle: typing.Optional[str] = None


class Edge(CanvasData):
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
    
    
if __name__ == '__main__':
    canvas = Canvas()
    canvas.create_text_node(id='1', x=0, y=0, width=100, height=100, text='Hello, World!')
    canvas.create_file_node(id='2', x=100, y=100, width=100, height=100, file='example.md')
    canvas.create_link_node(id='3', x=200, y=200, width=100, height=100, url='https://example.com')
    canvas.create_group_node(id='4', x=300, y=300, width=100, height=100)
    canvas.create_edge(id='5', fromNode='1', toNode='2', fromEnd='arrow', toEnd='arrow', color='red', label='Edge')
    pprint.pprint(canvas.dict())