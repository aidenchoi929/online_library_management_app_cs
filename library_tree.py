from library import Book, Periodical, Audiobook
from tabulate import tabulate

#Root, left child node, right child node
class LibraryTreeNode:
    def __init__(self, library_item):
        self.library_item = library_item
        self.left = None
        self.right = None

#Class with methods such as insert, search, search by title, search by id, search by author, delete, min value node, iterator
class LibraryTree:
    def __init__(self):
        self.root = None
    
    # Insert library item into the BST
    def insert(self, library_item):
        if not self.root:
            self.root = LibraryTreeNode(library_item)
        else:
            self._insert(self.root, library_item)
    
    # Helper method to recursively insert library item into the BST
    def _insert(self, node, library_item):
        if library_item.ID < node.library_item.ID:
            if node.left is None:
                node.left = LibraryTreeNode(library_item)
            else:
                self._insert(node.left, library_item)
        else:
            if node.right is None:
                node.right = LibraryTreeNode(library_item)
            else:
                self._insert(node.right, library_item)
    
    # Search for library item by ID(ISSN or ISBN) in the BST
    def search(self, ID):
        return self._search(self.root, ID)
    
    # Helper method to recursively search for library items by ID(ISSN or ISBN) in the BST and return the node(ID) if found
    def _search(self, node, ID):
        if node is None or node.library_item.ID == ID:
            return node
        if ID < node.library_item.ID:
            return self._search(node.left, ID)
        return self._search(node.right, ID)
    
    #Search for library items by item title
    def search_by_title(self, title):
        return self._search_by_title(self.root, title)

    #Helper method to recursively search by title for library items
    def _search_by_title(self, node, title):
        if node is None:
            return None
        if node.library_item.title == title:
            return node.library_item
        left_search = self._search_by_title(node.left, title)
        if left_search is not None:
            return left_search
        return self._search_by_title(node.right, title)
    
    #Search for library items by item id(ISSN or ISBN)
    def search_by_id(self, item_id):
        def inorder_search(node):
            if node is None:
                return None
            if node.library_item.ID == item_id:
                return node.library_item
            left_result = inorder_search(node.left)
            if left_result:
                return left_result
            return inorder_search(node.right)
        return inorder_search(self.root)
    
    #Search for library items by item's author with in-order search
    def search_items_by_author(self, author):
        author = author.lower()
        print(f"\n'{author}''s items will be shown...")
        table = []
        author_exists = False

        def inorder_search(node):
            nonlocal author_exists
            if node:
                inorder_search(node.left)
                item = node.library_item
                if author in item.author.lower():
                    author_exists = True
                    if isinstance(item, Audiobook):
                        item_type = "Audiobook"
                        audio_format = item.audio_format
                    elif isinstance(item, Book):
                        item_type = "Book"
                        audio_format = "N/A"
                    elif isinstance(item, Periodical):
                        item_type = "Periodical"
                        audio_format = "N/A"
                    table.append([item_type, item.ID, item.title, item.category, item.language, item.author, item.year_published, audio_format])
                inorder_search(node.right)

        inorder_search(self.root)
        
        return table, author_exists

    #Delete a library item(deletion)
    def delete(self, library_item):
        if self.root is None:
            print("The tree is empty.")
        else:
            self.root = self._delete(self.root, library_item)
    
    #Helper method to recursively delete library items
    def _delete(self, current_node, node):
        if current_node is None:
            print("Cannot locate the node to delete.")
            return current_node

        if node.ID < current_node.library_item.ID:
            current_node.left = self._delete(current_node.left, node)
        elif node.ID > current_node.library_item.ID:
            current_node.right = self._delete(current_node.right, node)
        else:
            if current_node.left is None:
                return current_node.right
            elif current_node.right is None:
                return current_node.left

            temp = self._min_value_node(current_node.right)
            current_node.library_item = temp.library_item
            current_node.right = self._delete(current_node.right, temp)

        return current_node
    
    # Private helper method that helps to locate the node with the minimum value in the BST, used during the deletion process
    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current
    
    # Returns an iterator for the binary search tree
    def __iter__(self):
        return self.in_order_traversal(self.root)
    
    # Performs an inorder traversal of the BST, which visits the nodes in ascending order
    # Left child node > Parent node(Root) > Right child node
    def in_order_traversal(self, node=None):
        if node is None:
            return
        yield from self.in_order_traversal(node.left)
        yield node.library_item
        yield from self.in_order_traversal(node.right)
    

