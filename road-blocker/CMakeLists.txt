cmake_minimum_required(VERSION 3.13)
project(roadblocker)

if (NOT UNIX)
    message(FATAL_ERROR "Only supports UNIX atm :)")
endif ()

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -Wpedantic")

list(APPEND CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake)

# Osmium
find_package(Osmium REQUIRED COMPONENTS xml io)
if(NOT OSMIUM_FOUND)
    message(WARNING "Libosmium not found!\n")
endif()
include_directories(${OSMIUM_INCLUDE_DIRS})
# Pthreads
find_package(Threads REQUIRED)
link_libraries(Threads::Threads)
# Bzip2
include(FindBZip2)
include_directories(${BZIP2_INCLUDE_DIRS})
link_libraries(${BZIP2_LIBRARIES})
# Zlib
find_package(ZLIB)
link_libraries(ZLIB::ZLIB)
# Expat
include(FindEXPAT)
find_package(EXPAT REQUIRED)
include_directories(${EXPAT_INCLUDE_DIRS})
link_libraries(${EXPAT_LIBRARIES})
# Others
include(EnableAddressSanitizer)
include(EnableUndefinedSanitizer)
include(clang-tidy)


add_custom_target(lint)

add_subdirectory(src)
