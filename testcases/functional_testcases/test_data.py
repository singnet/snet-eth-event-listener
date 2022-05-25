import json


class RegistryContract:
    abi = json.loads(
        '[{"type": "constructor", "inputs": [], "stateMutability": "nonpayable"}, {"name": "OrganizationCreated", "type": "event", "inputs": [{"name": "orgId", "type": "bytes32", "indexed": true, "internalType": "bytes32"}], "anonymous": false}, {"name": "OrganizationDeleted", "type": "event", "inputs": [{"name": "orgId", "type": "bytes32", "indexed": true, "internalType": "bytes32"}], "anonymous": false}, {"name": "OrganizationModified", "type": "event", "inputs": [{"name": "orgId", "type": "bytes32", "indexed": true, "internalType": "bytes32"}], "anonymous": false}, {"name": "ServiceCreated", "type": "event", "inputs": [{"name": "orgId", "type": "bytes32", "indexed": true, "internalType": "bytes32"}, {"name": "serviceId", "type": "bytes32", "indexed": true, "internalType": "bytes32"}, {"name": "metadataURI", "type": "bytes", "indexed": false, "internalType": "bytes"}], "anonymous": false}, {"name": "ServiceDeleted", "type": "event", "inputs": [{"name": "orgId", "type": "bytes32", "indexed": true, "internalType": "bytes32"}, {"name": "serviceId", "type": "bytes32", "indexed": true, "internalType": "bytes32"}], "anonymous": false}, {"name": "ServiceMetadataModified", "type": "event", "inputs": [{"name": "orgId", "type": "bytes32", "indexed": true, "internalType": "bytes32"}, {"name": "serviceId", "type": "bytes32", "indexed": true, "internalType": "bytes32"}, {"name": "metadataURI", "type": "bytes", "indexed": false, "internalType": "bytes"}], "anonymous": false}, {"name": "ServiceTagsModified", "type": "event", "inputs": [{"name": "orgId", "type": "bytes32", "indexed": true, "internalType": "bytes32"}, {"name": "serviceId", "type": "bytes32", "indexed": true, "internalType": "bytes32"}], "anonymous": false}, {"name": "supportsInterface", "type": "function", "inputs": [{"name": "interfaceId", "type": "bytes4", "internalType": "bytes4"}], "outputs": [{"name": "", "type": "bool", "internalType": "bool"}], "constant": true, "stateMutability": "view"}, {"name": "createOrganization", "type": "function", "inputs": [{"name": "orgId", "type": "bytes32", "internalType": "bytes32"}, {"name": "orgMetadataURI", "type": "bytes", "internalType": "bytes"}, {"name": "members", "type": "address[]", "internalType": "address[]"}], "outputs": [], "stateMutability": "nonpayable"}, {"name": "changeOrganizationOwner", "type": "function", "inputs": [{"name": "orgId", "type": "bytes32", "internalType": "bytes32"}, {"name": "newOwner", "type": "address", "internalType": "address"}], "outputs": [], "stateMutability": "nonpayable"}, {"name": "changeOrganizationMetadataURI", "type": "function", "inputs": [{"name": "orgId", "type": "bytes32", "internalType": "bytes32"}, {"name": "orgMetadataURI", "type": "bytes", "internalType": "bytes"}], "outputs": [], "stateMutability": "nonpayable"}, {"name": "addOrganizationMembers", "type": "function", "inputs": [{"name": "orgId", "type": "bytes32", "internalType": "bytes32"}, {"name": "newMembers", "type": "address[]", "internalType": "address[]"}], "outputs": [], "stateMutability": "nonpayable"}, {"name": "removeOrganizationMembers", "type": "function", "inputs": [{"name": "orgId", "type": "bytes32", "internalType": "bytes32"}, {"name": "existingMembers", "type": "address[]", "internalType": "address[]"}], "outputs": [], "stateMutability": "nonpayable"}, {"name": "deleteOrganization", "type": "function", "inputs": [{"name": "orgId", "type": "bytes32", "internalType": "bytes32"}], "outputs": [], "stateMutability": "nonpayable"}, {"name": "createServiceRegistration", "type": "function", "inputs": [{"name": "orgId", "type": "bytes32", "internalType": "bytes32"}, {"name": "serviceId", "type": "bytes32", "internalType": "bytes32"}, {"name": "metadataURI", "type": "bytes", "internalType": "bytes"}], "outputs": [], "stateMutability": "nonpayable"}, {"name": "updateServiceRegistration", "type": "function", "inputs": [{"name": "orgId", "type": "bytes32", "internalType": "bytes32"}, {"name": "serviceId", "type": "bytes32", "internalType": "bytes32"}, {"name": "metadataURI", "type": "bytes", "internalType": "bytes"}], "outputs": [], "stateMutability": "nonpayable"}, {"name": "deleteServiceRegistration", "type": "function", "inputs": [{"name": "orgId", "type": "bytes32", "internalType": "bytes32"}, {"name": "serviceId", "type": "bytes32", "internalType": "bytes32"}], "outputs": [], "stateMutability": "nonpayable"}, {"name": "listOrganizations", "type": "function", "inputs": [], "outputs": [{"name": "orgIds", "type": "bytes32[]", "internalType": "bytes32[]"}], "constant": true, "stateMutability": "view"}, {"name": "getOrganizationById", "type": "function", "inputs": [{"name": "orgId", "type": "bytes32", "internalType": "bytes32"}], "outputs": [{"name": "found", "type": "bool", "internalType": "bool"}, {"name": "id", "type": "bytes32", "internalType": "bytes32"}, {"name": "orgMetadataURI", "type": "bytes", "internalType": "bytes"}, {"name": "owner", "type": "address", "internalType": "address"}, {"name": "members", "type": "address[]", "internalType": "address[]"}, {"name": "serviceIds", "type": "bytes32[]", "internalType": "bytes32[]"}], "constant": true, "stateMutability": "view"}, {"name": "listServicesForOrganization", "type": "function", "inputs": [{"name": "orgId", "type": "bytes32", "internalType": "bytes32"}], "outputs": [{"name": "found", "type": "bool", "internalType": "bool"}, {"name": "serviceIds", "type": "bytes32[]", "internalType": "bytes32[]"}], "constant": true, "stateMutability": "view"}, {"name": "getServiceRegistrationById", "type": "function", "inputs": [{"name": "orgId", "type": "bytes32", "internalType": "bytes32"}, {"name": "serviceId", "type": "bytes32", "internalType": "bytes32"}], "outputs": [{"name": "found", "type": "bool", "internalType": "bool"}, {"name": "id", "type": "bytes32", "internalType": "bytes32"}, {"name": "metadataURI", "type": "bytes", "internalType": "bytes"}], "constant": true, "stateMutability": "view"}]')
    network_address = "0xB12089BD3F20A2C546FAad4167A08C57584f89C8"
    start_block_no = 10242667
    name = "Registry"
    blocks_adjustment = 5
    last_block_no = 10908545
