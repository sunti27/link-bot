#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''ext/rextension/api.py:
Rextester api: https://rextester.com
'''

###### IMPORTS ######

from typing import List

import aiohttp
import asyncio
import base64
from dataclasses import dataclass
import enum

###### MAIN ######

EDITOR = 3
LAYOUT = 1

ENDPOINT = 'http://rextester.com/rundotnet/Run'

class Language(enum.IntEnum):
    csharp = 1
    visual_basic = 2
    fsharp = 3
    java = 4
    python2 = 5
    c = gccc = 6
    cpp = gcccpp = 7
    php = 8
    pascal = 9
    objc = 10
    haskell = 11
    ruby = 12
    perl = 13
    lua = 14
    assembly = 15
    sqlserver = 16
    clientside_js = clientside_javascript = 17
    commonlisp = 18
    prolog = 19
    go = 20
    scala = 21
    scheme = 22
    js = javascript = nodejs = 23
    python = python3 = 24
    octave = 25
    clangc = 26
    clangcpp = 27
    visualcpp = 28
    visualc = 29
    d = 30
    r = 31
    tcl = 32
    mysql = 33
    sql = postgresql = 34
    oracle = 35
    html = 36
    swift = 37
    bash = 38
    ada = 39
    erlang = 40
    elixir = 41
    ocaml = 42
    kotlin = 43
    brainfuck = 44
    fortran = 45

@dataclass(repr=True)
class RextesterResponse:
    warnings: str
    errors: str
    files: List[bytes]
    stats: str
    result: str

async def execute(sesh: aiohttp.ClientSession, lang: Language,
                  source: str, compiler_args: str=None) -> RextesterResponse:
    '''
    Executes the given source code as the given language under rextester
    :param sesh: the aiohttp session to use.
    :param lang: the language to compile as.
    :param source: the source to compile.
    :param compiler_args: optional compiler args. Only applicable for C/C++
    :return: the response.
    '''

    form_args = {
        'LanguageChoiceWrapper': lang.value,
        'EditorChoiceWrapper': EDITOR,
        'LayoutChoiceWrapper': LAYOUT,
        'Program': source,
        'Input': '',
        'ShowWarnings': True,
        'Privacy': '',
        'PrivacyUsers': '',
        'Title': '',
        'SavedOutput': '',
        'WholeError': '',
        'WholeWarning': '',
        'StatsToSave': '',
        'CodeGuid': ''
    }

    if compiler_args:
        form_args['CompilerArgs'] = compiler_args

    async with sesh.post(ENDPOINT, data=form_args) as resp:
        resp.raise_for_status()

        data = await resp.json(content_type='text/html')

    return RextesterResponse(
        data['Errors'],
        data['Warnings'],
        list(map(base64.b64decode, (data['Files'] or {}).values())),
        data['Stats'],
        data['Result']
    )
