from hashlib import sha256


def update_hash(*args):
    hashing_text = ""
    h = sha256()

    for arg in args:
        hashing_text += str(arg)

    h.update(hashing_text.encode('utf-8'))
    return h.hexdigest()


class Block():

    def __init__(self, number=0, previous_hash="0"*64, tran=None, nonce=0):
        self.tran = tran
        self.number = number
        self.previous_hash = previous_hash
        self.nonce = nonce

    def hash(self):
        return update_hash(
            self.number,
            self.previous_hash,
            self.tran,
            self.nonce
        )

    def __str__(self):
        return str("Block: %s\nHash: %s\nPrevious: %s\nData: %s\nNonce: %s\n" % (
            self.number,
            self.hash(),
            self.previous_hash,
            self.tran,
            self.nonce
        )
        )


class JinxChain():
    # should be dynamic and increase as the number of clients / users on the blockchain increase!
    difficulty = 3

    def __init__(self):
        self.chain = []

    def add_block(self, block):
        self.chain.append(block)

    def remove(self, block):
        self.chain.remove(block)

    def mine_coin(self, block):
        try:
            block.previous_hash = self.chain[-1].hash()
        except IndexError:
            pass

        while True:
            if block.hash()[:self.difficulty] == "0" * self.difficulty:
                self.add_block(block)
                break
            else:
                block.nonce += 1

    def verify_integrity(self):
        for i in range(1, len(self.chain)):
            _previous = self.chain[i].previous_hash
            _current = self.chain[i-1].hash()
            if _previous != _current or _current[:self.difficulty] != "0"*self.difficulty:
                return False

        return True


def testCode():
    blockchain = JinxChain()
    database = ["sending money", "receiving money",
                "receiving money", "sending money"]
    num = 0

    for tran in database:
        num += 1
        blockchain.mine_coin(Block(num, tran=tran))

    for block in blockchain.chain:
        print(block)

    print(blockchain.verify_integrity())

    blockchain.chain[2].tran = "HACKED MONEY"
    for block in blockchain.chain:
        print(block)
    # blockchain.mine_coin(blockchain.chain[2])
    print(blockchain.verify_integrity())


if __name__ == '__main__':
    testCode()
