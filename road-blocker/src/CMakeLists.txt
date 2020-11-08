set(ROADBLOCKER_SOURCES
    # read-progress-example.cpp
    main.cpp
    )

add_library(roadblocker_core ${ROADBLOCKER_SOURCES} ${HEADER_FILES})
target_include_directories(roadblocker_core PUBLIC ${CMAKE_SOURCE_DIR})

add_clang_tidy_target(lint_roadblocker_core ${ROADBLOCKER_SOURCES})
add_dependencies(lint lint_roadblocker_core)

add_executable(roadblocker main.cpp)
# add_executable(roadblocker read-progress-example.cpp)

target_link_libraries(roadblocker PUBLIC roadblocker_core)
