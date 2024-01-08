pragma solidity ^0.5.16;

import "./shipping_status_contract.sol";

contract MarketplaceContract {
    ShippingStatusContract public shippingStatusContract;

    event NewAlert(address seller, uint price);
    event PurchasedItem(address seller, address buyer, uint price);

    constructor(address shippingStatusContractAddress) public {
        shippingStatusContract = ShippingStatusContract(shippingStatusContractAddress);
    }

    function addItem(address seller, uint price) public {
        // Add an item to the marketplace
        emit NewAlert(seller, price);
    }

    function purchaseItem(address seller, address buyer, uint price) public payable {
        // Purchase an item from the marketplace
        require(msg.sender == buyer, "Only the buyer can purchase items");
        require(shippingStatusContract.getState() == ShippingStatusContract.StateType.ItemAvailable, "Item must be available");
        require(msg.value >= price, "Insufficient funds");

        // Transfer funds from buyer to seller
        address(uint160(seller)).transfer(price);

        // Update the shipping status to "ItemPurchased"
        shippingStatusContract.updateState(ShippingStatusContract.StateType.ItemPurchased);

        emit PurchasedItem(seller, buyer, price);
    }
}
