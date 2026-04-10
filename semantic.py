import re

def semantic_analyzer(ast):

    errors = []

    header_count = 0

    for node in ast.children:

        if node.type == "WEBPAGE":

            if node.children and node.children[0].type != "HEADER":
                errors.append("Header should be the first element")

            for child in node.children:

                # -------- HEADER --------
                if child.type == "HEADER":
                    header_count += 1

                    if len(child.value.strip()) == 0:
                        errors.append("Header cannot be empty")

                # -------- IMAGE --------
                if child.type == "IMAGE":

                    alt = child.value.get("alt", "")

                    if len(alt.strip()) < 3:
                        errors.append("ALT text too short")

                    if alt.lower() in ["image", "img", "photo"]:
                        errors.append("ALT text is too generic")

                # -------- LINK --------
                if child.type == "LINK":

                    label = child.value.get("label", "")

                    if len(label.strip()) < 3:
                        errors.append("Link text too short")

                # -------- FOOTER --------
                if child.type == "FOOTER":

                    if child != node.children[-1]:
                        errors.append("Footer must be last")

    # -------- GLOBAL CHECK --------
    if header_count == 0:
        errors.append("No header present")

    return errors