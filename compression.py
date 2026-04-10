def compress_ir(ir):

    pool = {}
    reverse_pool = {}
    compressed = []

    def get_ref(value):
        if value not in pool:
            idx = len(pool)
            pool[value] = idx
            reverse_pool[idx] = value
        return pool[value]

    for instr in ir:

        instr_type = instr.get("type")
        value = instr.get("value")

        if isinstance(value, str):

            ref = get_ref(value)

            compressed.append({
                "type": instr_type,
                "value_ref": ref
            })

        elif isinstance(value, dict):

            compressed_value = {}

            for k, v in value.items():

                if isinstance(v, str):
                    compressed_value[k + "_ref"] = get_ref(v)
                else:
                    compressed_value[k] = v

            compressed.append({
                "type": instr_type,
                "value": compressed_value
            })

        else:
            compressed.append(instr)

    return compressed, reverse_pool