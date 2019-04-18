# ----------------------------------------------------------------------
# |
# |  BoostBuildImpl.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2019-04-17 15:14:35
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2019
# |  Distributed under the Boost Software License, Version 1.0. See
# |  accompanying file LICENSE_1_0.txt or copy at
# |  http://www.boost.org/LICENSE_1_0.txt.
# |
# ----------------------------------------------------------------------
"""Contains Build and Clean methods that build boost"""

import os
import sys

import CommonEnvironment
from CommonEnvironment.CallOnExit import CallOnExit
from CommonEnvironment import CommandLine
from CommonEnvironment import FileSystem
from CommonEnvironment import Process
from CommonEnvironment.Shell.All import CurrentShell
from CommonEnvironment.StreamDecorator import StreamDecorator

# ----------------------------------------------------------------------
_script_fullpath                            = CommonEnvironment.ThisFullpath()
_script_dir, _script_name                   = os.path.split(_script_fullpath)
#  ----------------------------------------------------------------------

# ----------------------------------------------------------------------
def CreateBuild(boost_root, is_standard_configuration):
    # ----------------------------------------------------------------------
    @CommandLine.EntryPoint
    @CommandLine.Constraints(
        output_stream=None,
    )
    def Build(
        output_stream=sys.stdout,
    ):
        with StreamDecorator(output_stream).DoneManager(
            line_prefix="",
            prefix="\nResults: ",
            suffix="\n",
        ) as dm:
            if is_standard_configuration:
                dm.stream.write("This build is not active with the 'Standard' configuration.\n")
                return dm.result

            # Build b2 (if necessary)
            dm.stream.write("Checking for 'b2'...")
            with dm.stream.DoneManager(
                suffix="\n",
            ) as this_dm:
                b2_filename = os.path.join(boost_root, CurrentShell.CreateExecutableName("b2"))
                if not os.path.isfile(b2_filename):
                    this_dm.stream.write("Building 'b2'...")
                    with this_dm.stream.DoneManager() as build_dm:
                        prev_dir = os.getcwd()
                        os.chdir(boost_root)

                        with CallOnExit(lambda: os.chdir(prev_dir)):
                            if CurrentShell.CategoryName == "Windows":
                                bootstrap_ext = ".bat"
                            else:
                                bootstrap_ext = ".sh"

                            build_dm.result, output = Process.Execute(
                                "bootstrap{}".format(bootstrap_ext),
                            )
                            if build_dm.result != 0:
                                build_dm.stream.write(output)
                                return build_dm.result

            # Build boost (if necessary)
            dm.stream.write("Building boost...")
            with dm.stream.DoneManager() as build_dm:
                prev_dir = os.getcwd()
                os.chdir(boost_root)

                with CallOnExit(lambda: os.chdir(prev_dir)):
                    command_line = 'b2 --build-type=complete stage{architecture} --with-serialization'.format(
                        architecture=" address-model=64" if os.getenv(
                            "DEVELOPMENT_ENVIRONMENT_CPP_ARCHITECTURE",
                        ) == "x64" else "",
                    )

                    build_dm.result = Process.Execute(command_line, build_dm.stream)
                    if build_dm.result != 0:
                        return build_dm.result

            return dm.result

    # ----------------------------------------------------------------------

    return Build


# ----------------------------------------------------------------------
def CreateClean(boost_root):
    # ----------------------------------------------------------------------
    @CommandLine.EntryPoint
    @CommandLine.Constraints(
        output_stream=None,
    )
    def Clean(
        force=False,
        output_stream=sys.stdout,
    ):
        with StreamDecorator(output_stream).DoneManager(
            line_prefix="",
            prefix="\nResults: ",
            suffix="\n",
        ) as dm:
            stage_dir = os.path.join(boost_root, "stage")
            if not os.path.isdir(stage_dir):
                dm.stream.write("There is nothing to remove.\n")
                return dm.result

            if not force:
                dm.stream.write(
                    "Call this method with the '/force' flag to remove the staging directory.\n",
                )
                return dm.result

            dm.stream.write("Removing '{}'...".format(stage_dir))
            with dm.stream.DoneManager():
                FileSystem.RemoveTree(stage_dir)

            bin_dir = os.path.join(boost_root, "bin.v2")
            if os.path.isdir(bin_dir):
                dm.stream.write("Removing '{}'...".format(bin_dir))
                FileSystem.RemoveTree(bin_dir)

            return dm.result

    # ----------------------------------------------------------------------

    return Clean
