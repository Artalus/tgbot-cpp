cmake_minimum_required(VERSION 2.8.4)
project(TgBot)
set(CMAKE_CXX_STANDARD 11)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)
set(CMAKE_MODULE_PATH ${CONAN_CMAKE_MODULE_PATH} ${CMAKE_MODULE_PATH})


### options
option(ENABLE_TESTS "Set to ON to enable building of tests" OFF)
option(BUILD_SHARED_LIBS "Build tgbot-cpp shared/static library." OFF)

### sources
set(SRC_LIST
	src/Api.cpp
	src/TgTypeParser.cpp
	src/TgException.cpp
	src/EventHandler.cpp
	src/net/Url.cpp
	src/net/HttpClient.cpp
	src/net/HttpParser.cpp
	src/net/TgLongPoll.cpp
	src/tools/StringTools.cpp
	src/tools/FileTools.cpp
	src/types/InlineQueryResult.cpp
	src/types/InputFile.cpp
)


set(LIB_LIST
	CONAN_PKG::boost_system
	CONAN_PKG::boost_property_tree
	CONAN_PKG::boost_asio
	CONAN_PKG::OpenSSL
)
set(Boost_USE_MULTITHREADED ON)
if (ENABLE_TESTS)
	set(LIB_LIST ${LIB_LIST} CONAN_PKG::boost_test)
endif()


### building project
add_library(${PROJECT_NAME} ${SRC_LIST})
if(UNIX)
	target_compile_options(${PROJECT_NAME} PRIVATE "-Wall")
elseif(MSVC)
	target_compile_options(${PROJECT_NAME} PRIVATE "/W4")
endif()
target_include_directories(${PROJECT_NAME} PUBLIC include)
target_link_libraries(${PROJECT_NAME} ${LIB_LIST})
install(TARGETS ${PROJECT_NAME} DESTINATION lib)
install(DIRECTORY include/ DESTINATION include)

### tests
if (ENABLE_TESTS)
	message(STATUS "Building of tests is enabled")
	enable_testing()
	add_subdirectory(test)
endif()
