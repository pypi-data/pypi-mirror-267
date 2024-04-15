import copy
import os
import socket
import json
import sys
import threading
from threading import Thread
from .manager import QYAMLDB
import logging
from cryptography.fernet import Fernet

READ_COMMANDS = ['$query']
WRITE_COMMANDS = ['$insert', '$insert_many', '$update', '$update_many', '$delete'
    , '$delete_many', '$del_many', '$del', '$create_table']


# Declare a class DaemonError to denote that daemon cannot start
class DaemonError(Exception):
    pass


class DatabaseDaemonBase:
    def __init__(self, dbpath, key, encrypted, encryption_key=None, log_file="daemon.log"):
        self.db_path = dbpath
        self.key_path = key
        self.encrypted = encrypted
        self.encryption_key = encryption_key
        self.fernet = Fernet(encryption_key) if encryption_key else None
        self.database: QYAMLDB = None
        self.running = False

        # Setup logging
        self.logger = logging.getLogger('DatabaseDaemon')
        self.logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

        self.logger.info("DatabaseDaemon initialized.")

    def _encrypt_message(self, message):
        if self.fernet:
            encrypted_message = self.fernet.encrypt(message.encode('utf-8'))
            self.logger.debug("Message encrypted.")
            return encrypted_message
        return message.encode('utf-8')

    def _decrypt_message(self, message):
        if self.fernet:
            decrypted_message = self.fernet.decrypt(message).decode('utf-8')
            self.logger.debug("Message decrypted.")
            return decrypted_message
        return message.decode('utf-8')

    def _setup_db(self):
        self.logger.info("Setting up database ...")
        print("Setting up database ....")
        self.database = QYAMLDB(self.db_path, self.key_path, self.encrypted)
        try:
            self.database.load_db()
            self.logger.info("Database loaded successfully.")
            print("Database Loaded Successfully")
        except Exception as e:
            self.logger.error(f"Initialization of the database failed: {e}")
            raise Exception(f"Initialization of the database failed: {e}")

    def start(self):
        self.running = True
        self._setup_db()
        self.logger.info("Database Daemon started.")

    def stop(self):
        self.running = False
        self.logger.info("Database Daemon stopped.")

    def _process_command(self, command):
        self.logger.info(f"Processing command: {command}")
        # Processing logic here...

    def run(self):
        self.logger.info("Daemon running.")
        # This should be implemented in subclass
        raise NotImplementedError("Daemon run loop not implemented.")


class DataBaseIPCDaemon(DatabaseDaemonBase):
    """A Database Daemon that listens to DB commands on separate thread
    Note: this class may not be thread safe and also this does not prevent any race condition.
    Use this when you have only one Thread accessing this,"""

    def __init__(self, dbpath, key, encrypted, socket_path, encryption_key=None, log_file="ipc_daemon.log"):
        # Initialize the base class with all required parameters
        super().__init__(dbpath=dbpath, key=key, encrypted=encrypted, encryption_key=encryption_key,
                         log_file=log_file)
        self.server_socket = None
        self.socket_path = socket_path

        self.logger.info("DataBaseIPCDaemon initialized.")

    def start(self):
        """
        Start the daemon by setting up the server socket and listening for incoming connections.
        Make sure to run this under a for your application
        """

        # connect,bind and listen in unix socket
        try:
            os.unlink(self.socket_path)
        except OSError:
            if os.path.exists(self.socket_path):
                raise DaemonError('Socket path exists')
        self.server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self._setup_db()
        try:
            self.server_socket.bind(self.socket_path)
            self.server_socket.listen(5)
            try:
                while True:
                    # Accept client connection
                    connection, address = self.server_socket.accept()
                    self.logger.info(" A Client has been connected")
                    # launch a separate thread handling client
                    ct = Thread(target=self._handle_client, args=(connection, address,))
                    ct.start()
            except KeyboardInterrupt:
                sys.exit(0)
            # Print
        except OSError:
            print(f"Socket {self.socket_path} already in use. Use different path")
        except KeyboardInterrupt:
            self.server_socket.close()
        finally:
            self.server_socket.close()

    def _handle_client(self, client_socket, mask=None):
        """
        Handle the client connection by receiving, processing, and sending messages.

        Parameters:
        - client_socket: the socket object for the client connection
        - mask: optional parameter to be used for handling the client (default is None)

        Returns:
        This function does not return anything.
        """
        # First, receive the length of the incoming message
        data_length = client_socket.recv(8)

        if not data_length:
            print("Connection closed by the client.")
            self.logger.info("Connection closed by the client.")

            return

        # Convert the length to an integer
        message_length = int(data_length.decode('utf-8'))
        self.logger.info(f"Received message length: {message_length}")
        # Send ack after receiving length to signal
        client_socket.send("ACK".encode('utf-8'))
        # Now receive the rest of the message based on the length
        data = b''
        while len(data) < message_length:
            packet = client_socket.recv(message_length - len(data))
            if not packet:
                self.logger.info("Client closed connection.")
                client_socket.close()
                return
            data += packet
        print('Receive data: ', data.decode('utf-8'))
        # Now that the complete message has been received, proceed with decryption and processing
        try:
            decrypted_command = self._decrypt_message(data)
            command = json.loads(decrypted_command)
            response = self._process_command(command)
            encrypted_response = self._encrypt_message(json.dumps(response))

            # send the length of data
            response_length = str(len(encrypted_response))
            client_socket.send(response_length.encode('utf-8'))
            # wait for acknowledgement from the client.
            ack = client_socket.recv(1024).decode('utf-8')
            self.logger.info(f"Received acknowledgement from client: {ack}")
            # Send actual response
            client_socket.send(encrypted_response)

        except Exception as e:
            print(f"Error processing command: {e}")
            error_response = self._encrypt_message(json.dumps({'error': str(e)}))
            client_socket.send(len(error_response).to_bytes(4, byteorder='big') + error_response)

    def _process_command(self, command):
        """Process the received command."""

        status = self.database.begin_transaction(command)
        return status

    def stop(self):
        """
        Stops the daemon. Closes the server socket.
        """
        # Close the connection
        self.running = False
        self.server_socket.close()


class DatabaseDaemonIPCThreadedSafe(DataBaseIPCDaemon):
    """

    [WIP]
    You are not recommended to use this class since this is under construction.
    """

    def __init__(self, dbpath, key, encrypted, socket_path, encryption_key=None, log_file="ipc_daemon.log",
                 max_readers=None):
        super().__init__(dbpath, key, encrypted, socket_path, encryption_key, log_file)
        self.max_readers = max_readers
        self.readers_lock = threading.Lock()
        self.writers_lock = threading.Lock()
        self.readers_count = 0

    def _handle_client(self, client_socket, mask=None):
        while True:
            try:
                data = client_socket.recv(8)
                if not data:
                    self.logger.info('Client Disconnected')
                    break
                response = None  # Initially, Response is set to None
                length = int.from_bytes(data, byteorder='big')  # Get the length of data
                client_socket.send("ACK".encode('utf-8'))  # Signal the client to send data by sending a 'ACK' Message
                data = client_socket.recv(length)  # Receive the data from the Client
                if data is None:
                    self.logger.info('Connection closed by the client')  # if No data found, Client can be terminated.
                    break

                original_data = json.loads(data.decode('utf-8'))  # Original Data as json
                transaction_data = original_data.get('operations', None)  # get only the operations for now.
                on_error_strategy = original_data.get('$on_error',
                                                      'rollback')  # Get the error strategy to handle errors\
                invalid_command_strategy = original_data.get('$on_invalid_command', 'rollback')
                if transaction_data is None:
                    client_socket.send("No Command to Process".encode('utf-8'))
                else:
                    backup_table = copy.deepcopy(self.database.tables)  # Begin transaction
                    transaction_report = {
                        'successful_operations': 0,
                        'failed_operation': 0,
                        'list_of_failed_operations': [],
                        'list_of_errors': []
                    }
                    for transaction in transaction_data:
                        results = None
                        if transaction['type'] in READ_COMMANDS:
                            results = self._handle_read(transaction)
                        elif transaction['type'] in WRITE_COMMANDS:
                            results = self._handle_write(transaction)
                        else:
                            results = {'status': 'error', 'message': 'Invalid Command'}  # invalid command error

                        if results['status'] == 'error':
                            if on_error_strategy == 'rollback':
                                self.database.tables = backup_table
                                transaction_report['failed_operation'] += len(transaction_data)
                                transaction_report['list_of_errors'].append(str(results['result_data']))
                                return transaction_report
                            if on_error_strategy in ('continue', 'break'):
                                transaction_report['failed_operation'] += 1
                                transaction_report['list_of_errors'].append(str(results['result_data']))
                                if on_error_strategy == 'break':
                                    break

                        transaction_report['successful_operations'] += 1
                    # Send Results
                    client_socket.send(json.dumps(transaction_report).encode('utf-8'))
            except Exception as e:
                self.logger.error(f'Exception while handling the client: {e}')

    def _handle_write(self, data):

        with self.writers_lock:
            result = self._process_command(data)

        return result

    def _handle_read(self, data):
        with self.readers_lock:
            self.readers_count += 1
            if self.readers_count == 1:
                self.writers_lock.acquire()

        result = self._process_command(data)

        with self.readers_lock:
            self.readers_count -= 1
            if self.readers_count == 0:
                self.writers_lock.release()
        return result

    def _process_command(self, command):

        try:
            return {'status': 'success', 'result_data': self.database.execute_command(command)}
        except Exception as e:
            return {'status': 'error', 'result_data': str(e)}
