@REM Builds boost libs using bjam.
@echo off

if not EXIST "%DEVELOPMENT_ENVIRONMENT_BOOST_ROOT%\b2.exe" (
    echo ----------------------------------------------------------------------
    echo ^|
    echo ^|  Building bjam
    echo ^|
    echo ----------------------------------------------------------------------
    
    pushd "%DEVELOPMENT_ENVIRONMENT_BOOST_ROOT%"
    call bootstrap.bat
    popd
)

echo ----------------------------------------------------------------------
echo ^|
echo ^|  Building boost
echo ^|
echo ----------------------------------------------------------------------

if "%DEVELOPMENT_ENVIRONMENT_CPP_ARCHITECTURE%"=="x64" (
    set _address_model_arg="address-model=64"
    goto :post_address_model_arg
)
set _address_model_arg=""
goto :post_address_model_arg

:post_address_model_arg

pushd "%DEVELOPMENT_ENVIRONMENT_BOOST_ROOT%"
b2 --build-type=complete stage %_address_model_arg% --with-serialization
popd

set _address_model_arg=
