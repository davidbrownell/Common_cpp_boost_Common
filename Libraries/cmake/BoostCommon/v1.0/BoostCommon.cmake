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

if(MSVC_VERSION LESS_EQUAL 1916)
    set(Boost_COMPILER "-vc141")
elseif(MSVC_VERSION LESS_EQUAL 1920)
    set(Boost_COMPILER "-vc142")
else()
    MESSAGE(FATAL_ERROR "'${MSVC_VERSION}' appears to be a new version of the compiler. Please manually add the appropriate compiler version here.")
endif()

find_package(Boost 
    $ENV{DEVELOPMENT_ENVIRONMENT_BOOST_VERSION} 
    COMPONENTS
        iostreams
        regex
        serialization
)
