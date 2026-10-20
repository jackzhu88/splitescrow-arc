// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title SplitEscrow - USDC escrow that pays out to several recipients by share.
/// @notice On Arc, USDC is the native gas token, so deals are funded with msg.value.
/// A payer funds a deal, then releases it (paid out by basis-point shares) or,
/// after the deadline passes without release, refunds it.
contract SplitEscrow {
    struct Deal {
        address payer;
        uint96 deadline;
        bool settled;
        uint256 amount;
        address[] recipients;
        uint16[] bps; // sums to 10000
        string memo;
    }

    Deal[] private deals;
    uint256 private locked = 1;

    event DealCreated(uint256 indexed id, address indexed payer, uint256 amount, uint256 deadline, string memo);
    event DealReleased(uint256 indexed id);
    event DealRefunded(uint256 indexed id);
    event Paid(uint256 indexed id, address indexed to, uint256 amount);

    modifier nonReentrant() { require(locked == 1, "reentrant"); locked = 2; _; locked = 1; }

    function createDeal(address[] calldata recipients, uint16[] calldata bps, uint96 deadline, string calldata memo)
        external payable returns (uint256 id)
    {
        require(msg.value > 0, "no funds");
        require(recipients.length > 0 && recipients.length <= 20 && recipients.length == bps.length, "bad recipients");
        require(deadline > block.timestamp, "bad deadline");
        uint256 total;
        for (uint256 i; i < bps.length; i++) {
            require(recipients[i] != address(0) && bps[i] > 0, "bad entry");
            total += bps[i];
        }
        require(total == 10000, "bps != 10000");
        id = deals.length;
        deals.push(Deal(msg.sender, deadline, false, msg.value, recipients, bps, memo));
        emit DealCreated(id, msg.sender, msg.value, deadline, memo);
    }

    function release(uint256 id) external nonReentrant {
        Deal storage d = deals[id];
        require(msg.sender == d.payer, "not payer");
        require(!d.settled, "settled");
        d.settled = true;
        uint256 n = d.recipients.length;
        uint256 sent;
        for (uint256 i; i < n; i++) {
            uint256 amt = i == n - 1 ? d.amount - sent : (d.amount * d.bps[i]) / 10000;
            sent += amt;
            (bool ok,) = d.recipients[i].call{value: amt}("");
            require(ok, "pay failed");
            emit Paid(id, d.recipients[i], amt);
        }
        emit DealReleased(id);
    }

    function refund(uint256 id) external nonReentrant {
        Deal storage d = deals[id];
        require(!d.settled, "settled");
        require(block.timestamp > d.deadline, "not expired");
        d.settled = true;
        (bool ok,) = d.payer.call{value: d.amount}("");
        require(ok, "refund failed");
        emit DealRefunded(id);
    }

    function dealCount() external view returns (uint256) { return deals.length; }

    function getDeal(uint256 id) external view returns (
        address payer, uint256 amount, uint256 deadline, bool settled,
        address[] memory recipients, uint16[] memory bps, string memory memo)
    {
        Deal storage d = deals[id];
        return (d.payer, d.amount, d.deadline, d.settled, d.recipients, d.bps, d.memo);
    }
}
