from typing import Dict
from .payload import Payload


def traverse(dictionary: Dict):
    stack = [([], dictionary)]

    while len(stack) > 0:
        rootpath, context = stack.pop()

        def do(key, value):
            path = [*rootpath, str(key)]

            if isinstance(value, dict) or isinstance(value, list):
                stack.append((path, value))  # type: ignore

            return Payload(path=path, key=key, value=value)

        if isinstance(context, dict):
            for key in context:
                yield do(key, context.get(key))

        elif isinstance(context, list):
            for key in range(0, len(context)):
                yield do(key, context[key])

        else:
            break


def juery(dictionary, *keys):
    """
    JSON Query.

    [Syntax]

    ^ = Direct Descendant; ('parent', '^direct_descendant', ...)
    """
    if dictionary != None:
        for payload in traverse(dictionary):
            if len(keys) > len(payload.path):
                continue

            index = 0

            for i in range(0, len(payload.path)):
                if index >= len(keys):
                    # Comparator terminated before
                    # finishing the path.
                    # Exclude this payload.
                    index = -1
                    break

                a = str(keys[index])
                directDescendant = a.startswith("^")

                if directDescendant:
                    a = a[1:]

                b = payload.path[i]

                if a.lower() == b.lower():
                    index += 1

                elif directDescendant:
                    # Not a direct descendant.
                    index = -1
                    break

            if index == len(keys):
                yield payload


def juery_one(dictionary, *keys, default_value=None):
    if dictionary == None:
        return default_value

    for payload in juery(dictionary, *keys):
        return payload

    return default_value


def juery_one_value(dictionary, *keys, default_value=None):
    if dictionary == None:
        return default_value

    for payload in juery(dictionary, *keys):
        return payload.value

    return default_value
