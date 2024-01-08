//interact.js
const MarketplaceContract = artifacts.require("Marketplace"); // Replace "Marketplace" with the actual contract name
const ShippingStatusContract = artifacts.require("ShippingStatus"); // Replace "ShippingStatus" with the actual contract name

module.exports = async function(callback) {
  try {
    const marketplaceInstance = await MarketplaceContract.deployed();
    const shippingStatusInstance = await ShippingStatusContract.deployed();

   // Interact with MarketplaceContract
let marketplaceResult = await marketplaceInstance.someFunction();
console.log("Interacting with MarketplaceContract");
console.log("Marketplace Result:", marketplaceResult);

// Interact with ShippingStatusContract
let shippingStatusResult = await shippingStatusInstance.getState();
console.log("Interacting with ShippingStatusContract");
console.log("Shipping Status:", shippingStatusResult);
  } catch (error) {
    console.error("Error:", error);
  }

  callback(); // This signals the completion of the script to Truffle
};
