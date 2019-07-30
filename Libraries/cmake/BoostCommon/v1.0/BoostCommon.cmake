# ----------------------------------------------------------------------
# |  Define Boost (Note that this relies on variables set in CppCommon)

option(
    BoostCommon_HEADER_ONLY
    "If `ON`, Boost libraries are not required to exist."
    "OFF"
)

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
set(Boost_DETAILED_FAILURE_MSG ON)

set(Boost_USE_STATIC_RUNTIME ${CppCommon_STATIC_CRT})
set(Boost_USE_STATIC_LIBS ${CppCommon_STATIC_CRT})
set(Boost_USE_MULTITHREADED ON)

set(Boost_NO_SYSTEM_PATHS ON)

if(NOT CMAKE_CXX_COMPILER_ARCHITECTURE_ID)
    if("$ENV{DEVELOPMENT_ENVIRONMENT_CPP_ARCHITECTURE}" STREQUAL "x64")
        set(CMAKE_CXX_COMPILER_ARCHITECTURE_ID "x64")
    elseif("$ENV{DEVELOPMENT_ENVIRONMENT_CPP_ARCHITECTURE}" STREQUAL "x86")
        set(CMAKE_CXX_COMPILER_ARCHITECTURE_ID "X86")
    else()
        message(FATAL_ERROR "'$ENV{DEVELOPMENT_ENVIRONMENT_CPP_ARCHITECTURE}' is not a supported architecture")
    endif()
endif()

if(DEFINED MSVC_VERSION)
    if(MSVC_VERSION LESS_EQUAL 1916)
        set(Boost_COMPILER "-vc141")
    elseif(MSVC_VERSION LESS_EQUAL 1920)
        set(Boost_COMPILER "-vc142")
    else()
        MESSAGE(FATAL_ERROR "'${MSVC_VERSION}' appears to be a new version of the compiler. Please manually add the appropriate compiler version here.")
    endif()
endif()

set(_components
    iostreams
    regex
    serialization
)

if(BoostCommon_HEADER_ONLY)
    find_package(Boost
        $ENV{DEVELOPMENT_ENVIRONMENT_BOOST_VERSION}
        COMPONENTS
            ${_components}
    )

else()
    find_package(Boost
        $ENV{DEVELOPMENT_ENVIRONMENT_BOOST_VERSION}
        REQUIRED
        COMPONENTS
            ${_components}
    )

endif()
