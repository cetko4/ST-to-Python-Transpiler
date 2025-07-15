import hashlib
import os

class UserCreate:
    """
    Synchronous simulation of ArUserCreate function block.
    Operation completes immediately in .call() when Execute is True.
    """

    created_users = set()

    def __init__(self):
        self.Execute = False
        self.UserName = ""
        self.Done = False
        self.Busy = False
        self.Error = False
        self.ErrorID = 0

    def call(self):
        if self.Execute:
            self.Busy = True

            # Check parameters immediately
            if not self.UserName.strip():
                self.Error = True
                self.ErrorID = -1070585894
                self.Done = False
            elif self.UserName in UserCreate.created_users:
                self.Error = True
                self.ErrorID = -1070585893
                self.Done = False
            else:
                # Success: create user immediately
                UserCreate.created_users.add(self.UserName)
                self.Done = True
                self.Error = False
                self.ErrorID = 0

            self.Busy = False
            self.Execute = False
        else:
            # Reset status when not executing
            self.Done = False
            self.Busy = False
            self.Error = False
            self.ErrorID = 0



class UserSetPassword:
    """
    Synchronous simulation of ArUserSetPassword function block.
    Sets password immediately when call() is invoked with Execute=True.
    """

    # Simulated user database: username -> hashed password
    _user_db = {}  # dict: username -> hashed_password (hex string)

    # Error codes
    ERR_PARAMETER = -1070585894
    ERR_DOES_NOT_EXIST = -1070585892
    ERR_INTERNAL = -1070585889
    ERR_MEMORY = -1070585890

    def __init__(self):
        self.Execute = False
        self.UserName = ""
        self.Password = ""  # plain text password input
        self.Done = False
        self.Busy = False
        self.Error = False
        self.ErrorID = 0

    def call(self):
        if self.Execute:
            self.Busy = True

            # Validate parameters
            if not self.UserName.strip() or not self.Password:
                self.Error = True
                self.ErrorID = self.ERR_PARAMETER
                self.Done = False

            # Check if user exists
            elif self.UserName not in UserCreate.created_users:
                self.Error = True
                self.ErrorID = self.ERR_DOES_NOT_EXIST
                self.Done = False

            else:
                try:
                    # Salt and hash the password
                    # Salt: 6 random bytes
                    salt = os.urandom(6)
                    salted_password = salt + self.Password.encode('utf-8')
                    hashed = hashlib.sha256(salted_password).hexdigest()

                    # Store password as hex string with salt prefix
                    # Format: hex(salt) + hashed password hex string
                    salt_hex = salt.hex()
                    stored_password = salt_hex + hashed

                    # Save hashed password to user database
                    self._user_db[self.UserName] = stored_password

                    self.Done = True
                    self.Error = False
                    self.ErrorID = 0

                except MemoryError:
                    self.Error = True
                    self.ErrorID = self.ERR_MEMORY
                    self.Done = False

                except Exception:
                    self.Error = True
                    self.ErrorID = self.ERR_INTERNAL
                    self.Done = False

            self.Busy = False
            self.Execute = False

        else:
            # Reset output flags if not executing
            self.Done = False
            self.Busy = False
            self.Error = False
            self.ErrorID = 0


class UserCreateRole:
    """
    Synchronous simulation of ArUserCreateRole function block.
    Creates a role immediately in .call() when Execute is True.
    """

    created_roles = set()

    # Error codes
    ERR_PARAMETER = -1070585894
    ERR_ALREADY_EXISTS = -1070585893
    ERR_INTERNAL = -1070585889

    def __init__(self):
        self.Execute = False
        self.RoleName = ""
        self.Done = False
        self.Busy = False
        self.Error = False
        self.ErrorID = 0

    def call(self):
        if self.Execute:
            self.Busy = True

            # Check parameters immediately
            if not self.RoleName.strip():
                self.Error = True
                self.ErrorID = self.ERR_PARAMETER
                self.Done = False

            elif self.RoleName in UserCreateRole.created_roles:
                self.Error = True
                self.ErrorID = self.ERR_ALREADY_EXISTS
                self.Done = False

            else:
                try:
                    # Success: create role immediately
                    UserCreateRole.created_roles.add(self.RoleName)
                    self.Done = True
                    self.Error = False
                    self.ErrorID = 0

                except Exception:
                    self.Error = True
                    self.ErrorID = self.ERR_INTERNAL
                    self.Done = False

            self.Busy = False
            self.Execute = False

        else:
            # Reset outputs when not executing
            self.Done = False
            self.Busy = False
            self.Error = False
            self.ErrorID = 0

class UserAssignRole:
    """
    Synchronous simulation of ArUserAssignRole function block.
    Assigns a role to an existing user immediately in .call() when Execute is True.
    """

    # Simulated assignments: (username, role) pairs
    assigned_roles = set()

    # Error codes
    ERR_PARAMETER = -1070585894
    ERR_DOES_NOT_EXIST = -1070585892
    ERR_ALREADY_EXISTS = -1070585893
    ERR_INTERNAL = -1070585889

    def __init__(self):
        self.Execute = False
        self.UserName = ""
        self.RoleName = ""
        self.Done = False
        self.Busy = False
        self.Error = False
        self.ErrorID = 0

    def call(self):
        if self.Execute:
            self.Busy = True

            try:
                # Validate parameters
                if not self.UserName.strip() or not self.RoleName.strip():
                    self.Error = True
                    self.ErrorID = self.ERR_PARAMETER
                    self.Done = False

                # Check if user and role exist
                elif self.UserName not in UserCreate.created_users or \
                     self.RoleName not in UserCreateRole.created_roles:
                    self.Error = True
                    self.ErrorID = self.ERR_DOES_NOT_EXIST
                    self.Done = False

                # Check if assignment already exists
                elif (self.UserName, self.RoleName) in UserAssignRole.assigned_roles:
                    self.Error = True
                    self.ErrorID = self.ERR_ALREADY_EXISTS
                    self.Done = False

                else:
                    # Success: assign role to user
                    UserAssignRole.assigned_roles.add((self.UserName, self.RoleName))
                    self.Done = True
                    self.Error = False
                    self.ErrorID = 0

            except Exception:
                self.Error = True
                self.ErrorID = self.ERR_INTERNAL
                self.Done = False

            self.Busy = False
            self.Execute = False

        else:
            # Reset outputs if not executing
            self.Done = False
            self.Busy = False
            self.Error = False
            self.ErrorID = 0

class UserAuthenticatePassword:
    """
    Synchronous simulation of ArUserAuthenticatePassword function block.
    Verifies the password for a user immediately in .call() when Execute is True.
    """

    # Error codes
    ERR_PARAMETER = -1070585894
    ERR_DOES_NOT_EXIST = -1070585892
    ERR_INTERNAL = -1070585889
    ERR_MEMORY = -1070585890

    def __init__(self):
        self.Execute = False
        self.UserName = ""
        self.Password = ""
        self.Done = False
        self.Busy = False
        self.Error = False
        self.ErrorID = 0
        self.IsAuthentic = False

    def call(self):
        if self.Execute:
            self.Busy = True

            try:
                # Check parameters
                if not self.UserName.strip() or not self.Password:
                    self.Error = True
                    self.ErrorID = self.ERR_PARAMETER
                    self.Done = False
                    self.IsAuthentic = False

                # Check user existence
                elif self.UserName not in UserCreate.created_users:
                    self.Error = True
                    self.ErrorID = self.ERR_DOES_NOT_EXIST
                    self.Done = False
                    self.IsAuthentic = False

                else:
                    # Retrieve stored salted hash
                    stored_password = UserSetPassword._user_db.get(self.UserName)
                    if stored_password is None:
                        self.Error = True
                        self.ErrorID = self.ERR_DOES_NOT_EXIST
                        self.Done = False
                        self.IsAuthentic = False
                    else:
                        # Extract salt from stored password
                        salt_hex = stored_password[:12]  # 6 bytes in hex = 12 chars
                        hashed_stored = stored_password[12:]

                        salt = bytes.fromhex(salt_hex)
                        salted_input = salt + self.Password.encode('utf-8')
                        hashed_input = hashlib.sha256(salted_input).hexdigest()

                        if hashed_input == hashed_stored:
                            self.IsAuthentic = True
                        else:
                            self.IsAuthentic = False

                        # Success path
                        self.Error = False
                        self.ErrorID = 0
                        self.Done = True

            except MemoryError:
                self.Error = True
                self.ErrorID = self.ERR_MEMORY
                self.Done = False
                self.IsAuthentic = False

            except Exception:
                self.Error = True
                self.ErrorID = self.ERR_INTERNAL
                self.Done = False
                self.IsAuthentic = False

            self.Busy = False
            self.Execute = False

        else:
            # Reset outputs if not executing
            self.Done = False
            self.Busy = False
            self.Error = False
            self.ErrorID = 0
            self.IsAuthentic = False

