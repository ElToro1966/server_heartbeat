Add tests

Configuration Test:
Ensure that the configuration is read correctly and has the expected values.

Logging Test:
Verify that the logging setup and log messages are working as expected. You can use a mock logger to capture log messages and then check if the messages are correct.

HTTP Server Test:
Test the HTTP server class to ensure it correctly initializes with the provided server configurations.

Logger Rotation Test:
Check if the log file is rotating correctly based on the specified size and backup count.

Server Status Logging Test:
Test the log_status function to ensure it logs the server status correctly.

Fail Check Test:
Test the fail_check function to ensure it logs the appropriate messages when a server is not reachable.

Server Up Check Test:
Test the server_up_check function to ensure it logs the server status and triggers the fail check when necessary.

Main Function Test:
Check the main function to ensure it creates tasks for all servers and gathers them correctly.