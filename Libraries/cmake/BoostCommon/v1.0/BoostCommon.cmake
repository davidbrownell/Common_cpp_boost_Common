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

# FindBoost.cmake has a difficult time detecting the clang compiler when it is 
# emulating MSVC. Explicitly set the compiler if that is the case.
get_filename_component(_compiler_basename "${CMAKE_CXX_COMPILER}" NAME)

if(CMAKE_CXX_COMPILER_ID MATCHES Clang AND _compiler_basename MATCHES "clang-cl.exe")
    if(MSVC_VERSION LESS_EQUAL 1916)
        set(Boost_COMPILER "-vc141")
    elseif(MSVC_VERSION LESS_EQUAL 1920)
        set(Boost_COMPILER "-vc142")
    else()
        MESSAGE(FATAL_ERROR "'${MSVC_VERSION}' appears to be a new version of the compiler. Please manually add the appropriate compiler version here.")
    endif()
endif()

find_package(Boost $ENV{DEVELOPMENT_ENVIRONMENT_BOOST_VERSION} COMPONENTS 
    serialization
)
