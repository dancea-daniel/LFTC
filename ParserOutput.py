from prettytable import PrettyTable

from LFTC.grammar import Grammar


class ParserOutput:
    def __init__(self):
        self.grammar = Grammar()
        self.index = 1
        self.table = dict()
        self.bfs_list = []

    def make_grammar(self):
        self.grammar.read_grammar_from_file("g4.txt")
        closure_list = self.grammar.canonical_collection()
        try:
            ps_table = self.grammar.create_action_parsing_table(closure_list)
            tree = self.grammar.parsing(ps_table, ["a", "b", "b", "c"])
            self.bfs_table(tree)
            print(f"table: {self.table}")
        except Exception as e:
            print(e)

    def bfs_table(self,tree):
        self.bfs_list.append((tree[0], self.index))
        first_key = next(iter(tree[0]))
        self.table[1] = (first_key, 0, 0)
        while len(self.bfs_list) != 0:
            item = self.bfs_list.pop(0)
            self.create_father_sibling_table(item[0], item[1])

    def create_father_sibling_table(self, tree:dict, parent_index):
        right_sibling = 0
        for key, value in tree.items():
            for i in range(len(value)):
                self.index += 1
                if type(value[i]) is dict:
                    self.bfs_list.append((value[i], self.index))

                    first_key = next(iter(value[i]))
                    self.table[self.index] = (first_key, parent_index, right_sibling)
                else:
                    self.table[self.index] = (value[i], parent_index, right_sibling)
                right_sibling = self.index

    def write_out_into_file(self, output_file):
        pretty_table = PrettyTable()
        pretty_table.field_names = ["Index", "Info", "Parent", "Right Sibling"]

        for index, values in self.table.items():
            pretty_table.add_row([index, *values])

        # Write the table to the file
        with open(output_file, 'w') as file:
            file.write(str(pretty_table))

        print(f"Table has been written to {output_file}")


ps = ParserOutput()
ps.make_grammar()
ps.write_out_into_file("out1.txt")