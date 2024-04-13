"""A python implementation of the JsonCanvas format: https://github.com/obsidianmd/jsoncanvas/blob/main/spec/1.0.md"""
import dataclasses
import json
import pathlib
import re
import typing
import functools
import pprint
__version__: str = '1.0.1'

camel_to_name = lambda x: re.sub(r'(?<!^)(?=[A-Z])', '_', x).lower()

@functools.lru_cache
def get_leaf_subclass(cls, name):
    if cls.__subclasses__():
        for subcls in cls.__subclasses__():
            if subcls.__subclasses__():
                return get_leaf_subclass(subcls, name)
            if subcls.__name__ == name:
                return subcls
    return cls
class CanvasData(typing.MutableMapping):
    __getattr__ = __getitem__ = lambda self, key: super().__getattribute__(camel_to_name(key))
    __setattr__ = __setitem__ = lambda self, key, value: super().__setattr__(camel_to_name(key), value)
    __delattr__ = __delitem__ = lambda self, key: super().__delattr__(camel_to_name(key))
    __len__ = lambda self: len(self.__dict__)
    __contains__ = lambda self, key: camel_to_name(key) in self.__dict__
    __iter__ = lambda self: iter(self.__dict__)

    def __new__(cls, *args, **kwargs):
        if cls.__name__ in ['CanvasData', 'Node']:
            raise TypeError(f'Cannot instantiate {cls.__name__} directly')
        if not dataclasses.is_dataclass(cls):
            raise TypeError(f'{cls.__name__} is not a dataclass')
        return super().__new__(cls)

@dataclasses.dataclass(kw_only=True)
class Node(CanvasData):
    id: str
    type: str
    x: int
    y: int
    width: int
    height: int
    color: typing.Optional[str] = None

@dataclasses.dataclass(kw_only=True)
class TextNode(Node):
    text: str
    type: str = 'text'
    
@dataclasses.dataclass(kw_only=True)
class FileNode(Node):
    file: str
    type: str = 'file'
    subpath: typing.Optional[str] = None
    
@dataclasses.dataclass(kw_only=True)
class LinkNode(Node):
    url: str
    type: str = 'link'
    
@dataclasses.dataclass(kw_only=True)
class GroupNode(Node):
    type: str = 'group'
    label: typing.Optional[str] = None
    background: typing.Optional[str] = None
    backgroundStyle: typing.Optional[str] = None
    
@dataclasses.dataclass(kw_only=True)
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
    
@dataclasses.dataclass(kw_only=True)
class Canvas:
    nodes: typing.List[Node] = dataclasses.field(default_factory=list)
    edges: typing.List[Edge] = dataclasses.field(default_factory=list)
    
    def to_json(self):
        return json.dumps(
                {
                        name: [dict(filter(lambda x: x[1] is not None, dataclasses.asdict(obj).items())) for obj in
                               getattr(self, name)]
                        for name in ['nodes', 'edges']
                },
                indent=4
        )
    
    def add_node(self, node):
        self.nodes.append(node)
        return self
    
    def add_edge(self, edge):
        self.edges.append(edge)
        return self
    
    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls(
                nodes=[
                        get_leaf_subclass(Node, node_data['type'].title() + "Node")(**node_data) 
                        for node_data in data.get('nodes', [])
                ],
                edges=[Edge(**edge_data) for edge_data in data.get('edges', [])]
        )
    
    def to_file(self, path):
        path = pathlib.Path(path)
        path.write_text(self.to_json())
    @classmethod
    def from_file(cls, path):
        path = pathlib.Path(path)
        content = path.read_text()
        if not content:
            return cls()
        return cls.from_json(content)
    
    def __str__(self):
        nodes = pprint.pformat(self.nodes)
        edges = pprint.pformat(self.edges)
        # properly indent the nodes and edges
        nodes = '\n'.join('    ' + line for line in nodes.splitlines())
        edges = '\n'.join('    ' + line for line in edges.splitlines())
        return f'Canvas(\n  nodes=\n{nodes}\n  ,\n  edges=\n{edges}\n  \n)'

    
if __name__ == '__main__':
    path = r"G:\vault\Wiki\Untitled.canvas"
    #canvas = Canvas.from_file(path)
    #print(canvas)
    print(json.load(open(path)))