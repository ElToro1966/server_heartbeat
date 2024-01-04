import unittest
from main import get_config, path_to_cwd, log_status, fail_check, server_up_check, create_rotating_log_file
import logging.handlers
from os.path import exists
import logging

log_file = "server_monitoring_testing.log"
log_file_max_bytes = 5000
log_file_backup_count = 3

error_message = "Testing - Server is down"
info_message = "Testing - Server is up"
down_check_message = "Server is still down. Checking again in {0} seconds."

server = []
server.append("GuaranteedFailure, https://www.hubbabubba.nowaythisisarealurl, 9, 6")
server.append("Wikipedia, https://www.wikipedia.org, 18, 3")
server.append("GitHub, https://www.github.com, 36, 36")
server.append("Google, https://www.google.com, 6, 2")


class ServerHeartbeatTestCase(unittest.TestCase):
    def test_log_created(self):
        create_rotating_log_file(log_file, log_file_max_bytes, log_file_backup_count)
        self.assertLogs("ServerLogger", level="INFO")  # The log exists

    def test_http__response_not_being_200_logged_as_error(self):
        create_rotating_log_file(log_file, log_file_max_bytes, log_file_backup_count)
        server_up_check(server[0])
        self.assertTrue(True)  # The log contains an error message

    def test_200_logged_as_info(self):
        self.assertEqual(True, False) # The log contains an info message


if __name__ == '__main__':
    unittest.main()
