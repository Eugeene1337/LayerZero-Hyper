<div align="center">
  <h1>LayerZero Soft</h1>
  <p>A script designed to simplify your interaction with LayerZero. It provides a range of features that will make it easier for you to work with LayerZero, simplify the management of your farm, and allow you to perform a cost effective route.</p>
</div>

<h2>Installation</h2>

```
git clone https://github.com/Eugeene1337/LayerZero-Hyper.git

cd LayerZero-Hyper

pip install -r requirements.txt

python main.py
```
---
<h2> Modules</h2>
<div>
<h4>1) Route by Krajekis </h4> 
<p>More info: https://teletype.in/@krajekis/LAYERZEROHYPERHYPER</p>
<p><b>Preparation:</b> Before running script you need to withdraw <b>0.56 BNB</b> (~200$) to your wallet</p>
<b>Route:</b>
<ul>
  <li>Bungee Refuel BNB -> Polygon</li>
  <li>Bungee Refuel BNB -> Gnosis</li>
  <li>Swap BNB -> USDT (BSC) on PancakeSwap</li>
  <li>Bridge Bsc USDT -> Base USDC on Stargate with gas on destination</li>
  <li>Bridge Base USDC ->  Bsc USDT on Stargate</li>
  <li>Gas refuel Gnosis -> Celo on Merkly</li>
  <li>Transfer USDT (BSC) to deposit address on exchange</li>
  <li>Swap USDT -> agEUR on PancakeSwap</li>
  <li>Bridge Bsc agEUR -> Gnosis on Angle Money </li>
  <li>Bridge Gnosis agEUR -> Celo on Angle Money</li>
  <li>Bridge Celo agEUR -> Gnosis on Angle Money</li>
  <li>Bridge Gnosis agEUR -> Polygon on Angle Money</li>
  <li>Swap agEUR -> Matic (Polygon) on SushiSwap</li>
  <li>Mint MERKs on Merkly</li>
   <li>Randomly bridge MERKs to chains: opBNB, Core, Harmony, Moonbeam, Moonriver, Tomo, Kava, Dfk, Loot, Conflux</li>
</ul>  
<h4>2) Accounts warmup</h4>
<ul>
  <li>Gas refuel Polygon -> Celo (~0.10$)</li>
</ul>  
</div>


