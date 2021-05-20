# Copyright (c) 2021 Bixbit s.c. All rights reserved.
# See LICENSE file for licensing information.

import furms
import logging
import os
from storage import Storage
from pathlib import Path
import time

class SSHKeyRequestHandler:
    """
    Creates the 'ssh_keys' directory in current one with a structure of subdirectories
    that corresponds to user, and 'authorized_keys' file inside.
    FURMS ssh key requests are applied to proper authorized_keys file. e.g. the request
    to add SSH key for user with fenix id "XYZ", is translated to the '$PWD/ssh_keys/XYZ/authorized_keys'
    file update, and the given ssh key is added to it.
    """
    _logger = logging.getLogger(__name__)

    def __init__(self, storage: Storage) -> None:
        self.varDir = storage.varDir

    def handle_sshkey_add(self, request:furms.UserSSHKeyAddRequest, header:furms.Header, sitePublisher:furms.SitePublisher) -> None:
        self._logger.info("SSH key add request: %s" % request)

        if "fake" in request.publicKey:
            headerOKResponse = self._header_from(header)
            sitePublisher.publish(headerOKResponse, furms.UserSSHKeyAddRequestAck())
            
            headerFailResponse = furms.Header(header.messageCorrelationId, 1, "FAILED", 
                            furms.Error("security_validation", "Creating fake keys is prohibited"))
            sitePublisher.publish(headerFailResponse, furms.UserSSHKeyAddResult())
            
        elif "evil" in request.publicKey:
            headerFailResponse = furms.Header(header.messageCorrelationId, 1, "FAILED", 
                            furms.Error("security_validation", "Creating evil keys is completely prohibited"))
            sitePublisher.publish(headerFailResponse, furms.UserSSHKeyAddRequestAck())

        elif "jit" in request.publicKey:
            headerResponse = self._header_from(header)
            UserAuthorizedKeys(request.fenixUserId, self.varDir).add(request.publicKey)
            sitePublisher.publish(headerResponse, furms.UserSSHKeyAddResult())

        elif "bug" in request.publicKey:
            headerResponse = self._header_from(header)
            UserAuthorizedKeys(request.fenixUserId, self.varDir).add(request.publicKey)
            sitePublisher.publish(headerResponse, furms.UserSSHKeyAddResult())
            sitePublisher.publish(headerResponse, furms.UserSSHKeyAddRequestAck())

        else:

            headerResponse = self._header_from(header)
            sitePublisher.publish(headerResponse, furms.UserSSHKeyAddRequestAck())

            UserAuthorizedKeys(request.fenixUserId, self.varDir).add(request.publicKey)

            sitePublisher.publish(headerResponse, furms.UserSSHKeyAddResult())

    def handle_sshkey_remove(self, request:furms.UserSSHKeyRemovalRequest, header:furms.Header, sitePublisher:furms.SitePublisher) -> None:
        self._logger.info("SSH key removal request: %s" % request)

        headerResponse = self._header_from(header)
        sitePublisher.publish(headerResponse, furms.UserSSHKeyRemovalRequestAck())

        UserAuthorizedKeys(request.fenixUserId, self.varDir).remove(request.publicKey)

        sitePublisher.publish(headerResponse, furms.UserSSHKeyRemovalResult())

    def handle_sshkey_update(self, request:furms.UserSSHKeyUpdateRequest, header:furms.Header, sitePublisher:furms.SitePublisher) -> None:
        self._logger.info("SSH key update request: %s" % request)

        if "evil" in request.newPublicKey:
            headerFailResponse = furms.Header(header.messageCorrelationId, 1, "FAILED", 
                            furms.Error("security_validation", "Creating evil keys is completely prohibited"))
            sitePublisher.publish(headerFailResponse, furms.UserSSHKeyUpdateRequestAck())
        else:
            headerResponse = self._header_from(header)
            sitePublisher.publish(headerResponse, furms.UserSSHKeyUpdateRequestAck())

            UserAuthorizedKeys(request.fenixUserId, self.varDir).update(request.oldPublicKey, request.newPublicKey)

            sitePublisher.publish(headerResponse, furms.UserSSHKeyUpdateResult())

    def _header_from(self, header:furms.Header):
        return furms.Header(header.messageCorrelationId, header.version, "OK")


class UserAuthorizedKeys:
    _SSH_KEYS_DIR = "ssh_keys"
    _AUTHORIZED_KEYS = "authorized_keys"

    def __init__(self, fenixUserId, varDir) -> None:
        keys_path = os.path.join(os.getcwd(), varDir, self._SSH_KEYS_DIR, fenixUserId)
        Path(keys_path).mkdir(parents=True, exist_ok=True)
        self._authorized_keys = os.path.join(keys_path, self._AUTHORIZED_KEYS)

    def add(self, publicKey):
        with open(self._authorized_keys, "a") as keys:
            keys.write(publicKey + "\n")

    def remove(self, publicKey):
        content = self._load()
        if content:
            with open(self._authorized_keys, "w") as file:
                for key in content:
                    if key.strip() != publicKey:
                        file.write(key)

    def update(self, oldPublicKey, newPublicKey):
        content = self._load()
        if content:
            with open(self._authorized_keys, "w") as file:
                for key in content:
                    if key.strip() == oldPublicKey:
                        file.write(newPublicKey + '\n')
                    else:
                        file.write(key)

    def _load(self):
        if Path(self._authorized_keys).is_file():
            file = open(self._authorized_keys, "r")
            return file.readlines()
        return []

