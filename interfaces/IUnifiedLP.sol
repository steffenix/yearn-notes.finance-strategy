// SPDX-License-Identifier: MIT

pragma solidity 0.6.12;

interface IUnifiedLP {
    function stake(address _lp_addr, uint256 _amount) external returns(bool);
    function redeem(address _lp_addr, uint256 _amount) external returns(bool);
    function lp_balances(address _lp_addr, address owner) external returns(uint256);
}
