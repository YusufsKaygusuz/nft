#contract.py
from web3 import Web3

# Web3 bağlantı detayları
infura_url = 'https://sepolia.infura.io/v3/e98b07a58abd43bd9f6f40209a7d600b'
web3 = Web3(Web3.HTTPProvider(infura_url))
contract_address = '0x4effee4385590cdfb3164355c8be7b356d172031'

# Convert to checksum address
contract_address = Web3.to_checksum_address(contract_address)

# Akıllı kontratın ABI'si
abi = [
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "internalType": "address", "name": "sender", "type": "address"},
            {"indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256"},
            {"indexed": False, "internalType": "string", "name": "hashValue", "type": "string"}
        ],
        "name": "HashStored",
        "type": "event"
    },
    {
        "inputs": [{"internalType": "string", "name": "hashValue", "type": "string"}],
        "name": "storeHash",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "stateMutability": "payable",
        "type": "receive"
    }
]

# Akıllı kontrat nesnesini oluştur
contract = web3.eth.contract(address=contract_address, abi=abi)

# Ethereum hesap bilgileri
sender_address = '0x45311ACDA40cB9EbCa1618dE7084c05347c1Cc52'
private_key = 'f5aa4f5c34f9e27e18352f758fe6c133e925e64834ee800595cf7a1907fa633f'

def store_hash(hash_value):
    if not hash_value:
        return False, "Hash value is missing"

    try:
        # storeHash fonksiyonunu çağırmak için işlem oluştur
        transaction = contract.functions.storeHash(hash_value).buildTransaction({
            'from': sender_address,
            'value': web3.toWei(0.01, 'ether'),  # 0.01 Ether gönderiliyor
            'gas': 2000000,
            'gasPrice': web3.toWei('20', 'gwei'),
            'nonce': web3.eth.getTransactionCount(sender_address),
        })

        # İşlemi imzala ve gönder
        signed_txn = web3.eth.account.signTransaction(transaction, private_key=private_key)
        tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)

        return True, web3.toHex(tx_hash)

    except Exception as e:
        return False, str(e)