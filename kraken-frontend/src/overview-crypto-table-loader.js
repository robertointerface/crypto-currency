import React, { useEffect, useState } from 'react';
import { OverViewCryptoTable } from './overview-crypto-table';

export const OverViewCryptoTableLoader = (props) => {
  /**
   * Load kraken symbols on useEffect from backend and pass them down to OverViewCryptoTable.
   */
  const [hasLoadedKrakenSymbols, setHasLoadedKrakenSymbols] = useState(false);
  const [loadedKrakenSymbols, setLoadedKrakenSymbols] = useState([]);
  const [error, setError] = useState('');
  useEffect(() => {
    const fetchKrakenSymbols = async () => {
      const response = await window.fetch('kraken-symbols/', {
        method: 'GET',
        credentials: 'same-origin',
        headers: { 'Content-Type': 'application/json' },
      });
      if (response.ok) {
        setHasLoadedKrakenSymbols(true);
        setLoadedKrakenSymbols(await response.json());
      } else {
        setError('error loading data');
      }
    };
    fetchKrakenSymbols();
  }, []); // with empty array you define to call useEffect only one time at the begining.
  return (
    <>
      {(!error)
        ? (
          <OverViewCryptoTable
            cryptosData={loadedKrakenSymbols}
          />
        )
        : <p className="error">{error}</p>}
    </>
  );
};
