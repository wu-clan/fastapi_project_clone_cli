#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import typer

from fastapi_ccli.CN.cloner_zh import app_zh
from fastapi_ccli.CN.cloner_zh_form import app_zh_form
from fastapi_ccli.EN.cloner_en import app_en
from fastapi_ccli.EN.cloner_en_form import app_en_form


def main():
    interactive = typer.confirm('是否以交互模式运行(whether to run in interactive mode)?', default=True)
    language = typer.confirm('是否开启命令行中文提示(Whether to enable the command line Chinese prompt)?', default=True)
    if interactive:
        if language:
            app_zh_form()
        else:
            app_en_form()
    else:
        if language:
            app_zh()
        else:
            app_en()


if __name__ == '__main__':
    main()
