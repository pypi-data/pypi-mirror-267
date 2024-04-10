from tetra import BasicComponent, Component, Library
from sourcetypes import django_html, css

default = Library()


@default.register
class SimpleBasicComponent(BasicComponent):
    template: django_html = "<div id='component'>foo</div>"


@default.register
class SimpleBasicComponentWithCSS(BasicComponent):
    template: django_html = "<div id='component' class='text-red'>bar</div>"
    style: css = ".text-red { color: red; }"


@default.register
class SimpleComponentWithDefaultBlock(BasicComponent):
    template: django_html = (
        "<div id='component'>{% block default %}{% endblock %}</div>"
    )


@default.register
class SimpleComponentWithNamedBlock(BasicComponent):
    template: django_html = "<div id='component'>{% block foo %}{% endblock %}</div>"


@default.register
class SimpleComponentWithNamedBlockWithContent(BasicComponent):
    template: django_html = "<div id='component'>{% block foo %}foo{% endblock %}</div>"


@default.register
class SimpleComponentWithConditionalBlock(BasicComponent):
    template: django_html = """
<div id="component">
{% if blocks.foo %}BEFORE{% block foo %}content{% endblock %}AFTER{% endif %}always
</div>
"""


@default.register
class SimpleComponentWith2Blocks(BasicComponent):
    template: django_html = """
<div id="component">{% block default %}default{% endblock %}{% block foo %}foo{% endblock %}</div>
"""
