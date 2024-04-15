🏗👷🏾 Moodyeth
============

Ether API for Python The only Library
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

|moodyeth| |image1| |image2| |image3|

Ethereum based all Moody tool chain for smart contract development kit
`documentation <https://htmlpreview.github.io/?https://github.com/tokenchain/moodyeth/blob/main/docs/moody/index.html>`__.

Why do we use python
~~~~~~~~~~~~~~~~~~~~

Using it because it is fast and easy. More importantly it runs directly
by its own and no more dependencies.

Its much faster to building modules and calling functions on python.
Also it can be wrapped into an executable binary on wasm or cpython that
runs on natively any platforms.

If you are using PyCharm or similar IDE, all type are ready to show at
your finger tips.

Get Started
~~~~~~~~~~~

``pip3 install moodyeth``

or upgrade using

``sudo pip3 install moodyeth --upgrade``

or try this without vpn

``sudo pip3 install moodyeth --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple``

``sudo pip3 install moodyeth --upgrade -i https://pypi.python.org/simple``

The development of Moody contract deployment tools:

Setup (for the early version, we are going to setup the workspace
manually. )

Setup the folders: /vault /artifact /deploy_history /deploy_results
/factoryabi

Why use moody eth
~~~~~~~~~~~~~~~~~

It is a all-in-one package with zero setup and configurations that works
for multiple architectures. It is lightweight and simple. Build-in ERC20
support and bulk token sending support. Out of the box that comes with
solc-compile automation and web3 executions.

Features
~~~~~~~~

-  support most of the evm compatible chains
-  golang module compile support
-  python module compile support
-  typescript module compile support
-  forge foundry support
-  flashbots support
-  implementation of contract upgradings
-  upgrade contracts for 3 different ways
-  Multicall3 interactions

Examples:
~~~~~~~~~

Deployment of the new contract:
'''''''''''''''''''''''''''''''

.. code:: python

   # !/usr/bin/env python
   # coding: utf-8
   import os

   from moody.libeb import MiliDoS
   from moody import conf

   privatekey = "xxxxxxxx"
   # now using xDAI
   network = conf.XDaiMainnet()

   ROOT = os.path.join(os.path.dirname(__file__))
   meta = MiliDoS(network).withPOA()
   meta.setWorkspace(ROOT).Auth(privatekey)
   meta.deploy("Ori20")

BSend add signer
^^^^^^^^^^^^^^^^

Adding signer using bsend

.. code:: python

   # !/usr/bin/env python
   # coding: utf-8
   import os

   from moody.libeb import MiliDoS
   from moody import conf

   privatekey = "xxxxxxxx"
   # now using xDAI
   network = conf.XDaiMainnet()

   #gas and gas price configurations
   meta.OverrideGasConfig(6000000, 2000000000)

   ROOT = os.path.join(os.path.dirname(__file__))
   meta = MiliDoS(network).withPOA().setWorkspace(ROOT).Auth(privatekey)

   contract_address = "0x_________________"

   signing_address =  "0x________my_wallet"

   expressContract = BSend(meta, contract_address).CallAutoConf(meta).CallDebug(True)

   expressContract.add_signer(signing_address)

Mint Coins
^^^^^^^^^^

The example for minting coins with 18 decimal

.. code:: python

   # !/usr/bin/env python
   # coding: utf-8
   import os

   from moody.libeb import MiliDoS
   from moody import conf
   from moody.m.tc20 import Tc20

   privatekey = "xxxxxxxx"
   contract_address = "0x_________________"
   my_wallet =  "0x________my_wallet"

   # now using xDAI
   network = conf.XDaiMainnet()

   #gas and gas price configurations
   meta.OverrideGasConfig(6000000, 2000000000)

   ROOT = os.path.join(os.path.dirname(__file__))
   meta = MiliDoS(network).withPOA().setWorkspace(ROOT).Auth(privatekey)


   tokenContract = Tc20(meta, contract_address).CallAutoConf(meta)

   # assume this coin comes with 18 decimal
   tokenContract.EnforceTxReceipt(True).mint(my_wallet, 300*10**18)

Example for compiling contracts with solc
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   # !/usr/bin/env python
   # coding: utf-8


   from moody import conf, Evm
   from moody.libeb import MiliDoS

   ROOT = "my_workspace_path"

   # as the solidity compiler version
   SOLV = "0.8.6"

   CONTRACT_LIST = [
       "vault/folder1/xxx1.sol",
       "vault/folder2/xxx2.sol",
       "vault/folder2/xxx3.sol",
   ]



   netcompile = conf.RSCMainnet()
   r = MiliDoS(netcompile)
   print("-----> the workspace location")
   print(ROOT)
   r.setWorkspace(ROOT).setOptimizationRuns(5000).setEvm(Evm.ISTANBUL).setClassSolNames(CONTRACT_LIST).remoteCompile(SOLV).localTranspile()
   # Optionally you can directly call the execution to run the localtranspile
   # r.setWorkspace(ROOT).setClassSolNames(CONTRACT_LIST).localTranspile()
   # os.system("sh localpile")

Code compile
^^^^^^^^^^^^

The new build codebase all in the one take. In order to use this
feature, the required package will need to be installed to the system.
Otherwise the error message will show.

-  factoryabi (source transpiler for ts and python)
-  forge (solidity compiler)
-  abigen (golang transpile generator)
-  abi-gen-uni (transpiler consumer)

If you are all set, then you are ready to run the following code for
example:

.. code:: python

   # !/usr/bin/env python
   # coding: utf-8
   import os
   from moody.libeb import MiliDoS
   from moody import Evm, conf
   from key import ROOT

   SOLV = "0.8.12"
   C811 = [
       "vault/token/RaceToken.sol",
   ]
   network = conf.EthereumFL()
   r = MiliDoS(network)

   ROOT = '/.../Documents/b95/devmoody'
   FACTORY = '$HOME/Documents/piplines/factoryabi'
   r.brew(ROOT, FACTORY).setClassSolNames(C811).setEvm(Evm.ISTANBUL)
   r.useForge().localTranspile()

Example for multicall
~~~~~~~~~~~~~~~~~~~~~

.. code:: python


   from multicall import Call, Multicall

   # assuming you are on kovan
   MKR_TOKEN = '0xaaf64bfcc32d0f15873a02163e7e500671a4ffcd'
   MKR_WHALE = '0xdb33dfd3d61308c33c63209845dad3e6bfb2c674'
   MKR_FISH = '0x2dfcedcb401557354d0cf174876ab17bfd6f4efd'

   def from_wei(value):
       return value / 1e18

   multi = Multicall([
       Call(MKR_TOKEN, ['balanceOf(address)(uint256)', MKR_WHALE], [('whale', from_wei)]),
       Call(MKR_TOKEN, ['balanceOf(address)(uint256)', MKR_FISH], [('fish', from_wei)]),
       Call(MKR_TOKEN, 'totalSupply()(uint256)', [('supply', from_wei)]),
   ])

   multi()  # {'whale': 566437.0921992733, 'fish': 7005.0, 'supply': 1000003.1220798912}

   # seth-style calls
   Call(MKR_TOKEN, ['balanceOf(address)(uint256)', MKR_WHALE])()
   Call(MKR_TOKEN, 'balanceOf(address)(uint256)')(MKR_WHALE)
   # return values processing
   Call(MKR_TOKEN, 'totalSupply()(uint256)', [('supply', from_wei)])()

Documentation is ready
`here <https://htmlpreview.github.io/?https://github.com/tokenchain/moodyeth/blob/main/docs/moody/index.html>`__

Also there is a brother library for those who works with
`Tron <https://github.com/tokenchain/tronpytool>`__ network.

Donations
~~~~~~~~~

Welcome for donation for the good works!

.. |moodyeth| image:: https://img.shields.io/pypi/v/moodyeth?style=plastic
   :target: https://pypi.org/project/moodyeth/
.. |image1| image:: https://img.shields.io/pypi/pyversions/moodyeth.svg
   :target: https://pypi.org/project/moodyeth/
.. |image2| image:: https://api.travis-ci.com/tokenchain/moodyeth.svg?branch=master
   :target: https://pypi.org/project/moodyeth/
.. |image3| image:: https://img.shields.io/github/issues/tokenchain/moodyeth.svg
   :target: https://pypi.org/project/moodyeth/
