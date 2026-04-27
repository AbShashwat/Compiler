from compiler.lexer import lexer
from compiler.parser import parser, ParserError
from compiler.semantic import semantic_analyzer
from compiler.ir import generate_ir
from compiler.optimizer import optimize_ir
from compiler.compression import compress_ir
from compiler.codegen import generate_markdown, generate_html

import os
import sys


def main():

    try:
        with open("input.txt", encoding="utf-8") as f:
            data = f.read()

        tokens = lexer(data)

        # ---------- PARSER ----------
        try:
            ast = parser(tokens)
        except ParserError as e:
            print(f"SYNTAX ERROR: {e}")
            sys.exit(1)

        # ---------- SEMANTIC ----------
        semantic_errors = semantic_analyzer(ast)
        if semantic_errors:
            print("SEMANTIC ERROR:")
            for err in semantic_errors:
                print(err)
            sys.exit(1)

        # ---------- IR ----------
        ir = generate_ir(ast)
        ir = optimize_ir(ir)
        compressed_ir, pool = compress_ir(ir)

        # ---------- CODEGEN ----------
        md = generate_markdown(compressed_ir, pool)
        html = generate_html(compressed_ir, pool, semantic_errors)

        os.makedirs("output", exist_ok=True)

        with open("output/output.md", "w", encoding="utf-8") as f:
            f.write(md)

        with open("output/output.html", "w", encoding="utf-8") as f:
            f.write(html)

        print("SUCCESS")

    except Exception as e:
        print(f"ERROR: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()