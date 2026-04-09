def generate_ir(ast):

    ir = []

    for node in ast.children:

        if node.type == "WEBPAGE":

            for child in node.children:

                ir.append({
                    "type": child.type,
                    "value": child.value
                })

    return ir