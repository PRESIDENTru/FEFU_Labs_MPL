import re


class GoToPythonTranslator:
    def __init__(self):
        self.patterns = [
            (r"fmt\.Println\s*\((.*?)\)", r"print(\1)"),

            (r"var\s+(\w+)\s+\w+\s*=\s*(.+)", r"\1 = \2"),

            (r"(\w+)\s*:=\s*(.+)", r"\1 = \2"),

            (r"(\w+)\s+\w+", r"\1"),
        ]

    def translate_function(self, line):
        match = re.match(
            r"func\s+(\w+)\s*\((.*?)\)\s*(\w+)?\s*\{",
            line
        )
        if not match:
            return None

        name, args, _ = match.groups()
        args = re.sub(r"(\w+)\s+\w+", r"\1", args)
        return f"def {name}({args}):"

    def translate_for(self, line):
        match = re.match(
            r"for\s+(\w+)\s*:=\s*(\d+);\s*\1\s*<\s*(\d+);\s*\1\+\+\s*\{",
            line
        )
        if match:
            var, start, end = match.groups()
            return f"for {var} in range({start}, {end}):"
        return None

    def translate_line(self, line):
        stripped = line.strip()

        if stripped.startswith("package "):
            return ""

        if stripped.startswith("import"):
            return ""

        if stripped.startswith("func"):
            result = self.translate_function(stripped)
            if result:
                return result

        if stripped.startswith("for"):
            result = self.translate_for(stripped)
            if result:
                return result

        for pattern, repl in self.patterns:
            line = re.sub(pattern, repl, line)

        line = line.replace("{", ":")
        return line.strip()

    def translate(self, go_code):
        lines = go_code.splitlines()
        py_lines = []
        indent = 0

        for line in lines:
            stripped = line.strip()

            if stripped == "}":
                indent = max(0, indent - 1)
                continue

            py_line = self.translate_line(stripped)
            if not py_line:
                continue

            header = py_line.lstrip()
            if re.match(r"(def|for|if|else|elif)\b", header):
                py_lines.append("    " * indent + header)
                if header.endswith(":"):
                    indent += 1
            else:
                py_lines.append("    " * indent + py_line)

        return "\n".join(py_lines)

    def translate_file(self, input_file):
        with open(input_file, "r", encoding="utf-8") as f:
            go_code = f.read()

        py_code = self.translate(go_code)

        with open("pycode.py", "w", encoding="utf-8") as f:
            f.write(py_code)

        print("Записано в pycode.py")
        return py_code


if __name__ == "__main__":
    translator = GoToPythonTranslator()
    print(translator.translate_file("main.go"))
