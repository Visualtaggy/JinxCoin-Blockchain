from hashlib import sha256


def update_hash(*args):
    hashing_text = ""
    h = sha256()

    for arg in args:
        hashing_text += str(arg)

    h.update(hashing_text.encode('utf-8'))
    return h.hexdigest()


class Block():
    tran = None
    hash = None
    nonce = 0
    previous_hash = "0" * 64

    def __init__(self, tran, number=0):
        self.tran = tran
        self.number = number

    def hash(self):
        return update_hash(self.previous_hash, self.number, self.tran, self.nonce)

    def __str__(self):
        return str("Block#: %s\nHash: %s\nPreviousHash%s\nData: %s\nNonce: %s\n" % (self.number, self.hash(), self.previous_hash, self.tran, self.nonce))


class JinxChain():
    difficulty = 4

    def __init__(self, chain=[]):
        self.chain = chain

    def add_block(self, block):
        self.chain.append(
            {
                "hash": block.hash(),
                "previous": block.previous_hash,
                "number": block.number,
                "tran": block.tran,
                "nonce": block.nonce
            }
        )

    def mine_coin(self, block):
        try:
            block.previous_hash = self.chain[-1].get('hash')
        except IndexError:
            pass

        while True:
            if block.hash()[:4] == "0" * self.difficulty:
                self.add_block(block)
                break
            else:
                block.nonce += 1


def testCode():
    blockchain = JinxChain()

    trans = ['sending money', 'receiving money', 'receiving money']

    idx = 0
    for tran in trans:
        idx += 1
        blockchain.mine_coin(Block(tran, idx))

    for block in blockchain.chain:
        print(block)


if __name__ == '__main__':
    testCode()
