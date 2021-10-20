import React from 'react';
import PropTypes from 'prop-types';

const TABLE_HEADER = ['name', 'open', 'high', 'low', 'close'];

export const OverViewCryptoTable = ({ cryptosData }) => {
  return (
    <>
      {(cryptosData.length > 0)
        ? (
          <table id="crypto-table">
            <thead>
              <tr>
                {TABLE_HEADER.map((header) => <th key={`${header}`}>{header}</th>)}
              </tr>
            </thead>
            <tbody>
              {cryptosData.map((cryptoData) => (
                <CryptoDataRow cryptoInfo={cryptoData} key={cryptoData.name} />
              ))}
            </tbody>
          </table>
        )
        : <p className="errorMessage">Crypto Data Not Available</p>}
    </>
  );
};

OverViewCryptoTable.defaultProps = {
  cryptosData: [],
};
OverViewCryptoTable.propTypes = {
  // eslint-disable-next-line react/forbid-prop-types
  cryptosData: PropTypes.array,
};

export const CryptoDataRow = ({ cryptoInfo }) => {
  // get Crypto name to use it to form keys and the other values might repeat themselves
  // but name is unique
  const CrytoName = cryptoInfo.name;
  return (
    <tr key={`data-${CrytoName}`} className="cryptoData">
      {Object.entries(cryptoInfo).map(
        ([key, value]) => (
          <td key={`${CrytoName}${key}`}>
            {value}
          </td>
        ),
      )}
    </tr>
  );
};
CryptoDataRow.defaultProps = {
  cryptoInfo: {
    name: '',
  },
};
CryptoDataRow.propTypes = {
  // eslint-disable-next-line react/forbid-prop-types
  cryptoInfo: PropTypes.object,
};
