# TESTS DESCRIPTION
# python main.py --help

# TESTS WITHOUT BLOCKCHAIN

# python main.py --help
# python main.py --type authentication --authentication-url http://127.0.0.1:5000 --jwt-secret JWT_SECRET_DEV_KEY --roles-field roles --owner-role owner --customer-role customer --courier-role courier 
# python main.py --type level0 --with-authentication --authentication-url http://127.0.0.1:5000 --owner-url http://127.0.0.1:5001 --customer-url http://127.0.0.1:5002
# python main.py --type level1 --with-authentication --authentication-url http://127.0.0.1:5000 --owner-url http://127.0.0.1:5001 --customer-url http://127.0.0.1:5002
# python main.py --type level2 --with-authentication --authentication-url http://127.0.0.1:5000 --customer-url http://127.0.0.1:5002 --courier-url http://127.0.0.1:5003 
# python main.py --type level3 --with-authentication --authentication-url http://127.0.0.1:5000 --owner-url http://127.0.0.1:5001 --customer-url http://127.0.0.1:5002 --courier-url http://127.0.0.1:5003
python main.py --type all --authentication-url http://127.0.0.1:5000 --jwt-secret JWT_SECRET_DEV_KEY --roles-field roles --owner-role owner --customer-role customer --courier-role courier --with-authentication --owner-url http://127.0.0.1:5001 --customer-url http://127.0.0.1:5002 --courier-url http://127.0.0.1:5003

# TESTS WITH BLOCKCHAIN

#python .\initialize_customer_account.py

# python main.py --type level1 --with-authentication --authentication-url http://127.0.0.1:5000 --owner-url http://127.0.0.1:5001 --customer-url http://127.0.0.1:5002 --with-blockchain --provider-url http://127.0.0.1:8545 --customer-keys-path ./keys.json --customer-passphrase iep_project --owner-private-key 0xb64be88dd6b89facf295f4fd0dda082efcbe95a2bb4478f5ee582b7efe88cf60
# python main.py --type level2 --with-authentication --authentication-url http://127.0.0.1:5000 --owner-url http://127.0.0.1:5001 --customer-url http://127.0.0.1:5002 --courier-url http://127.0.0.1:5003 --with-blockchain --provider-url http://127.0.0.1:8545 --customer-keys-path ./keys.json --customer-passphrase iep_project --owner-private-key 0xb64be88dd6b89facf295f4fd0dda082efcbe95a2bb4478f5ee582b7efe88cf60 --courier-private-key 0xbe07088da4ecd73ecb3d9d806cf391dfaef5f15f9ee131265da8af81728a4379
# python main.py --type level3 --with-authentication --authentication-url http://127.0.0.1:5000 --owner-url http://127.0.0.1:5001 --customer-url http://127.0.0.1:5002 --courier-url http://127.0.0.1:5003 --with-blockchain --provider-url http://127.0.0.1:8545 --customer-keys-path ./keys.json --customer-passphrase iep_project --owner-private-key 0xb64be88dd6b89facf295f4fd0dda082efcbe95a2bb4478f5ee582b7efe88cf60 --courier-private-key 0xbe07088da4ecd73ecb3d9d806cf391dfaef5f15f9ee131265da8af81728a4379
#python main.py --type all --authentication-url http://127.0.0.1:5000 --jwt-secret JWT_SECRET_DEV_KEY --roles-field roles --owner-role owner --customer-role customer --courier-role courier --with-authentication --owner-url http://127.0.0.1:5001 --customer-url http://127.0.0.1:5002 --courier-url http://127.0.0.1:5003 --with-blockchain --provider-url http://127.0.0.1:8545 --customer-keys-path ./keys.json --customer-passphrase iep_project --owner-private-key 0xb64be88dd6b89facf295f4fd0dda082efcbe95a2bb4478f5ee582b7efe88cf60 --courier-private-key 0xbe07088da4ecd73ecb3d9d806cf391dfaef5f15f9ee131265da8af81728a4379