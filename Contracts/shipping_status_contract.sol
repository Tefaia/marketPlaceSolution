pragma solidity ^0.5.16;

contract ShippingStatusContract {
    enum StateType { ItemAvailable, ItemPurchased }

    StateType public state;

    constructor() public {
        state = StateType.ItemAvailable;
    }

    function updateState(StateType newState) public {
        state = newState;
    }

    function getState() public view returns (StateType) {
        return state;
    }
}
