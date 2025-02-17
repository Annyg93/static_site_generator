class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props if props is not None else {}

    def __eq__(self, other):
        if not isinstance(other, LeafNode):
            return False
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is None:
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html

    def __repr__(self):
        return f"HTMLNode(tag={self.tag!r}, value={self.value!r}, children={self.children!r}, props={self.props!r})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def __eq__(self, other):
        if not isinstance(other, LeafNode):
            return False
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.props == other.props
        )

    def to_html(self):
        if not self.value:
            raise ValueError("invalid HTML: must have a value")
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def __eq__(self, other):
        if not isinstance(other, LeafNode):
            return False
        return (
            self.tag == other.tag
            and self.children == other.children
            and self.props == other.props
        )

    def to_html(self):
        if self.tag is None:
            raise ValueError("invalid HTML: must have a tag")
        if not self.children:
            raise ValueError("invalid HTML: must have children")

        result_string = f"<{self.tag}{self.props_to_html()}>"

        for child in self.children:
            child_html = child.to_html()
            result_string += child_html

        result_string += f"</{self.tag}>"
        return result_string

    def __repr__(self):
        return f"ParentNode({self.tag}, Children: {self.children}, {self.props})"
