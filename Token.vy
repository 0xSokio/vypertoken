# @notice A simple Vyper ERC20 Token 

# Token information
name: public(String[64])
symbol: public(String[32])
decimals: public(uint256)
totalSupply: public(uint256)

# Owner balances and allowances
balances: public(HashMap[address, uint256])
allowed: HashMap[address, HashMap[address, uint256]]

# Events
event Transfer:
    _from: address
    _to: address
    _value: uint256

event Approval:
    _owner: address
    _spender: address
    _value: uint256

@external
def __init__(initialSupply: uint256):
    self.name = "Baschke"
    self.symbol = "BASCHK"
    self.decimals = 18
    self.totalSupply = initialSupply
    self.balances[msg.sender] = initialSupply

@external
def transfer(_to: address, _value: uint256) -> bool:
    assert _value <= self.balances[msg.sender]
    self.balances[msg.sender] -= _value
    self.balances[_to] += _value
    log Transfer(msg.sender, _to, _value)
    return True

@external
def approve(_spender: address, _value: uint256) -> bool:
    self.allowed[msg.sender][_spender] = _value
    log Approval(msg.sender, _spender, _value)
    return True

@external
def transferFrom(_from: address, _to: address, _value: uint256) -> bool:
    assert _value <= self.balances[_from]
    assert _value <= self.allowed[_from][msg.sender]
    self.balances[_from] -= _value
    self.balances[_to] += _value
    self.allowed[_from][msg.sender] -= _value
    log Transfer(_from, _to, _value)
    return True

@view
@external
def balanceOf(_owner: address) -> uint256:
    return self.balances[_owner]

@view
@external
def allowance(_owner: address, _spender: address) -> uint256:
    return self.allowed[_owner][_spender]
