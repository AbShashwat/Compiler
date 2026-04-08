from compiler.ast_nodes import ASTNode


class ParserError(Exception):
    pass


def parser(tokens):

    root = ASTNode("PROGRAM")
    webpage_node = None

    i = 0

    def expect(token_type, index):
        if index >= len(tokens) or tokens[index]["type"] != token_type:
            raise ParserError(f"Expected {token_type} at position {index}")
        return tokens[index]

    while i < len(tokens):

        token = tokens[i]

        if token["type"] == "NEWLINE":
            i += 1
            continue

        if token["type"] == "CREATE":

            expect("WEBPAGE", i + 1)

            webpage_node = ASTNode("WEBPAGE")
            root.add_child(webpage_node)

            i += 2
            continue

        if token["type"] == "ADD":

            if webpage_node is None:
                raise ParserError("ADD used before CREATE WEBPAGE")

            if i + 1 >= len(tokens):
                raise ParserError("Incomplete ADD statement")

            next_token = tokens[i + 1]

            # -------- HEADER --------
            if next_token["type"] == "HEADER":

                j = i + 2

                title_words = []
                while j < len(tokens) and tokens[j]["type"] != "NEWLINE":
                    if tokens[j]["type"] in ["WORD", "STRING"]:
                        title_words.append(tokens[j]["value"].strip('"'))
                    j += 1

                if not title_words:
                    raise ParserError("HEADER requires text")

                title = " ".join(title_words)

                webpage_node.add_child(ASTNode("HEADER", title))

                i = j
                continue

            # -------- IMAGE --------
            if next_token["type"] == "IMAGE":

                j = i + 2

                expect("SOURCE", j)
                j += 1

                if j >= len(tokens) or tokens[j]["type"] not in ["URL", "FILE"]:
                    raise ParserError("IMAGE requires a valid source path")

                src = tokens[j]["value"]
                j += 1

                expect("ALT", j)
                j += 1

                alt_words = []
                while j < len(tokens) and tokens[j]["type"] != "NEWLINE":
                    alt_words.append(tokens[j]["value"].strip('"'))
                    j += 1

                if not alt_words:
                    raise ParserError("ALT requires text")

                alt = " ".join(alt_words)

                webpage_node.add_child(ASTNode("IMAGE", {
                    "src": src,
                    "alt": alt
                }))

                i = j
                continue

            # -------- LINK --------
            if next_token["type"] == "LINK":

                j = i + 2

                if j >= len(tokens) or tokens[j]["type"] != "URL":
                    raise ParserError("LINK requires a URL")

                url = tokens[j]["value"]
                j += 1

                expect("TEXT", j)
                j += 1

                label_words = []
                while j < len(tokens) and tokens[j]["type"] != "NEWLINE":
                    label_words.append(tokens[j]["value"].strip('"'))
                    j += 1

                if not label_words:
                    raise ParserError("TEXT requires label")

                label = " ".join(label_words)

                webpage_node.add_child(ASTNode("LINK", {
                    "url": url,
                    "label": label
                }))

                i = j
                continue

            # -------- FOOTER --------
            if next_token["type"] == "FOOTER":

                webpage_node.add_child(ASTNode("FOOTER", "Footer"))

                i += 2
                continue

            raise ParserError(f"Unknown ADD type at position {i}")

        raise ParserError(f"Unexpected token {token['type']} at position {i}")

    return root