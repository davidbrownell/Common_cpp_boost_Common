# ----------------------------------------------------------------------
# |
# |  BoostBuildImpl.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2019-04-17 15:14:35
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2019-22
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
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
def CreateBuild(boost_root, is_standard_configuration):
    boost_libs = ["iostreams", "regex", "serialization"]

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
                dm.stream.write(
                    "This build is not active with the 'standard' configuration.\n",
                )
                return dm.result

            # Build b2 (if necessary)
            dm.stream.write("Checking for 'b2'...")
            with dm.stream.DoneManager(
                suffix="\n",
            ) as this_dm:
                b2_filename = os.path.join(
                    boost_root,
                    CurrentShell.CreateExecutableName("b2"),
                )
                if not os.path.isfile(b2_filename):
                    this_dm.stream.write("Building 'b2'...")
                    with this_dm.stream.DoneManager() as build_dm:
                        prev_dir = os.getcwd()
                        os.chdir(boost_root)

                        with CallOnExit(lambda: os.chdir(prev_dir)):
                            if CurrentShell.CategoryName == "Windows":
                                bootstrap_name = "bootstrap.bat"
                                command_line = bootstrap_name

                            else:
                                bootstrap_name = "bootstrap.sh"

                                # Manually set the toolset
                                compiler_name = os.getenv(
                                    "DEVELOPMENT_ENVIRONMENT_CPP_COMPILER_NAME",
                                ).lower()

                                if "clang" in compiler_name:
                                    toolset = "clang"
                                else:
                                    build_dm.stream.write(
                                        "ERROR: '{}' is not a recognized compiler.\n".format(
                                            compiler_name,
                                        ),
                                    )
                                    build_dm.result = -1

                                    return build_dm.result

                                command_line = "./{} --with-toolset={}".format(
                                    bootstrap_name,
                                    toolset,
                                )

                            for filename in [
                                bootstrap_name,
                                os.path.join("tools", "build", "bootstrap.sh"),
                                os.path.join(
                                    "tools",
                                    "build",
                                    "src",
                                    "engine",
                                    "build.sh",
                                ),
                            ]:
                                assert os.path.isfile(filename), filename

                                CurrentShell.MakeFileExecutable(filename)

                            build_dm.result, output = Process.Execute(command_line)
                            if build_dm.result != 0:
                                build_dm.stream.write(output)
                                return build_dm.result

            # Build boost (if necessary)
            dm.stream.write("Building boost...")
            with dm.stream.DoneManager() as build_dm:
                prev_dir = os.getcwd()
                os.chdir(boost_root)

                architecture = os.getenv("DEVELOPMENT_ENVIRONMENT_CPP_ARCHITECTURE")

                with CallOnExit(lambda: os.chdir(prev_dir)):
                    command_line = "b2 --build-type=complete --layout=versioned --build-dir=build/{architecture} --hash stage address-model={architecture} {libs}".format(
                        architecture="64" if architecture == "x64" else "32",
                        libs=" ".join(
                            ["--with-{}".format(lib_name) for lib_name in boost_libs],
                        ),
                    )

                    if CurrentShell.CategoryName != "Windows":
                        # TODO: Enable ASLR
                        #   command_line = './{} variant=release cxxflags="-fPIC -fpie" linkflags="-pie"'.format(command_line)

                        command_line = "./{} ".format(command_line)

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
            for subdir in ["stage", "build"]:
                this_dir = os.path.join(boost_root, subdir)
                if not os.path.isdir(this_dir):
                    continue

                if not force:
                    dm.stream.write(
                        "Call this method with the '/force' flag to remove '{}'.\n".format(
                            this_dir,
                        ),
                    )
                    continue

                dm.stream.write("Removing '{}'...".format(this_dir))
                with dm.stream.DoneManager():
                    FileSystem.RemoveTree(this_dir)

            return dm.result

    # ----------------------------------------------------------------------

    return Clean
