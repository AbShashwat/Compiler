def optimize_ir(ir):

    optimized = []
    seen = set()

    def make_key(instr):
        instr_type = instr.get("type")
        value = instr.get("value")

        if isinstance(value, dict):
            value_tuple = tuple(sorted(value.items()))
        else:
            value_tuple = value

        return (instr_type, value_tuple)

    for instr in ir:

        if instr.get("type") is None:
            continue

        key = make_key(instr)

        if key not in seen:
            optimized.append(instr)
            seen.add(key)

    return optimized