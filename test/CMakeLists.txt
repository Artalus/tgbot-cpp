set(TEST_SRC_LIST
	main.cpp
	tgbot/net/Url.cpp
	tgbot/net/HttpParser.cpp
	tgbot/tools/StringTools.cpp
)

set(TEST_NAME ${PROJECT_NAME}_test)

add_executable(${TEST_NAME} ${TEST_SRC_LIST})
target_include_directories(${TEST_NAME} PRIVATE ${PROJECT_SOURCE_DIR}/test)
target_link_libraries(${TEST_NAME}
	TgBot
	CONAN_PKG::boost_test
)
add_test(${TEST_NAME} ${TEST_NAME})
