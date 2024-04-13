#!/usr/bin/python3
# -*- coding: utf-8 -*-

from pathlib import Path

from slpkg.configs import Configs
from slpkg.views.views import View
from slpkg.utilities import Utilities
from slpkg.downloader import Downloader
from slpkg.install_data import InstallData
from slpkg.repositories import Repositories
from slpkg.multi_process import MultiProcess
from slpkg.check_updates import CheckUpdates
from slpkg.sbos.sbo_generate import SBoGenerate


class UpdateRepositories(Configs):
    """ Updates the local repositories and install the data
        into the database.
    """

    def __init__(self, flags: list, repository: str):
        super(Configs, self).__init__()
        self.flags: list = flags
        self.repository: str = repository

        self.view = View(flags)
        self.multi_process = MultiProcess(flags)
        self.repos = Repositories()
        self.utils = Utilities()
        self.data = InstallData()
        self.generate = SBoGenerate()
        self.check_updates = CheckUpdates(flags, repository)
        self.download = Downloader(flags)

        self.repos_for_update: dict = {}

        self.option_for_repository: bool = self.utils.is_option(
            ('-o', '--repository'), flags)

    def repositories(self) -> None:
        self.repos_for_update: dict = self.check_updates.updates()
        self.update_the_repositories()

    def update_the_repositories(self) -> None:
        if not any(list(self.repos_for_update.values())):
            self.view.question(message='Do you want to force update?')
            # Force update the repositories.
            for repo in self.repos_for_update:
                self.repos_for_update[repo] = True

        if self.option_for_repository:
            self.view_downloading_message(self.repository)
            if self.repository in [self.repos.sbo_repo_name, self.repos.ponce_repo_name]:
                self.update_slackbuild_repos(self.repository)
            else:
                self.update_binary_repos(self.repository)
        else:
            for repo, update in self.repos_for_update.items():
                if update:
                    self.view_downloading_message(repo)
                    if repo in [self.repos.sbo_repo_name, self.repos.ponce_repo_name]:
                        self.update_slackbuild_repos(repo)
                    else:
                        self.update_binary_repos(repo)

    def view_downloading_message(self, repo: str) -> None:
        print(f"Syncing with the repository '{self.green}{repo}{self.endc}', please wait...\n")

    def update_binary_repos(self, repo: str) -> None:
        urls: dict = {}

        install: dict = {
            self.repos.slack_repo_name: self.data.install_slack_data,
            self.repos.slack_extra_repo_name: self.data.install_slack_extra_data,
            self.repos.slack_patches_repo_name: self.data.install_slack_patches_data,
            self.repos.alien_repo_name: self.data.install_alien_data,
            self.repos.multilib_repo_name: self.data.install_multilib_data,
            self.repos.restricted_repo_name: self.data.install_restricted_data,
            self.repos.gnome_repo_name: self.data.install_gnome_data,
            self.repos.msb_repo_name: self.data.install_msb_data,
            self.repos.csb_repo_name: self.data.install_csb_data,
            self.repos.conraid_repo_name: self.data.install_conraid_data,
            self.repos.slackdce_repo_name: self.data.install_slackdce_data,
            self.repos.slackonly_repo_name: self.data.install_slackonly_data,
            self.repos.salix_repo_name: self.data.install_salix_data,
            self.repos.salix_extra_repo_name: self.data.install_salix_extra_data,
            self.repos.slackel_repo_name: self.data.install_slackel_data,
            self.repos.slint_repo_name: self.data.install_slint_data,
            self.repos.pprkut_repo_name: self.data.install_pprkut_data
        }

        self.utils.create_directory(self.repos.repositories[repo]['path'])
        self.utils.remove_file_if_exists(self.repos.repositories[repo]['path'], self.repos.repositories[repo]['changelog_txt'])
        self.utils.remove_file_if_exists(self.repos.repositories[repo]['path'], self.repos.repositories[repo]['packages_txt'])
        self.utils.remove_file_if_exists(self.repos.repositories[repo]['path'], self.repos.repositories[repo]['checksums_txt'])

        changelog: str = f"{self.repos.repositories[repo]['mirror_changelog']}{self.repos.repositories[repo]['changelog_txt']}"
        packages: str = f"{self.repos.repositories[repo]['mirror_packages']}{self.repos.repositories[repo]['packages_txt']}"
        checksums: str = f"{self.repos.repositories[repo]['mirror_packages']}{self.repos.repositories[repo]['checksums_txt']}"

        urls[repo] = ((changelog, packages, checksums), self.repos.repositories[repo]['path'])

        self.download.download(urls)

        install[repo]()

    def update_slackbuild_repos(self, repo: str) -> None:
        """ Update the slackbuild repositories. """
        self.utils.create_directory(self.repos.repositories[repo]['path'])
        self.utils.remove_file_if_exists(self.repos.repositories[repo]['path'],
                                         self.repos.repositories[repo]['slackbuilds_txt'])
        self.utils.remove_file_if_exists(self.repos.repositories[repo]['path'],
                                         self.repos.repositories[repo]['changelog_txt'])

        lftp_command: str = (f"lftp {self.lftp_mirror_options} {self.repos.repositories[repo]['mirror_packages']} "
                             f"{self.repos.repositories[repo]['path']}")

        self.multi_process.process(lftp_command)

        # It checks if there is a SLACKBUILDS.TXT file, otherwise it going to create one.
        if not Path(self.repos.repositories[repo]['path'],
                    self.repos.repositories[repo]['slackbuilds_txt']).is_file():
            self.generate.slackbuild_file(self.repos.repositories[repo]['path'],
                                          self.repos.repositories[repo]['slackbuilds_txt'])

        install: dict = {
            self.repos.sbo_repo_name: self.data.install_sbo_data,
            self.repos.ponce_repo_name: self.data.install_ponce_data
        }

        install[repo]()
