A Blockchain Network has been designed to facilitate interaction between two fundamental contracts: the Marketplace Contract and the Shipping Status Contract. The Marketplace Contract governs the functionalities and transactions within the marketplace ecosystem, while the Shipping Status Contract oversees the tracking and management of shipping-related information. This interaction enables seamless coordination between the marketplace operations and the tracking of shipping statuses, ensuring a comprehensive and integrated system for users engaging in transactions within this blockchain environment.


1.Install Python dependencies: bash 
pip install flask 

2.Install Java dependencies: bash 
Install Java Development Kit (JDK)
java -version

3.Install Solidity compiler: bash 
npm install -g solc 


1. Run the blockchain node: (cd .\MarketPlace\) 
bash 
python blockchain_node.py 

2. Run the miner: 
bash
python miner.py 

3. Run the wallet app: 
bash 
python wallet.py 

4. Run the faucet app: 
bash
python faucet.py 

5. Run the block explorer app: 
bash 
java BlockExplorer.java java BlockExplorer

6. Compile the smart contracts: 
(cd MarketPlaceSolutions> truffle compile) or truffle init

7. truffle migrate --network development



open another bash to project folder
10. truffle console

11. truffle(development)>  exec ./interact.js

   
Run node via terminal - node index.js

cd MarketPlace

node index.js

(Then http://localhost:3001 should work)

http://127.0.0.1:5000/ (the Welcome to Blockchain Node! should also be running in localhost)

cd MarketPlaceSolution/MarketPlace (i reinstalled pip install flask) to run functions in that folder. 



TO RUN Program 

cd MarketPlaceSolutions

1.truffle compile  (in case to restart do truffle init) then compile again

2.truffle migrate --network development 

(migrating them to the Ganache development network) 

3.truffle migrate --network goerli (deploying to Goerli network) 

4.truffle console (interact with contract) 

5.truffle develop 

6.truffle(development)> exec ./interact.js 

7.exit - (to get out of truffle development) 








