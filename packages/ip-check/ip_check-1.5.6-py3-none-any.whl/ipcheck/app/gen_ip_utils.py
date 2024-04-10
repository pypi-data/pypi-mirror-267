#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from typing import List
from ipcheck.app.config import Config
from ipcheck.app.ip_info import IpInfo
from ipcheck.app.ipparser.ip_dir_parser import IpDirParser
from ipcheck.app.ipparser.ip_file_parser import IpFileParser
from ipcheck.app.ipparser.ip_cidr_parser import IpCidrParser
from ipcheck.app.ipparser.ip_parser import IpParser
from ipcheck.app.ipparser.ip_port_parser import IpPortParser


def gen_ip_list_by_arg(source) -> List[IpInfo]:
    ip_list = []
    parsers = [IpDirParser(source), IpFileParser(source), IpParser(source), IpCidrParser(source), IpPortParser(source)]
    for parser in parsers:
        if parser.is_valid:
            ips = parser.parse()
            ip_list.extend(ips)
            break
    config = Config()
    if config.white_list:
        ip_list = filter_ip_list_by_white_list(ip_list, config.white_list)
    if config.block_list:
        ip_list = filter_ip_list_by_block_list(ip_list, config.block_list)
    return ip_list

def filter_ip_list_by_white_list(ip_list: List[IpInfo], white_list):
    fixed_list = []
    for pref_str in white_list:
        fixed_list = [ip_info for ip_info in ip_list if ip_info.ip.startswith(pref_str)]
    return fixed_list

def filter_ip_list_by_block_list(ip_list: List[IpInfo], block_list):
    fixed_list = []
    for block_str in block_list:
        fixed_list = [ip_info for ip_info in ip_list if not ip_info.ip.startswith(block_str)]
    return fixed_list