# SplitEscrow on Arc

USDC escrow + payment splitting on **Arc Mainnet** (chainId 5042) for shared bills, freelance milestones and team payouts.

- Payer funds a deal in native USDC with recipients, % shares (basis points), deadline and memo.
- Payer releases → funds split automatically (rounding dust to last recipient).
- Not released by the deadline → anyone can trigger a refund to the payer.
- Reentrancy-guarded, max 20 recipients, shares must sum to 100%.

## Live on Arc Mainnet
- Contract: [0x2DcAb07de247880D01E3aAf1293B3dd7681E19F1](https://explorer.arc.io/address/0x2DcAb07de247880D01E3aAf1293B3dd7681E19F1)
- Deploy tx: [0x772b47…e0c3](https://explorer.arc.io/tx/0x772b476e27d4ec7d5e52e6e4232ad49e45a7d7e3d69fe343a733108e5fcce0c3)
- Demo deal #0 create (0.05 USDC, 50/50): [0x15ee40…3c2f](https://explorer.arc.io/tx/0x15ee4043a828c4831948836d15bfb0ce3001e3e5d466666e6081016c94c03c2f)
- Demo release: [0x0d85ee…53fd](https://explorer.arc.io/tx/0x0d85ee384c6d3f8eeef83f77c5a0f3fd9ec0ccad3e4e42438d6c2f3d254553fd)

## Web UI
Open `index.html` (or the GitHub Pages site). The mainnet contract is prefilled (override with `?c=<address>`).
1. Click **Connect** with an injected wallet (MetaMask etc.) on Arc Mainnet (RPC `https://rpc.mainnet.arc.io`, chainId 5042, gas token USDC).
2. Create a deal: recipients, shares, amount, deadline, memo.
3. Release as payer, or refund after the deadline.

## Build & test
```
pip install py-solc-x web3 eth-tester py-evm
python build_test.py        # compiles with solc 0.8.24, runs local tests
python deploy.py testnet    # needs your own funded key (not included)
```

## Files
`contracts/SplitEscrow.sol`, `build_test.py`, `deploy.py`, `demo.py`, `web/` (static dApp + ABI), `deployed.mainnet.json`, `demo.mainnet.json`.
