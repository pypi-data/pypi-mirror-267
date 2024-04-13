#!/usr/bin/python3
# -*- coding: utf-8 -*-


try:
    import tomli
except ModuleNotFoundError:
    import tomllib as tomli

from pathlib import Path
from dataclasses import dataclass

from slpkg.configs import Configs
from slpkg.toml_errors import TomlErrors


@dataclass
class Repositories:
    toml_errors = TomlErrors()

    repositories_toml_file: Path = Path(Configs.etc_path, 'repositories.toml')
    repositories_path: Path = Path(Configs.lib_path, 'repos')

    repos_config = {}
    repositories = {}

    data_json: str = 'data.json'
    last_update_json: Path = Path(repositories_path, 'last_update.json')
    default_repository: str = 'sbo'

    sbo_repo: bool = True
    sbo_repo_name: str = 'sbo'
    sbo_repo_path: Path = Path(repositories_path, sbo_repo_name)
    sbo_repo_mirror_packages: str = ''
    sbo_repo_mirror_changelog: str = ''
    sbo_repo_slackbuilds: str = 'SLACKBUILDS.TXT'
    sbo_repo_changelog: str = 'ChangeLog.txt'
    sbo_repo_tag: str = '_SBo'
    sbo_repo_tar_suffix: str = '.tar.gz'

    ponce_repo: bool = False
    ponce_repo_name: str = 'ponce'
    ponce_repo_path: Path = Path(repositories_path, ponce_repo_name)
    ponce_repo_mirror: str = ''
    ponce_repo_slackbuilds: str = 'SLACKBUILDS.TXT'
    ponce_repo_changelog: str = 'ChangeLog.txt'
    ponce_repo_tag: str = '_SBo'
    ponce_repo_tar_suffix: str = '.tar.gz'

    slack_repo: bool = False
    slack_repo_name: str = 'slack'
    slack_repo_path: Path = Path(repositories_path, slack_repo_name)
    slack_repo_mirror_packages: str = ''
    slack_repo_mirror_changelog: str = ''
    slack_repo_packages: str = 'PACKAGES.TXT'
    slack_repo_checksums: str = 'CHECKSUMS.md5'
    slack_repo_changelog: str = 'ChangeLog.txt'
    slack_repo_tag: str = ''

    slack_extra_repo: bool = False
    slack_extra_repo_name: str = 'slack_extra'
    slack_extra_repo_path: Path = Path(repositories_path, slack_extra_repo_name)
    slack_extra_repo_mirror_packages: str = ''
    slack_extra_repo_mirror_changelog: str = ''
    slack_extra_repo_packages: str = 'PACKAGES.TXT'
    slack_extra_repo_checksums: str = 'CHECKSUMS.md5'
    slack_extra_repo_changelog: str = 'ChangeLog.txt'
    slack_extra_repo_tag: str = ''

    slack_patches_repo: bool = False
    slack_patches_repo_name: str = 'slack_patches'
    slack_patches_repo_path: Path = Path(repositories_path, slack_patches_repo_name)
    slack_patches_repo_mirror_packages: str = ''
    slack_patches_repo_mirror_changelog: str = ''
    slack_patches_repo_packages: str = 'PACKAGES.TXT'
    slack_patches_repo_checksums: str = 'CHECKSUMS.md5'
    slack_patches_repo_changelog: str = 'ChangeLog.txt'
    slack_patches_repo_tag: str = ''

    alien_repo: bool = False
    alien_repo_name: str = 'alien'
    alien_repo_path: Path = Path(repositories_path, alien_repo_name)
    alien_repo_mirror_packages: str = ''
    alien_repo_mirror_changelog: str = ''
    alien_repo_packages: str = 'PACKAGES.TXT'
    alien_repo_checksums: str = 'CHECKSUMS.md5'
    alien_repo_changelog: str = 'ChangeLog.txt'
    alien_repo_tag: str = 'alien'

    multilib_repo: bool = False
    multilib_repo_name: str = 'multilib'
    multilib_repo_path: Path = Path(repositories_path, multilib_repo_name)
    multilib_repo_mirror_packages: str = ''
    multilib_repo_mirror_changelog: str = ''
    multilib_repo_packages: str = 'PACKAGES.TXT'
    multilib_repo_checksums: str = 'CHECKSUMS.md5'
    multilib_repo_changelog: str = 'ChangeLog.txt'
    multilib_repo_tag: str = 'alien'

    restricted_repo: bool = False
    restricted_repo_name: str = 'restricted'
    restricted_repo_path: Path = Path(repositories_path, restricted_repo_name)
    restricted_repo_mirror_packages: str = ''
    restricted_repo_mirror_changelog: str = ''
    restricted_repo_packages: str = 'PACKAGES.TXT'
    restricted_repo_checksums: str = 'CHECKSUMS.md5'
    restricted_repo_changelog: str = 'ChangeLog.txt'
    restricted_repo_tag: str = 'alien'

    gnome_repo: bool = False
    gnome_repo_name: str = 'gnome'
    gnome_repo_path: Path = Path(repositories_path, gnome_repo_name)
    gnome_repo_mirror_packages: str = ''
    gnome_repo_mirror_changelog: str = ''
    gnome_repo_packages: str = 'PACKAGES.TXT'
    gnome_repo_checksums: str = 'CHECKSUMS.md5'
    gnome_repo_changelog: str = 'ChangeLog.txt'
    gnome_repo_tag: str = 'gfs'

    msb_repo: bool = False
    msb_repo_name: str = 'msb'
    msb_repo_path: Path = Path(repositories_path, msb_repo_name)
    msb_repo_mirror_packages: str = ''
    msb_repo_mirror_changelog: str = ''
    msb_repo_packages: str = 'PACKAGES.TXT'
    msb_repo_checksums: str = 'CHECKSUMS.md5'
    msb_repo_changelog: str = 'ChangeLog.txt'
    msb_repo_tag: str = 'msb'

    csb_repo: bool = False
    csb_repo_name: str = 'csb'
    csb_repo_path: Path = Path(repositories_path, csb_repo_name)
    csb_repo_mirror_packages: str = ''
    csb_repo_mirror_changelog: str = ''
    csb_repo_packages: str = 'PACKAGES.TXT'
    csb_repo_checksums: str = 'CHECKSUMS.md5'
    csb_repo_changelog: str = 'ChangeLog.txt'
    csb_repo_tag: str = 'csb'

    conraid_repo: bool = False
    conraid_repo_name: str = 'conraid'
    conraid_repo_path: Path = Path(repositories_path, conraid_repo_name)
    conraid_repo_mirror_packages: str = ''
    conraid_repo_mirror_changelog: str = ''
    conraid_repo_packages: str = 'PACKAGES.TXT'
    conraid_repo_checksums: str = 'CHECKSUMS.md5'
    conraid_repo_changelog: str = 'ChangeLog.txt'
    conraid_repo_tag: str = 'cf'

    slackdce_repo: bool = False
    slackdce_repo_name: str = 'slackdce'
    slackdce_repo_path: Path = Path(repositories_path, slackdce_repo_name)
    slackdce_repo_mirror_packages: str = ''
    slackdce_repo_mirror_changelog: str = ''
    slackdce_repo_packages: str = 'PACKAGES.TXT'
    slackdce_repo_checksums: str = 'CHECKSUMS.md5'
    slackdce_repo_changelog: str = 'ChangeLog.txt'
    slackdce_repo_tag: str = 'dce'

    slackonly_repo: bool = False
    slackonly_repo_name: str = 'slackonly'
    slackonly_repo_path: Path = Path(repositories_path, slackonly_repo_name)
    slackonly_repo_mirror_packages: str = ''
    slackonly_repo_mirror_changelog: str = ''
    slackonly_repo_packages: str = 'PACKAGES.TXT'
    slackonly_repo_checksums: str = 'CHECKSUMS.md5'
    slackonly_repo_changelog: str = 'ChangeLog.txt'
    slackonly_repo_tag: str = 'slonly'

    salix_repo: bool = False
    salix_repo_name: str = 'salix'
    salix_repo_path: Path = Path(repositories_path, salix_repo_name)
    salix_repo_mirror_packages: str = ''
    salix_repo_mirror_changelog: str = ''
    salix_repo_packages: str = 'PACKAGES.TXT'
    salix_repo_checksums: str = 'CHECKSUMS.md5'
    salix_repo_changelog: str = 'ChangeLog.txt'
    salix_repo_tag: str = ''

    salix_extra_repo: bool = False
    salix_extra_repo_name: str = 'salix_extra'
    salix_extra_repo_path: Path = Path(repositories_path, salix_extra_repo_name)
    salix_extra_repo_mirror_packages: str = ''
    salix_extra_repo_mirror_changelog: str = ''
    salix_extra_repo_packages: str = 'PACKAGES.TXT'
    salix_extra_repo_checksums: str = 'CHECKSUMS.md5'
    salix_extra_repo_changelog: str = 'ChangeLog.txt'
    salix_extra_repo_tag: str = ''

    slackel_repo: bool = False
    slackel_repo_name: str = 'slackel'
    slackel_repo_path: Path = Path(repositories_path, slackel_repo_name)
    slackel_repo_mirror_packages: str = ''
    slackel_repo_mirror_changelog: str = ''
    slackel_repo_packages: str = 'PACKAGES.TXT'
    slackel_repo_checksums: str = 'CHECKSUMS.md5'
    slackel_repo_changelog: str = 'ChangeLog.txt'
    slackel_repo_tag: str = 'dj'

    slint_repo: bool = False
    slint_repo_name: str = 'slint'
    slint_repo_path: Path = Path(repositories_path, slint_repo_name)
    slint_repo_mirror_packages: str = ''
    slint_repo_mirror_changelog: str = ''
    slint_repo_packages: str = 'PACKAGES.TXT'
    slint_repo_checksums: str = 'CHECKSUMS.md5'
    slint_repo_changelog: str = 'ChangeLog.txt'
    slint_repo_tag: str = 'slint'

    pprkut_repo: bool = False
    pprkut_repo_name: str = 'pprkut'
    pprkut_repo_path: Path = Path(repositories_path, pprkut_repo_name)
    pprkut_repo_mirror_packages: str = ''
    pprkut_repo_mirror_changelog: str = ''
    pprkut_repo_packages: str = 'PACKAGES.TXT'
    pprkut_repo_checksums: str = 'CHECKSUMS.md5'
    pprkut_repo_changelog: str = 'ChangeLog.txt'
    pprkut_repo_tag: str = 'pprkut'

    try:
        if repositories_toml_file.is_file():
            with open(repositories_toml_file, 'rb') as repo:
                repos_config = tomli.load(repo)

            default_repository: str = repos_config['DEFAULT']['REPO'].lower()

            sbo_repo: bool = repos_config['SBO']['ENABLE']
            sbo_repo_url: str = repos_config['SBO']['MIRROR']
            sbo_repo_version: str = repos_config['SBO']['VERSION']
            sbo_repo_mirror_packages: str = f'{sbo_repo_url}{sbo_repo_version}/'
            sbo_repo_mirror_changelog: str = f'{sbo_repo_url}{sbo_repo_version}/'

            ponce_repo: bool = repos_config['PONCE']['ENABLE']
            ponce_repo_mirror: str = repos_config['PONCE']['MIRROR']

            slack_repo: bool = repos_config['SLACK']['ENABLE']
            slack_repo_url: str = repos_config['SLACK']['MIRROR']
            slack_repo_version: str = repos_config['SLACK']['VERSION']
            slack_repo_arch: str = repos_config['SLACK']['ARCH']
            slack_arch: str = ''
            if slack_repo_arch == 'x86_64':
                slack_arch: str = '64'
            slack_repo_mirror_packages: str = f'{slack_repo_url}slackware{slack_arch}-{slack_repo_version}/'
            slack_repo_mirror_changelog: str = f'{slack_repo_url}slackware{slack_arch}-{slack_repo_version}/'

            slack_extra_repo: bool = repos_config['SLACK_EXTRA']['ENABLE']
            slack_extra_repo_url: str = repos_config['SLACK_EXTRA']['MIRROR']
            slack_extra_repo_version: str = repos_config['SLACK_EXTRA']['VERSION']
            slack_extra_repo_arch: str = repos_config['SLACK_EXTRA']['ARCH']
            slack_extra_arch: str = ''
            if slack_extra_repo_arch == 'x86_64':
                slack_extra_arch: str = '64'
            slack_extra_repo_branch: str = repos_config['SLACK_EXTRA']['BRANCH']
            slack_extra_repo_mirror_packages: str = (f'{slack_extra_repo_url}slackware{slack_extra_arch}-'
                                                     f'{slack_extra_repo_version}/{slack_extra_repo_branch}/')
            slack_extra_repo_mirror_changelog: str = (f'{slack_extra_repo_url}slackware{slack_extra_arch}-'
                                                      f'{slack_extra_repo_version}/')

            slack_patches_repo: bool = repos_config['SLACK_PATCHES']['ENABLE']
            slack_patches_repo_url: str = repos_config['SLACK_PATCHES']['MIRROR']
            slack_patches_repo_version: str = repos_config['SLACK_PATCHES']['VERSION']
            slack_patches_repo_arch: str = repos_config['SLACK_PATCHES']['ARCH']
            slack_patches_arch: str = ''
            if slack_patches_repo_arch == 'x86_64':
                slack_patches_arch: str = '64'
            slack_patches_repo_branch: str = repos_config['SLACK_PATCHES']['BRANCH']
            slack_patches_repo_mirror_packages: str = (f'{slack_patches_repo_url}slackware{slack_patches_arch}-'
                                                       f'{slack_patches_repo_version}/{slack_patches_repo_branch}/')
            slack_patches_repo_mirror_changelog: str = (f'{slack_patches_repo_url}slackware{slack_patches_arch}-'
                                                        f'{slack_patches_repo_version}/')

            alien_repo: bool = repos_config['ALIEN']['ENABLE']
            alien_repo_url: str = repos_config['ALIEN']['MIRROR']
            alien_repo_version: str = repos_config['ALIEN']['VERSION']
            alien_repo_arch: str = repos_config['ALIEN']['ARCH']
            alien_repo_mirror_packages: str = f'{alien_repo_url}{alien_repo_version}/{alien_repo_arch}/'
            alien_repo_mirror_changelog: str = alien_repo_url

            multilib_repo: bool = repos_config['MULTILIB']['ENABLE']
            multilib_repo_url: str = repos_config['MULTILIB']['MIRROR']
            multilib_repo_version: str = repos_config['MULTILIB']['VERSION']
            multilib_repo_mirror_packages: str = f'{multilib_repo_url}{multilib_repo_version}/'
            multilib_repo_mirror_changelog: str = multilib_repo_url

            restricted_repo: bool = repos_config['RESTRICTED']['ENABLE']
            restricted_repo_url: str = repos_config['RESTRICTED']['MIRROR']
            restricted_repo_version: str = repos_config['RESTRICTED']['VERSION']
            restricted_repo_arch: str = repos_config['RESTRICTED']['ARCH']
            restricted_repo_mirror_packages: str = (f'{restricted_repo_url}{restricted_repo_version}/'
                                                    f'{restricted_repo_arch}/')
            restricted_repo_mirror_changelog: str = restricted_repo_url

            gnome_repo: bool = repos_config['GNOME']['ENABLE']
            gnome_repo_url: str = repos_config['GNOME']['MIRROR']
            gnome_repo_version: str = repos_config['GNOME']['VERSION']
            gnome_repo_arch: str = repos_config['GNOME']['ARCH']
            gnome_repo_mirror_packages: str = f'{gnome_repo_url}{gnome_repo_version}/{gnome_repo_arch}/'
            gnome_repo_mirror_changelog: str = f'{gnome_repo_url}{gnome_repo_version}/{gnome_repo_arch}/'

            msb_repo: bool = repos_config['MSB']['ENABLE']
            msb_repo_url: str = repos_config['MSB']['MIRROR']
            msb_repo_version: str = repos_config['MSB']['VERSION']
            msb_repo_branch: str = repos_config['MSB']['BRANCH']
            msb_repo_arch: str = repos_config['MSB']['ARCH']
            msb_repo_mirror_packages: str = f'{msb_repo_url}{msb_repo_version}/{msb_repo_branch}/{msb_repo_arch}/'
            msb_repo_mirror_changelog: str = msb_repo_url

            csb_repo: bool = repos_config['CSB']['ENABLE']
            csb_repo_url: str = repos_config['CSB']['MIRROR']
            csb_repo_version: str = repos_config['CSB']['VERSION']
            csb_repo_arch: str = repos_config['CSB']['ARCH']
            csb_repo_mirror_packages: str = f'{csb_repo_url}{csb_repo_version}/{csb_repo_arch}/'
            csb_repo_mirror_changelog: str = csb_repo_url

            conraid_repo: bool = repos_config['CONRAID']['ENABLE']
            conraid_repo_url: str = repos_config['CONRAID']['MIRROR']
            conraid_repo_arch: str = repos_config['CONRAID']['ARCH']
            conraid_repo_version: str = repos_config['CONRAID']['VERSION']
            conraid_arch: str = ''
            if conraid_repo_arch == 'x86_64':
                conraid_arch: str = '64'
            conraid_repo_mirror_packages: str = f'{conraid_repo_url}slackware{conraid_arch}-{conraid_repo_version}/'
            conraid_repo_mirror_changelog: str = f'{conraid_repo_url}slackware{conraid_arch}-{conraid_repo_version}/'

            slackdce_repo: bool = repos_config['SLACKDCE']['ENABLE']
            slackdce_repo_url: str = repos_config['SLACKDCE']['MIRROR']
            slackdce_repo_version: str = repos_config['SLACKDCE']['VERSION']
            slackdce_repo_arch: str = repos_config['SLACKDCE']['ARCH']
            slackdce_repo_mirror_packages: str = f'{slackdce_repo_url}{slackdce_repo_version}/{slackdce_repo_arch}/'
            slackdce_repo_mirror_changelog: str = f'{slackdce_repo_url}{slackdce_repo_version}/{slackdce_repo_arch}/'

            slackonly_repo: bool = repos_config['SLACKONLY']['ENABLE']
            slackonly_repo_url: str = repos_config['SLACKONLY']['MIRROR']
            slackonly_repo_version: str = repos_config['SLACKONLY']['VERSION']
            slackonly_repo_arch: str = repos_config['SLACKONLY']['ARCH']
            slackonly_repo_mirror_packages: str = f'{slackonly_repo_url}{slackonly_repo_version}-{slackonly_repo_arch}/'
            slackonly_repo_mirror_changelog: str = (f'{slackonly_repo_url}{slackonly_repo_version}-'
                                                    f'{slackonly_repo_arch}/')

            salix_repo: bool = repos_config['SALIX']['ENABLE']
            salix_repo_url: str = repos_config['SALIX']['MIRROR']
            salix_repo_arch: str = repos_config['SALIX']['ARCH']
            salix_repo_version: str = repos_config['SALIX']['VERSION']
            salix_repo_mirror_packages: str = f'{salix_repo_url}{salix_repo_arch}/{salix_repo_version}/'
            salix_repo_mirror_changelog: str = f'{salix_repo_url}{salix_repo_arch}/{salix_repo_version}/'

            salix_extra_repo: bool = repos_config['SALIX_EXTRA']['ENABLE']
            salix_extra_repo_url: str = repos_config['SALIX_EXTRA']['MIRROR']
            salix_extra_repo_arch: str = repos_config['SALIX_EXTRA']['ARCH']
            salix_extra_repo_branch: str = repos_config['SALIX_EXTRA']['BRANCH']
            salix_extra_repo_version: str = repos_config['SALIX_EXTRA']['VERSION']
            salix_extra_repo_mirror_packages: str = (f'{salix_extra_repo_url}{salix_extra_repo_arch}/'
                                                     f'{salix_extra_repo_branch}-{salix_extra_repo_version}/')
            salix_extra_repo_mirror_changelog: str = (f'{salix_extra_repo_url}{salix_extra_repo_arch}/'
                                                      f'{salix_extra_repo_branch}-{salix_extra_repo_version}/')

            slackel_repo: bool = repos_config['SLACKEL']['ENABLE']
            slackel_repo_url: str = repos_config['SLACKEL']['MIRROR']
            slackel_repo_arch: str = repos_config['SLACKEL']['ARCH']
            slackel_repo_version: str = repos_config['SLACKEL']['VERSION']
            slackel_repo_mirror_packages: str = f'{slackel_repo_url}{slackel_repo_arch}/{slackel_repo_version}/'
            slackel_repo_mirror_changelog: str = f'{slackel_repo_url}{slackel_repo_arch}/{slackel_repo_version}/'

            slint_repo: bool = repos_config['SLINT']['ENABLE']
            slint_repo_url: str = repos_config['SLINT']['MIRROR']
            slint_repo_arch: str = repos_config['SLINT']['ARCH']
            slint_repo_version: str = repos_config['SLINT']['VERSION']
            slint_repo_mirror_packages: str = f'{slint_repo_url}{slint_repo_arch}/slint-{slint_repo_version}/'
            slint_repo_mirror_changelog: str = f'{slint_repo_url}{slint_repo_arch}/slint-{slint_repo_version}/'

            pprkut_repo: bool = repos_config['PPRKUT']['ENABLE']
            pprkut_repo_url: str = repos_config['PPRKUT']['MIRROR']
            pprkut_repo_version: str = repos_config['PPRKUT']['VERSION']
            pprkut_repo_arch: str = repos_config['PPRKUT']['ARCH']
            pprkut_repo_mirror_packages: str = f'{pprkut_repo_url}{pprkut_repo_version}/{pprkut_repo_arch}/'
            pprkut_repo_mirror_changelog: str = f'{pprkut_repo_url}{pprkut_repo_version}/{pprkut_repo_arch}/'
    except (tomli.TOMLDecodeError, KeyError) as error:
        toml_errors.raise_toml_error_message(error, repositories_toml_file)

    # Dictionary configurations of repositories.
    repositories = {
        sbo_repo_name: {
            'enable': sbo_repo,
            'path': sbo_repo_path,
            'mirror_packages': sbo_repo_mirror_packages,
            'mirror_changelog': sbo_repo_mirror_changelog,
            'slackbuilds_txt': sbo_repo_slackbuilds,
            'changelog_txt': sbo_repo_changelog,
            'repo_tag': sbo_repo_tag,
            'tar_suffix': sbo_repo_tar_suffix},

        ponce_repo_name: {
            'enable': ponce_repo,
            'path': ponce_repo_path,
            'mirror_packages': ponce_repo_mirror,
            'mirror_changelog': ponce_repo_mirror,
            'slackbuilds_txt': ponce_repo_slackbuilds,
            'changelog_txt': ponce_repo_changelog,
            'repo_tag': ponce_repo_tag,
            'tar_suffix': ponce_repo_tar_suffix},

        slack_repo_name: {
            'enable': slack_repo,
            'path': slack_repo_path,
            'mirror_packages': slack_repo_mirror_packages,
            'mirror_changelog': slack_repo_mirror_changelog,
            'packages_txt': slack_repo_packages,
            'checksums_txt': slack_repo_checksums,
            'changelog_txt': slack_repo_changelog,
            'repo_tag': slack_repo_tag},

        slack_extra_repo_name: {
            'enable': slack_extra_repo,
            'path': slack_extra_repo_path,
            'mirror_packages': slack_extra_repo_mirror_packages,
            'mirror_changelog': slack_extra_repo_mirror_changelog,
            'packages_txt': slack_extra_repo_packages,
            'checksums_txt': slack_extra_repo_checksums,
            'changelog_txt': slack_extra_repo_changelog,
            'repo_tag': slack_extra_repo_tag},

        slack_patches_repo_name: {
            'enable': slack_patches_repo,
            'path': slack_patches_repo_path,
            'mirror_packages': slack_patches_repo_mirror_packages,
            'mirror_changelog': slack_patches_repo_mirror_changelog,
            'packages_txt': slack_patches_repo_packages,
            'checksums_txt': slack_patches_repo_checksums,
            'changelog_txt': slack_patches_repo_changelog,
            'repo_tag': slack_patches_repo_tag},

        alien_repo_name: {
            'enable': alien_repo,
            'path': alien_repo_path,
            'mirror_packages': alien_repo_mirror_packages,
            'mirror_changelog': alien_repo_mirror_changelog,
            'packages_txt': alien_repo_packages,
            'checksums_txt': alien_repo_checksums,
            'changelog_txt': alien_repo_changelog,
            'repo_tag': alien_repo_tag},

        multilib_repo_name: {
            'enable': multilib_repo,
            'path': multilib_repo_path,
            'mirror_packages': multilib_repo_mirror_packages,
            'mirror_changelog': multilib_repo_mirror_changelog,
            'packages_txt': multilib_repo_packages,
            'checksums_txt': multilib_repo_checksums,
            'changelog_txt': multilib_repo_changelog,
            'repo_tag': multilib_repo_tag},

        restricted_repo_name: {
            'enable': restricted_repo,
            'path': restricted_repo_path,
            'mirror_packages': restricted_repo_mirror_packages,
            'mirror_changelog': restricted_repo_mirror_changelog,
            'packages_txt': restricted_repo_packages,
            'checksums_txt': restricted_repo_checksums,
            'changelog_txt': restricted_repo_changelog,
            'repo_tag': restricted_repo_tag},

        gnome_repo_name: {
            'enable': gnome_repo,
            'path': gnome_repo_path,
            'mirror_packages': gnome_repo_mirror_packages,
            'mirror_changelog': gnome_repo_mirror_changelog,
            'packages_txt': gnome_repo_packages,
            'checksums_txt': gnome_repo_checksums,
            'changelog_txt': gnome_repo_changelog,
            'repo_tag': gnome_repo_tag},

        msb_repo_name: {
            'enable': msb_repo,
            'path': msb_repo_path,
            'mirror_packages': msb_repo_mirror_packages,
            'mirror_changelog': msb_repo_mirror_changelog,
            'packages_txt': msb_repo_packages,
            'checksums_txt': msb_repo_checksums,
            'changelog_txt': msb_repo_changelog,
            'repo_tag': msb_repo_tag},

        csb_repo_name: {
            'enable': csb_repo,
            'path': csb_repo_path,
            'mirror_packages': csb_repo_mirror_packages,
            'mirror_changelog': csb_repo_mirror_changelog,
            'packages_txt': csb_repo_packages,
            'checksums_txt': csb_repo_checksums,
            'changelog_txt': csb_repo_changelog,
            'repo_tag': csb_repo_tag},

        conraid_repo_name: {
            'enable': conraid_repo,
            'path': conraid_repo_path,
            'mirror_packages': conraid_repo_mirror_packages,
            'mirror_changelog': conraid_repo_mirror_changelog,
            'packages_txt': conraid_repo_packages,
            'checksums_txt': conraid_repo_checksums,
            'changelog_txt': conraid_repo_changelog,
            'repo_tag': conraid_repo_tag},

        slackdce_repo_name: {
            'enable': slackdce_repo,
            'path': slackdce_repo_path,
            'mirror_packages': slackdce_repo_mirror_packages,
            'mirror_changelog': slackdce_repo_mirror_changelog,
            'packages_txt': slackdce_repo_packages,
            'checksums_txt': slackdce_repo_checksums,
            'changelog_txt': slackdce_repo_changelog,
            'repo_tag': slackdce_repo_tag},

        slackonly_repo_name: {
            'enable': slackonly_repo,
            'path': slackonly_repo_path,
            'mirror_packages': slackonly_repo_mirror_packages,
            'mirror_changelog': slackonly_repo_mirror_changelog,
            'packages_txt': slackonly_repo_packages,
            'checksums_txt': slackonly_repo_checksums,
            'changelog_txt': slackonly_repo_changelog,
            'repo_tag': slackonly_repo_tag},

        salix_repo_name: {
            'enable': salix_repo,
            'path': salix_repo_path,
            'mirror_packages': salix_repo_mirror_packages,
            'mirror_changelog': salix_repo_mirror_changelog,
            'packages_txt': salix_repo_packages,
            'checksums_txt': salix_repo_checksums,
            'changelog_txt': salix_repo_changelog,
            'repo_tag': salix_repo_tag},

        salix_extra_repo_name: {
            'enable': salix_extra_repo,
            'path': salix_extra_repo_path,
            'mirror_packages': salix_extra_repo_mirror_packages,
            'mirror_changelog': salix_extra_repo_mirror_changelog,
            'packages_txt': salix_extra_repo_packages,
            'checksums_txt': salix_extra_repo_checksums,
            'changelog_txt': salix_extra_repo_changelog,
            'repo_tag': salix_extra_repo_tag},

        slackel_repo_name: {
            'enable': slackel_repo,
            'path': slackel_repo_path,
            'mirror_packages': slackel_repo_mirror_packages,
            'mirror_changelog': slackel_repo_mirror_changelog,
            'packages_txt': slackel_repo_packages,
            'checksums_txt': slackel_repo_checksums,
            'changelog_txt': slackel_repo_changelog,
            'repo_tag': slackel_repo_tag},

        slint_repo_name: {
            'enable': slint_repo,
            'path': slint_repo_path,
            'mirror_packages': slint_repo_mirror_packages,
            'mirror_changelog': slint_repo_mirror_changelog,
            'packages_txt': slint_repo_packages,
            'checksums_txt': slint_repo_checksums,
            'changelog_txt': slint_repo_changelog,
            'repo_tag': slint_repo_tag},

        pprkut_repo_name: {
            'enable': pprkut_repo,
            'path': pprkut_repo_path,
            'mirror_packages': pprkut_repo_mirror_packages,
            'mirror_changelog': pprkut_repo_mirror_changelog,
            'packages_txt': pprkut_repo_packages,
            'checksums_txt': pprkut_repo_checksums,
            'changelog_txt': pprkut_repo_changelog,
            'repo_tag': pprkut_repo_tag}
    }
