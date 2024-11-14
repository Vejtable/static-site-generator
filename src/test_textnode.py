import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):

         ##TESTING EQUALITIES##
            #NORMAL#
        node = TextNode("This is a text node", TextType.NORMAL, None)
        node2 = TextNode("This is a text node", TextType.NORMAL, None)
        self.assertEqual(node, node2)
            #BOLD#
        node3 = TextNode("This is a text node", TextType.BOLD, None)
        node4 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node3, node4)
            #ITALIC#
        node5 = TextNode("This is a text node", TextType.ITALIC, None)
        node6 = TextNode("This is a text node", TextType.ITALIC, None)
        self.assertEqual(node5, node6)
            #CODE#
        node7 = TextNode("This is a text node", TextType.CODE, None)
        node8 = TextNode("This is a text node", TextType.CODE, None)
        self.assertEqual(node7, node8)
            #LINK#
        node9 = TextNode("This is a text node", TextType.LINK, None)
        node10 = TextNode("This is a text node", TextType.LINK, None)
        self.assertEqual(node9, node10)
            #IMAGE#
        node11 = TextNode("This is a text node", TextType.IMAGE, None)
        node12 = TextNode("This is a text node", TextType.IMAGE, None)
        self.assertEqual(node11, node12)

        ##TESTING INEQUALITIES##
            #NORMAL vs BOLD#
        self.assertNotEqual(node, node3)
            #NORMAL vs ITALIC#
        self.assertNotEqual(node, node5)
            #NORMAL vs CODE#
        self.assertNotEqual(node, node7)
            #NORMAL vs LINK#
        self.assertNotEqual(node, node9)
            #NORMAL vs IMAGE#
        self.assertNotEqual(node, node11)
            #BOLD vs ITALIC#
        self.assertNotEqual(node3, node5)
            #BOLD vs CODE#
        self.assertNotEqual(node3, node7)
            #BOLD vs LINK#
        self.assertNotEqual(node3, node9)
            #BOLD vs IMAGE
        self.assertNotEqual(node3, node11)
            #ITALIC vs CODE#
        self.assertNotEqual(node5, node7)
            #ITALIC vs LINK#
        self.assertNotEqual(node5, node9)
            #ITALIC vs IMAGE#
        self.assertNotEqual(node5, node11)
            #CODE vs LINK#
        self.assertNotEqual(node7, node9)
            #CODE vs IMAGE#
        self.assertNotEqual(node7, node11)
            #LINK vs IMAGE#
        self.assertNotEqual(node9, node11)

if __name__ == "__main__":
    unittest.main()