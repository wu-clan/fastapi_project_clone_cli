#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import time
from typing import Optional

import questionary
import typer
from rich import print

from fastapi_ccli import GREEN, RED, github_fs_src, gitee_fs_src, github_ft_src, gitee_ft_src
from fastapi_ccli.utils.get_country import get_current_country
from fastapi_ccli.utils.get_ip import get_net_ip
from fastapi_ccli.utils.get_path import get_project_path
from fastapi_ccli.utils.get_src import get_sqlalchemy_app_src

app_zh_form = typer.Typer(rich_markup_mode="rich")


def project_path_callback(project_path: str) -> str:
    """
    选择项目路径.

    :param project_path:
    :return:
    """
    if project_path:
        if not isinstance(project_path, str):
            raise typer.BadParameter("输入错误参数，请输入正确的路径'")
        else:
            use_project_name = project_path
    else:
        use_project_name = '../fastapi_project'
    return use_project_name


def orm_style(orm: str) -> str:
    """
    orm 风格

    :param orm:
    :return:
    """
    return typer.style(orm, fg='green', bold=True)


def is_dns(dns: str) -> str:
    """
    是否使用 dns

    :param dns:
    :return:
    """
    with typer.progressbar(range(5), label='  分析中') as progress:
        for i in progress:
            ip = get_net_ip()
            if ip:
                progress.update(5)
                break
            else:
                time.sleep(0.3)
                progress.update(i)
                continue
        rp = get_current_country(ip)
        if 'CN' in rp:
            ending = GREEN if 'Yes' in dns else RED
        else:
            ending = RED if 'Yes' in dns else GREEN
        return ending


def is_async_app(async_app: str) -> str:
    """
    是否使用异步.

    :param async_app:
    :return:
    """
    ending = GREEN if 'Yes' in async_app else RED
    return ending


def is_generic_crud(generic_crud: str) -> str:
    """
    是否使用泛型 CRUD.

    :param generic_crud:
    :return:
    """
    ending = GREEN if 'Yes' in generic_crud else RED
    return ending


def is_casbin(casbin: str) -> str:
    """
    是否使用 rbac

    :param casbin:
    :return:
    """
    ending = GREEN if 'Yes' in casbin else RED
    return ending


@app_zh_form.command(epilog="由 :beating_heart: wu-clan 制作")
def cloner(
        _version: Optional[bool] = typer.Option(
            None,
            "--version",
            '-V',
            help="打印版本信息并退出"
        ),
        project_path: Optional[str] = typer.Option(
            None,
            "--path",
            "-p",
            callback=project_path_callback,
            help="项目克隆路径，默认为 ../fastapi_project，支持绝对路径或相对路径，"
                 "例如，绝对路径：D:\\fastapi_project，相对路径：../fastapi_project。"
        ),
):
    """
    FastAPI 项目克隆器
    """
    path = get_project_path(project_path)
    path_style = typer.style(path, fg='green', bold=True)
    project_name = typer.style(re.split(r'/|\'|\\|\\\\', project_path)[-1], fg='blue', bold=True)
    result_if = questionary.form(
        orm=questionary.select('请选择你要使用的 orm', choices=['SQLAlchemy', 'Tortoise-ORM'], default='SQLAlchemy'),
        dns=questionary.select('你想使用 dns 吗？', choices=['Yes', 'No'], default='No'),
    ).ask()
    if len(result_if) == 0:
        raise typer.Abort
    dns = is_dns(result_if['dns'])
    orm = orm_style(result_if['orm'])
    if 'SQLAlchemy' in orm:
        result = questionary.form(
            async_app=questionary.select('你想使用异步吗？', choices=['Yes', 'No']),
            generic_crud=questionary.select('你想使用泛型 crud 吗？', choices=['Yes', 'No']),
        ).ask()
        if len(result_if) == 0:
            raise typer.Abort
        async_app = is_async_app(result['async_app'])
        generic_crud = is_generic_crud(result['generic_crud'])
        casbin = None
        if 'True' in generic_crud:
            rbac = questionary.form(casbin=questionary.select('你想使用 rbac 鉴权吗?', choices=['Yes', 'No'])).ask()
            if len(rbac) == 0:
                raise typer.Abort
            if rbac['casbin'] == 'Yes':
                casbin = is_casbin(rbac['casbin'])
        typer.echo('项目名称：' + project_name)
        typer.echo('使用 ORM：' + orm)
        typer.echo('使用 DNS：' + dns)
        typer.echo('使用异步：' + async_app)
        typer.echo('使用泛型 CRUD：' + generic_crud)
        if casbin:
            typer.echo('使用 RBAC 鉴权：' + casbin)
        source = github_fs_src if 'True' in dns else gitee_fs_src
        src = get_sqlalchemy_app_src(
            src=source,
            async_app=async_app,
            generic_crud=generic_crud,
            casbin=casbin
        )
        __exec_clone(orm, src, path, path_style)
    else:
        typer.echo('项目名称：' + project_name)
        typer.echo('使用 ORM：' + orm)
        typer.echo('使用 DNS：' + dns)
        src = github_ft_src if 'True' in dns else gitee_ft_src
        __exec_clone(orm, src, path, path_style)


def __exec_clone(orm: str, src: str, path: str, path_style: str) -> None:
    """
    执行克隆

    :param orm:
    :param src:
    :param path:
    :return:
    """
    try:
        # typer.launch(src)
        if 'SQLAlchemy' in orm:
            print(f'⏳ 开始克隆存储库 {src.split()[1]} 的 {src.split()[0]} 分支')
            out = os.system(f'git clone -b {src} {path}')
        else:
            print(f'⏳ 开始克隆存储库 {src}')
            out = os.system(f'git clone {src} {path}')
        if out != 0:
            raise RuntimeError(out)
    except Exception as e:
        print(f'❌ 克隆项目失败: {e}')
        raise typer.Exit(code=1)
    else:
        print('✅ 项目克隆成功')
        typer.echo(f'请到目录 {path_style} 查看')