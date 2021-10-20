import React from 'react';
import {
  describe,
  it,
  expect,
  beforeEach,
} from '@jest/globals';
import { createContainer } from './dom-manipulators';
import { OverViewCryptoTable, CryptoDataRow } from '../src/overview-crypto-table';

describe('overview table', () => {
  let render;
  let element;
  let elements;
  const cryptoData = [
    {
      name: 'BTCUSD',
      open: 152.21,
      high: 170,
      low: 162,
      close: 165,
    },
    {
      name: 'ETHUSD',
      open: 100.21,
      high: 105,
      low: 95,
      close: 102.78,
    },
    {
      name: 'USDTUSD',
      open: 50,
      high: 58,
      low: 45,
      close: 55.32,
    },
    {
      name: 'ADAUSD',
      open: 25,
      high: 26,
      low: 18,
      close: 20.85,
    },
  ];
  beforeEach(() => {
    ({ render, element, elements } = createContainer());
  });
  it('initially shows a table', () => {
    render(<OverViewCryptoTable cryptosData={cryptoData} />);
    expect(element('table')).not.toBeNull();
  });
  it('CryptoDataRow displays passed crypto info', () => {
    const cryptoInfo = {
      name: 'ADAUSD',
      open: 25,
      high: 26,
      low: 18,
      close: 20.85,
    };
    render(
      <table>
        <tbody>
          <CryptoDataRow cryptoInfo={cryptoInfo} />
        </tbody>
      </table>,
    );
    expect(elements('td')).toHaveLength(Object.keys(cryptoInfo).length);
  });
  it('It displays one row per crypto coin', () => {
    render(<OverViewCryptoTable cryptosData={cryptoData} />);
    expect(elements('tr.cryptoData')).toHaveLength(cryptoData.length);
  });
  it('Does not display the table and displays message when no cryptosData passed', () => {
    render(<OverViewCryptoTable />);
    expect(element('.errorMessage')).not.toBeNull();
    expect(element('.errorMessage').textContent).toEqual('Crypto Data Not Available');
  });
  it('table displays correct data', () => {
    render(<OverViewCryptoTable cryptosData={cryptoData} />);
    const BTCData = elements('.cryptoData')[0];
    expect(BTCData.children).toHaveLength(5);
    expect(BTCData.children[0].textContent).toEqual('BTCUSD');
    expect(BTCData.children[1].textContent).toEqual('152.21');
    expect(BTCData.children[3].textContent).toEqual('162');
  });

});
