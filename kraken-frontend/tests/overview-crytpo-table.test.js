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
    render(<OverViewCryptoTable />);
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
    expect(elements('tr.cryptoData')).toHaveLength(4);
  });
});
