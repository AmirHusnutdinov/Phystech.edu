def is_json_correct(json, poles) -> bool:
    flag = True
    for pole in poles:
        flag = flag and pole in json
    return flag and json
