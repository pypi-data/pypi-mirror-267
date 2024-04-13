# DeFiPy: DeFi Analytics with Python (v 0.0.17)

Welcome to the worlds first DeFi Python package with all major protocols intergrated into one package! Implement your analytics in one package with DeFiPy. Since DeFiPy is built with a modular design in mind, your can also silo your analytics by protocol 
using:
* [UniswapPy](https://github.com/defipy-devs/uniswappy)
* [BalancerPy](https://github.com/defipy-devs/balancerpy)
* [StableSwapPy](https://github.com/defipy-devs/stableswappy)

## Docs
Visit [DeFiPy docs](https://defipy.org) for full documentation with walk-through tutorials

## Install
Must first install gmpy2 python package to handle the precision within the StableSwap protocol (requires CPython 3.7 or above). To install the latest release with pip:
```
> pip install gmpy2
```
Also, in many cases will need to have required libraries (GMP, MPFR and MPC) already installed on your system, see [gmpy2 installation docs](https://gmpy2.readthedocs.io/en/latest/install.html) for more info. Once setup, install the latest release of DeFiPy with pip:
```
> git clone https://github.com/defipy-devs/defipy
> pip install .
```
or
```
> pip install defipy
```

Uniswap Example
--------------------------

To setup a liquidity pool, you must first create the tokens in the pair using the `ERC20` object. Next, create a liquidity pool (LP) factory using `IFactory` object. Once this is setup, an unlimited amount of LPs can be created; the procedures for such are as follows:


    from defipy import *

    user_nm = 'user_intro'
    eth_amount = 1000
    dai_amount = 1000000

    dai = ERC20("DAI", "0x01")
    eth = ERC20("ETH", "0x02")
    
    factory = UniswapFactory("ETH pool factory", "0x")
    exchg_data = UniswapExchangeData(tkn0 = eth, tkn1 = dai, symbol="LP", address="0x11")
    lp = factory.deploy(exchg_data)
    lp.add_liquidity("user0", eth_amount, dai_amount, eth_amount, dai_amount)
    lp.summary()
    

    #OUTPUT:
    Exchange ETH-DAI (LP)
    Reserves: ETH = 1000, DAI = 1000000
    Liquidity: 31622.776601683792 
    
Balancer Example
--------------------------   

    from defipy import *
    
    USER = 'user_test'

    amt_dai = 10000000
    denorm_wt_dai = 10

    amt_eth = 67738.6361731024
    denorm_wt_eth = 40

    init_pool_shares = 100    

    dai = ERC20("DAI", "0x01")
    dai.deposit(None, amt_dai)

    weth = ERC20("WETH", "0x02")
    weth.deposit(None, amt_eth)

    bgrp = BalancerVault()
    bgrp.add_token(dai, denorm_wt_dai)
    bgrp.add_token(weth, denorm_wt_eth)

    bfactory = BalancerFactory("WETH pool factory", "0x")
    exchg_data = BalancerExchangeData(vault = bgrp, symbol="LP", address="0x1")
    lp = bfactory.deploy(exchg_data)
    lp.join_pool(bgrp, init_pool_shares, USER)
    lp.summary()


    #OUTPUT:
    Balancer Exchange: DAI|WETH (LP)
    Reserves: DAI = 10000000, WETH = 67738.6361731024
    Weights: DAI = 0.2, WETH = 0.8
    Pool Shares: 100 
    
StableSwap Example
--------------------------   

    from defipy import *
    
    USER = 'user_test'

    AMPL_COEFF = 2000 

    amt_dai = 79566307.559825807715868071
    decimal_dai = 18

    amt_usdc = 81345068.187939
    decimal_usdc = 6

    amt_usdt = 55663250.772939
    decimal_usdt = 6
    
    dai = ERC20("DAI", "0x01", decimal_dai)
    dai.deposit(None, amt_dai)

    usdc = ERC20("USDC", "0x02", decimal_usdc)
    usdc.deposit(None, amt_usdc)

    usdt = ERC20("USDT", "0x03", decimal_usdt)
    usdt.deposit(None, amt_usdt)    
    
    sgrp = StableswapVault()
    sgrp.add_token(dai)
    sgrp.add_token(usdc)
    sgrp.add_token(usdt)    

    sfactory = StableswapFactory("Pool factory", "0x")
    exchg_data = StableswapExchangeData(vault = sgrp, symbol="LP", address="0x11")
    lp = sfactory.deploy(exchg_data)
    lp.join_pool(sgrp, AMPL_COEFF, USER)
    lp.summary()


    #OUTPUT:
    Stableswap Exchange: DAI-USDC-USDT (LP)
    Reserves: DAI = 79566307.55982581, USDC = 81345068.187939, USDT = 55663250.772939
    Liquidity: 216573027.91811988   
