#!/usr/bin/env python3

from test_framework.test_framework import BitcoinTestFramework
from test_framework.util import *
from test_framework.script import *
from test_framework.p2p import *
from test_framework.address import *
from test_framework.qtum import *
import pprint
import subprocess
import time

from decimal import Decimal 

pp = pprint.PrettyPrinter()

class QtumEVMLondonTest(BitcoinTestFramework):
    def add_options(self, parser):
        self.add_wallet_options(parser)

    def set_test_params(self):
        self.setup_clean_chain = True
        self.num_nodes = 4
        london_height=10000
        self.extra_args = [
                ['-txindex', '-logevents=1', '-staking=0', '-taprootheight={}'.format(london_height),'-londonheight={}'.format(london_height), '-addrindex'],
                ['-txindex', '-logevents=1', '-staking=1', '-taprootheight={}'.format(london_height), '-londonheight={}'.format(london_height)],
                ['-txindex', '-logevents=1', '-staking=1', '-taprootheight={}'.format(london_height), '-londonheight={}'.format(london_height)],
                ['-txindex', '-logevents=1', '-staking=1', '-taprootheight={}'.format(london_height), '-londonheight={}'.format(london_height)],
            ]
    
    def skip_test_if_missing_module(self):
        self.skip_if_no_wallet()
        
    def minemempool(self, node):
        while node.getmempoolinfo()['size']>0:
            generatesynchronized(node, 1)
        
    def run_test(self):
        self.log.info("Setting up chain and nodes")
        self.node = self.nodes[0]
        for n in self.nodes: n.setmocktime(int(time.time())-10000)
        
        generatesynchronized(self.node, COINBASE_MATURITY + 20, None, self.nodes[0:(self.num_nodes-1)])

            
        self.node_addresses=[]
        bytecode_qrc20 = "6080604052600860ff16600a620000179190620000f7565b7af316271c7fc3908a8bef464e3945ef7a25360a00000000000000006200003f919062000234565b6000553480156200004f57600080fd5b50600054600160003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002081905550620002db565b6000808291508390505b6001851115620000ee57808604811115620000c657620000c56200029f565b5b6001851615620000d65780820291505b8081029050620000e685620002ce565b9450620000a6565b94509492505050565b6000620001048262000295565b9150620001118362000295565b9250620001407fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff848462000148565b905092915050565b6000826200015a57600190506200022d565b816200016a57600090506200022d565b81600181146200018357600281146200018e57620001c4565b60019150506200022d565b60ff841115620001a357620001a26200029f565b5b8360020a915084821115620001bd57620001bc6200029f565b5b506200022d565b5060208310610133831016604e8410600b8410161715620001fe5782820a905083811115620001f857620001f76200029f565b5b6200022d565b6200020d84848460016200009c565b925090508184048111156200022757620002266200029f565b5b81810290505b9392505050565b6000620002418262000295565b91506200024e8362000295565b9250817fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff04831182151516156200028a57620002896200029f565b5b828202905092915050565b6000819050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052601160045260246000fd5b60008160011c9050919050565b610f5380620002eb6000396000f3fe608060405234801561001057600080fd5b506004361061009e5760003560e01c80635a3b7e42116100665780635a3b7e421461015d57806370a082311461017b57806395d89b41146101ab578063a9059cbb146101c9578063dd62ed3e146101f95761009e565b806306fdde03146100a3578063095ea7b3146100c157806318160ddd146100f157806323b872dd1461010f578063313ce5671461013f575b600080fd5b6100ab610229565b6040516100b89190610ce0565b60405180910390f35b6100db60048036038101906100d69190610c00565b610262565b6040516100e89190610cc5565b60405180910390f35b6100f961045a565b6040516101069190610d22565b60405180910390f35b61012960048036038101906101249190610bb1565b610460565b6040516101369190610cc5565b60405180910390f35b6101476107d4565b6040516101549190610d3d565b60405180910390f35b6101656107d9565b6040516101729190610ce0565b60405180910390f35b61019560048036038101906101909190610b4c565b610812565b6040516101a29190610d22565b60405180910390f35b6101b361082a565b6040516101c09190610ce0565b60405180910390f35b6101e360048036038101906101de9190610c00565b610863565b6040516101f09190610cc5565b60405180910390f35b610213600480360381019061020e9190610b75565b610a5e565b6040516102209190610d22565b60405180910390f35b6040518060400160405280600881526020017f515243205445535400000000000000000000000000000000000000000000000081525081565b600082600073ffffffffffffffffffffffffffffffffffffffff168173ffffffffffffffffffffffffffffffffffffffff1614156102d5576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016102cc90610d02565b60405180910390fd5b600083148061036057506000600260003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002054145b61036957600080fd5b82600260003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055508373ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff167f8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925856040516104479190610d22565b60405180910390a3600191505092915050565b60005481565b600083600073ffffffffffffffffffffffffffffffffffffffff168173ffffffffffffffffffffffffffffffffffffffff1614156104d3576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016104ca90610d02565b60405180910390fd5b83600073ffffffffffffffffffffffffffffffffffffffff168173ffffffffffffffffffffffffffffffffffffffff161415610544576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161053b90610d02565b60405180910390fd5b6105ca600260008873ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205485610a83565b600260008873ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002081905550610693600160008873ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205485610a83565b600160008873ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000208190555061071f600160008773ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205485610ad0565b600160008773ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055508473ffffffffffffffffffffffffffffffffffffffff168673ffffffffffffffffffffffffffffffffffffffff167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef866040516107bf9190610d22565b60405180910390a36001925050509392505050565b600881565b6040518060400160405280600981526020017f546f6b656e20302e31000000000000000000000000000000000000000000000081525081565b60016020528060005260406000206000915090505481565b6040518060400160405280600381526020017f515443000000000000000000000000000000000000000000000000000000000081525081565b600082600073ffffffffffffffffffffffffffffffffffffffff168173ffffffffffffffffffffffffffffffffffffffff1614156108d6576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016108cd90610d02565b60405180910390fd5b61091f600160003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205484610a83565b600160003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055506109ab600160008673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205484610ad0565b600160008673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055508373ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef85604051610a4b9190610d22565b60405180910390a3600191505092915050565b6002602052816000526040600020602052806000526040600020600091509150505481565b600081831015610abc577f4e487b7100000000000000000000000000000000000000000000000000000000600052600160045260246000fd5b8183610ac89190610dca565b905092915050565b6000808284610adf9190610d74565b905083811015610b18577f4e487b7100000000000000000000000000000000000000000000000000000000600052600160045260246000fd5b8091505092915050565b600081359050610b3181610eef565b92915050565b600081359050610b4681610f06565b92915050565b600060208284031215610b5e57600080fd5b6000610b6c84828501610b22565b91505092915050565b60008060408385031215610b8857600080fd5b6000610b9685828601610b22565b9250506020610ba785828601610b22565b9150509250929050565b600080600060608486031215610bc657600080fd5b6000610bd486828701610b22565b9350506020610be586828701610b22565b9250506040610bf686828701610b37565b9150509250925092565b60008060408385031215610c1357600080fd5b6000610c2185828601610b22565b9250506020610c3285828601610b37565b9150509250929050565b610c4581610e10565b82525050565b6000610c5682610d58565b610c608185610d63565b9350610c70818560208601610e53565b610c7981610eb5565b840191505092915050565b6000610c91600f83610d63565b9150610c9c82610ec6565b602082019050919050565b610cb081610e3c565b82525050565b610cbf81610e46565b82525050565b6000602082019050610cda6000830184610c3c565b92915050565b60006020820190508181036000830152610cfa8184610c4b565b905092915050565b60006020820190508181036000830152610d1b81610c84565b9050919050565b6000602082019050610d376000830184610ca7565b92915050565b6000602082019050610d526000830184610cb6565b92915050565b600081519050919050565b600082825260208201905092915050565b6000610d7f82610e3c565b9150610d8a83610e3c565b9250827fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff03821115610dbf57610dbe610e86565b5b828201905092915050565b6000610dd582610e3c565b9150610de083610e3c565b925082821015610df357610df2610e86565b5b828203905092915050565b6000610e0982610e1c565b9050919050565b60008115159050919050565b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b6000819050919050565b600060ff82169050919050565b60005b83811015610e71578082015181840152602081019050610e56565b83811115610e80576000848401525b50505050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052601160045260246000fd5b6000601f19601f8301169050919050565b7f41646472657373206973204e554c4c0000000000000000000000000000000000600082015250565b610ef881610dfe565b8114610f0357600080fd5b50565b610f0f81610e3c565b8114610f1a57600080fd5b5056fea2646970667358221220428f0675eabb8d19af3d0c2868ed3d1faf18c135df79935059e8f6da0fba00e864736f6c63430008020033"
        
        create_contract = self.node.createcontract(bytecode_qrc20)
        self.contract_address = create_contract['address']
        self.sender = create_contract['sender']
        self.minemempool(self.node)
        self.log.info("Distributing coins and tokens")
        balances=[]
        for i in range(1, self.num_nodes):
            self.node_addresses.append(self.nodes[i].getnewaddress())
            self.node.sendtoaddress(address=self.node_addresses[i-1], amount=40000)
            self.node.qrc20transfer(self.contract_address, self.sender, self.node_addresses[i-1], "1000000")
            balances.append({'address':self.node_addresses[i-1], 'amount':1000000})
            generatesynchronized(self.node, 6, None, self.nodes[0:(self.num_nodes-1)])
            self.nodes[i].splitutxosforaddress(self.node_addresses[i-1], 100, 100, 10000)
            generatesynchronized(self.nodes[i], 6, None, self.nodes[0:(self.num_nodes-1)])     
        
        generatesynchronized(self.node, COINBASE_MATURITY+20, None, self.nodes[0:(self.num_nodes-1)])
        
        for n in self.nodes: n.setmocktime(int(time.time()))
        
        next_possible_fork_height = 6048
        self.log.info("Advancing to fork height -10")
        generatesynchronized(self.node, next_possible_fork_height-self.node.getblockcount()-10, None, self.nodes[0:(self.num_nodes-1)])
        
        london_height = next_possible_fork_height
        self.log.info("Restart nodes")
        self.stop_nodes()
        self.start_node(0, ['-txindex', '-logevents=1', '-staking=0', '-taprootheight={}'.format(london_height), '-londonheight={}'.format(london_height), '-addrindex'])
        for i in range(1, self.num_nodes):
            self.start_node(i, ['-txindex', '-logevents=1', '-staking=1', '-taprootheight={}'.format(london_height), '-londonheight={}'.format(london_height)])
        for i in range(1, self.num_nodes):
            self.connect_nodes(i-1, i)
        
        self.log.info("Waiting for fork to activate (using PoS)")
        printforkdone=False
        printmempoolwait=False
        while True:
            for i in range(0, self.num_nodes):
                if(not printforkdone and self.node.getblockcount() >= london_height):
                    self.log.info("Fork active at height {}, generating more transactions".format(london_height))
                    printforkdone = True
                if i>0 and self.node.getblockcount() <= london_height+30:
                    self.node.qrc20transfer(self.contract_address, self.sender, self.node_addresses[i-1], "1000000")
                    balances[i-1]["amount"]+=1000000
                    self.nodes[i].sendtoaddress(address=self.node_addresses[i-1], amount=777)
                elif self.node.getblockcount() > london_height+30 and printforkdone and not printmempoolwait:
                    self.log.info("Stopped transactions generation, waiting for mempool to be cleared")
                    printmempoolwait= True
            mempoolclear= True;
            for i in range(0, self.num_nodes):
                if self.nodes[i].getmempoolinfo()['size']: mempoolclear= False;
            if mempoolclear: break
            time.sleep(3)

        self.log.info("Checking balances)")
        for i in range(1, self.num_nodes):
            assert_equal(Decimal(balances[i-1]["amount"]), Decimal(self.nodes[i].qrc20balanceof(self.contract_address, self.node_addresses[i-1])))   
        
if __name__ == '__main__':
    QtumEVMLondonTest().main()