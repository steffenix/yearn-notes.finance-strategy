// SPDX-License-Identifier: MIT

pragma solidity 0.6.12;
pragma experimental ABIEncoderV2;

interface ITokenGeyser {
  function totalStakedFor(address _addr) external view returns (uint256);
  function totalStaked() external view returns (uint256);
  function token() external view returns (address);
  function totalLocked()  external view returns (uint256);
  function getStakingToken() external view returns (address);
  function getDistributionToken() external view returns (address);
  function stake(uint256 _amount, bytes[32] memory _data) external;
  function stakeFor(address _user, uint256 _amount, bytes[32] memory _data) external;
  function unstake( uint256 _amount, bytes[32] memory _data) external;
  function unstakeQuery( uint256 _amount) external payable;
}
