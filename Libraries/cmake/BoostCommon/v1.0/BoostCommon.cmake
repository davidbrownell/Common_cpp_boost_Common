# ----------------------------------------------------------------------
# |  Define Boost (Note that this relies on variables set in CppCommon)
foreach(_env_var_name IN ITEMS
    DEVELOPMENT_ENVIRONMENT_BOOST_VERSION
    DEVELOPMENT_ENVIRONMENT_BOOST_VERSION_SHORT
    DEVELOPMENT_ENVIRONMENT_BOOST_ROOT
)
    set(_temp "$ENV{${_env_var_name}}")
    if(NOT _temp)
        message(FATAL_ERROR "The environment variable '${_env_var_name}' must be defined")
    endif()
endforeach()

set(BOOST_ROOT "$ENV{DEVELOPMENT_ENVIRONMENT_BOOST_ROOT}")

set(Boost_ADDITIONAL_VERSIONS $ENV{DEVELOPMENT_ENVIRONMENT_BOOST_VERSION} $ENV{DEVELOPMENT_ENVIRONMENT_BOOST_VERSION_SHORT})

set(Boost_DEBUG ${CppCommon_CMAKE_DEBUG_OUTPUT})
set(Boost_USE_STATIC_RUNTIME ${CppCommon_STATIC_CRT})
set(Boost_USE_STATIC_LIBS ${CppCommon_STATIC_CRT})
set(Boost_USE_MULTITHREADED ON)

find_package(Boost $ENV{DEVELOPMENT_ENVIRONMENT_BOOST_VERSION} COMPONENTS 
    serialization
)

# ----------------------------------------------------------------------
# |  Define BoostCommon
set(_boost_common_version "1.0")
get_filename_component(_boost_common_root "${CMAKE_CURRENT_LIST_DIR}/../../../C++/BoostCommon/v${_boost_common_version}" ABSOLUTE)

add_library(BoostCommon INTERFACE)

target_include_directories(BoostCommon 
    INTERFACE
        "${_boost_common_root}"
)

file(GLOB _headers "${_boost_common_root}/**/*")

target_sources(BoostCommon
    INTERFACE
        ${_headers}
)
