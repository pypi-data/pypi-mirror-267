# standard imports
import re

re_camel = re.compile(r'([a-z0-9]+)([A-Z])')
re_snake = re.compile(r'([a-z0-9]+)_([A-Za-z])')


def camel_to_snake(k):
    s_snake = ''
    right_pos = 0
    for m in re_camel.finditer(k):
        g = m.group(0)
        s_snake += g[:len(g)-1]
        s_snake += '_' + g[len(g)-1].lower()
        right_pos = m.span()[1]
    s_snake += k[right_pos:]
    return s_snake


def snake_to_camel(k):
    s_camel = ''
    right_pos = 0
    for m in re_snake.finditer(k):
        g = m.group(0)
        s_camel += g[:len(g)-2]
        s_camel += g[len(g)-1].upper()
        right_pos = m.span()[1]
    s_camel += k[right_pos:]
    return s_camel


def snake_and_camel_s(k):
    s_camel = camel_to_snake(k)
    s_snake = snake_to_camel(k)
    return (s_snake, s_camel)


def snake_and_camel(src):
    src_normal = {}
    for k in src.keys():
        (s_snake, s_camel) = snake_and_camel_s(k) 
        src_normal[k] = src[k]
        #if s != k:
        if k != s_snake:
            src_normal[s_snake] = src[k]

        if k != s_camel:
            src_normal[s_camel] = src[k]

    return src_normal


def ensure_key(src, key, default_value):
    (s_snake, s_camel) = snake_and_camel_s(key)
    try:
        v = src[s_snake]
    except KeyError:
        try:
            v = src[s_camel]
        except KeyError:
            src[key] = default_value
    return src


def mimic_key(src, key_one, key_two, default_value=None):
    v = None
    try:
        v = src[key_one]
    except KeyError:
        try:
            v = src[key_two]
        except KeyError:
            if default_value != None:
                v = default_value

    if v != None:
        src[key_one] = v
        src[key_two] = v
    return src
