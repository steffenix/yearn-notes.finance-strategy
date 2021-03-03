import pytest
from brownie import config
from brownie import Contract


@pytest.fixture
def gov(accounts):
    yield accounts[0]


@pytest.fixture
def rewards(accounts):
    yield accounts[1]


@pytest.fixture
def guardian(accounts):
    yield accounts[2]


@pytest.fixture
def management(accounts):
    yield accounts[3]


@pytest.fixture
def strategist(accounts):
    yield accounts[4]


@pytest.fixture
def keeper(accounts):
    yield accounts[5]


@pytest.fixture
def token():
    token_address = "0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490"  # this should be the address of the ERC-20 used by the strategy/vault (DAI)
    yield Contract(token_address)

@pytest.fixture
def amount(accounts, token, dai, three_curvepool):
    amount = 10_000 * 10 ** dai.decimals()
    dai.approve(three_curvepool, amount, {"from": accounts[0]})
    three_curvepool.add_liquidity([amount, 0, 0], 0, {"from": accounts[0]})
    
    print(token.balanceOf(accounts[0]))

    yield token.balanceOf(accounts[0])


@pytest.fixture
def weth():
    token_address = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
    yield Contract(token_address)

@pytest.fixture
def three_curvepool():
    yield Contract("0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7")

@pytest.fixture
def dai(accounts):
    dai = Contract("0x6b175474e89094c44da98b954eedeac495271d0f")
    reserve = accounts.at("0xd551234ae421e3bcba99a0da6d736074f22192ff", force=True)
    amount = 50_000 * 10 ** dai.decimals()
    dai.transfer(accounts[0], amount, {"from": reserve})
    yield dai

@pytest.fixture
def weth_amout(gov, weth):
    weth_amout = 10 ** weth.decimals()
    gov.transfer(weth, weth_amout)
    yield weth_amout


@pytest.fixture
def vault(pm, gov, rewards, guardian, management, token):
    Vault = pm(config["dependencies"][0]).Vault
    vault = guardian.deploy(Vault)
    vault.initialize(token, gov, rewards, "", "", guardian)
    vault.setDepositLimit(2 ** 256 - 1, {"from": gov})
    vault.setManagement(management, {"from": gov})
    yield vault


@pytest.fixture
def strategy(strategist, keeper, vault, Strategy, gov):
    strategy = strategist.deploy(Strategy, vault)
    strategy.setKeeper(keeper)
    vault.addStrategy(strategy, 10_000, 0, 2 ** 256 - 1, 1_000, {"from": gov})
    yield strategy

@pytest.fixture(scope="session")
def RELATIVE_APPROX():
    yield 1e-5
