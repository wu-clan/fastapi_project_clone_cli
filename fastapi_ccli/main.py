#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from pathlib import Path

import questionary
import typer

sys.path.append(str(Path(__file__).resolve().parent.parent))

from fastapi_ccli.CN.cloner_zh import app_zh
from fastapi_ccli.CN.cloner_zh_form import app_zh_form
from fastapi_ccli.EN.cloner_en import app_en
from fastapi_ccli.EN.cloner_en_form import app_en_form


def main():
    select_language = questionary.form(
        language = questionary.select('Please select your language:', choices=['zh-hans', 'en'], default='en')
    ).unsafe_ask()
    if select_language['language'] == 'zh-hans':
        interactive_zh = typer.confirm('是否以交互模式运行?', default=True)
        if interactive_zh:
            app_zh_form()
        else:
            app_zh()
    else:
        interactive_en = typer.confirm('Whether to run in interactive mode?', default=True)
        if interactive_en:
            app_en_form()
        else:
            app_en()


if __name__ == '__main__':
    main()
