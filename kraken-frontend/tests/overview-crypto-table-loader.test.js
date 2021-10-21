import React from 'react';
import 'whatwg-fetch';
import {
  jest,
  describe,
  it,
  expect,
  beforeEach,
  afterEach,
} from '@jest/globals';
import { createContainer } from './dom-manipulators';
import {
  fetchResponseOk,
  fetchResponseError,
} from './spy-helpers';
import * as OverViewCryptoTableExport from '../src/overview-crypto-table';
import { OverViewCryptoTableLoader } from '../src/overview-crypto-table-loader';

describe('overview crypto table tests', () => {
  /**
   * Test component OverViewCryptoTableLoader fetches data and passes it down to OverViewCryptoTable
   */
  const fetchData = [
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
  let renderAndWait;
  let element;
  beforeEach(() => {
    ({ renderAndWait, element } = createContainer());
    jest.spyOn(window, 'fetch').mockReturnValue(fetchResponseOk(fetchData));
    // Need to mock OverViewCryptoTable if we want to test what gets passed to it
    jest.spyOn(OverViewCryptoTableExport, 'OverViewCryptoTable').mockReturnValue(null);
  });
  afterEach(() => {
    window.fetch.mockRestore();
  });
  it('useEffect calls correct url', async () => {
    // use act to allow useEffect to complete before we start testing.
    await renderAndWait(<OverViewCryptoTableLoader />);
    expect(window.fetch).toHaveBeenCalledWith('kraken-symbols/', {
      method: 'GET',
      credentials: 'same-origin',
      headers: { 'Content-Type': 'application/json' },
    });
  });
  it('initially passes no data to OverViewCryptoTable', async () => {
    await renderAndWait(<OverViewCryptoTableLoader />);
    expect(OverViewCryptoTableExport.OverViewCryptoTable).toHaveBeenCalledWith(
      { cryptosData: [] }, expect.anything(),
    );
  });
  it('OverViewCryptoTable gets cryptoData once this has been fetched', async () => {
    await renderAndWait(<OverViewCryptoTableLoader />);
    expect(OverViewCryptoTableExport.OverViewCryptoTable).toHaveBeenLastCalledWith(
      { cryptosData: fetchData }, expect.anything(),
    );
  });
  it('displays error if error when fetching data', async () => {
    jest.spyOn(window, 'fetch').mockReturnValue(fetchResponseError());
    await renderAndWait(<OverViewCryptoTableLoader />);
    const errorElement = element('p.error');
    expect(errorElement.textContent).toEqual('error loading data');
  });
});
