cmake_minimum_required(VERSION 3.10)
project(AITradingBot)

# Locate Arrow using its CMake configuration (installed in $HOME/.local)
find_package(Arrow CONFIG REQUIRED PATHS $ENV{HOME}/.local/lib/cmake/Arrow)

# Locate libcurl (provided by the system via pkg in Termux)
find_package(CURL REQUIRED)

# Create the executable
add_executable(ai_trading_bot main.cpp)

# Link the executable with Arrow (shared library) and libcurl.
target_link_libraries(ai_trading_bot PRIVATE Arrow::arrow_shared CURL::libcurl)
