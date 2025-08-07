class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        output = ""
        if not self.props:
            return output
        for key, value in self.props.items():
            output += f' {key}="{value}"'
        return output


    def __repr__(self):
        return f"""
            tag = {self.tag}
            value = {self.value}
            children = {self.children}
            props = {self.props}
            """
    
    def __eq__(self, other):

        return (
            self.__repr__() == other.__repr__()
        )


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)


    def to_html(self):
        if not self.value:
            raise ValueError()
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Tag cannot be None")
        if not self.children:
            raise ValueError("Children cannot be None")
        html = f"<{self.tag}>"
        for child in self.children:
            html += child.to_html()

        return html + f"</{self.tag}>"
