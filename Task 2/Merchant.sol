// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Merchant {
    address public owner;
    
    event Purchase(address indexed buyer, uint amount);

    constructor() {
        owner = msg.sender;
    }

    // Function to simulate the merchant receiving payment
    function buyItem() public payable {
        require(msg.value > 0, "Send Ether to buy item");
        emit Purchase(msg.sender, msg.value);
    }

    // Owner can withdraw funds later
    function withdraw() public {
        require(msg.sender == owner, "Only owner can withdraw funds");
        payable(owner).transfer(address(this).balance);
    }
}
