from django import template
from django.template import TemplateSyntaxError

register = template.Library()


@register.tag
def hover(parser, token):
    try:
        tag_name, title = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError("%r takes two arguments: the modal id and title" % token.contents.split()[0])

    nodelist = parser.parse(('endhover',))
    parser.delete_first_token()
    return HoverNode(title, nodelist)


class HoverNode(template.Node):

    def __init__(self,title, nodelist):
        self.title = title
        self.nodelist = nodelist

    def render(self, context):
        n=0
        a = """<style>
                .documentationtip""" + str(n) + """ {
                  position: relative;
                  display: inline-block;
                  border-bottom: 1px dotted black;
                }

                .documentationtip""" + str(n) + """ .doctiptext""" + str(n) + """{
                  visibility: hidden;
                  width: 280px;
                  background-color: lightGray;
                  color: #000;
                  font-size: xx-small;
                  text-align: center;
                  border-radius: 6px;
                  padding: 5px 0;

                  /* Position the tooltip */
                  position: absolute;
                  z-index: 1;
                }

                .documentationtip""" + str(n) + """:hover .doctiptext""" + str(n) + """ {
                  visibility: visible;
                }
                </style>"""
        arriba = '<div class="documentationtip' + str(n) + '">\n  <span class="doctiptext' + str(
            n) + '">' + self.title + '</span>\n'
        abajo = '</div>'

        output = a + '\n' + arriba + '\n' + self.nodelist.render(context) + '\n' + abajo

        return output

