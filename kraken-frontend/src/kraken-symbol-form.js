import React, { useState } from 'react';
import PropTypes from 'prop-types';

export const KrakenCoinForm = ({ coinName, coinSymbol, currency }) => {
  const [symbolData, setSymbolData] = useState({
    coinName, coinSymbol, currency,
  });
  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await window.fetch('/kraken-symbols/', {
      method: 'POST',
      credentials: 'same-origin',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(symbolData),
    });
    if (response.ok) {

    }
  };
  const onChangeSymbolData = (e) => {
    e.preventDefault();
    setSymbolData({
      ...symbolData,
      [e.target]: e.value,
    });
  };
  return (
    <form id="KrakenSymbolForm" onSubmit={handleSubmit}>
      <label htmlFor="coinName">
        Symbol Name
        <input
          type="text"
          name="coinName"
          value={symbolData.coinName}
          id="coinName"
          onChange={onChangeSymbolData}
        />
      </label>
      <label htmlFor="coinSymbol">
        coin symbol
        <input
          type="text"
          name="coinSymbol"
          value={symbolData.coinSymbol}
          id="coinSymbol"
          onChange={onChangeSymbolData}
        />
      </label>
      <label htmlFor="currency">
        currency
        <input
          type="text"
          name="currency"
          value={symbolData.currency}
          id="currency"
          onChange={onChangeSymbolData}
        />
      </label>
      <input
        type="submit"
        value="Save"
      />
    </form>
  );
};
KrakenCoinForm.defaultProps = {
  coinName: 'symbol name',
  coinSymbol: 'BTC',
  currency: 'USD',
};
KrakenCoinForm.propTypes = {
  // eslint-disable-next-line react/forbid-prop-types
  coinName: PropTypes.string,
  coinSymbol: PropTypes.string,
  currency: PropTypes.string,
};
