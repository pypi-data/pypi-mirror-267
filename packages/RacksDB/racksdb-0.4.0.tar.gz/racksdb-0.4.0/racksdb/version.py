# Copyright (c) 2022-2023 Rackslab
#
# This file is part of RacksDB.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pkg_resources


def get_version():
    return pkg_resources.get_distribution("racksdb").version
