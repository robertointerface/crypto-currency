import React from 'react';
import 'whatwg-fetch';
import ReactTestUtils, {act} from 'react-dom/test-utils';
import {
  describe,
  it,
  expect,
  beforeEach,
  afterEach,
  jest,
} from '@jest/globals';
import { createContainer } from './dom-manipulators';
import { KrakenCoinForm } from '../src/kraken-symbol-form';
import {
  fetchResponseOk,
  fetchResponseError,
  fetchRequestBody
} from './spy-helpers';

describe('KrakenSymbolForm', () => {
  let render;
  let form;
  let element;
  let field;
  let labelFor;
  beforeEach(() => {
    ({
      render,
      form,
      element,
      field,
      labelFor,
    } = createContainer());
    jest.spyOn(window, 'fetch').mockReturnValue(fetchResponseOk());
  });
  afterEach(() => {
    window.fetch.mockRestore();
  });
  it('KrakenSymbolForm is not Null', () => {
    render(<KrakenCoinForm />);
    expect(form('KrakenSymbolForm')).not.toBeNull();
  });
  const itDisplaysfieldInput = (fieldName) => {
    it(`displays ${fieldName} input`, () => {
      render(<KrakenCoinForm />);
      const fieldInput = field('KrakenSymbolForm', fieldName);
      expect(fieldInput).toBeDefined();
    });
  };
  const itRendersLabel = (labelName, labelText) => {
    it(`renders label for ${labelName}`, () => {
      render(<KrakenCoinForm />);
      const symbolLabel = labelFor(labelName);
      expect(symbolLabel).toBeDefined();
      expect(symbolLabel.textContent).toEqual(labelText);
    });
  };
  const itContainsValue = (fieldId, fieldValue) => {
    it(`field ${fieldId} contains value ${fieldValue}`, () => {
      render(<KrakenCoinForm />);
      const symbolField = field('KrakenSymbolForm', fieldId);
      expect(symbolField.value).toEqual(fieldValue);
    });
  };
  const itModifiesValueWhenChanged = (fieldId, newValue) => {
    it(`modifies value for ${fieldId}`, async () => {
      render(<KrakenCoinForm />);
      const fieldElement = field('KrakenSymbolForm', fieldId);
      ReactTestUtils.Simulate.change(fieldElement, { target: fieldId, value: newValue });
      const newfieldElement = field('KrakenSymbolForm', fieldId);
      expect(newfieldElement.value).toEqual(newValue);
    });
  };
  const itSavesExistingValueWhenSubmitted = (fieldId, newValue, expectedOutput) => {
    it('saves exiting value when submitted', async () => {
      render(<KrakenCoinForm />);
      const fieldElement = field('KrakenSymbolForm', fieldId);
      await ReactTestUtils.Simulate.change(fieldElement, { target: fieldId, value: newValue });
      await ReactTestUtils.Simulate.submit(form('KrakenSymbolForm'));
      expect(fetchRequestBody(window.fetch)).toMatchObject(expectedOutput);
    });
  };
  describe('coin name field', () => {
    itDisplaysfieldInput('coinName');
    itRendersLabel('coinName', 'Symbol Name');
    itContainsValue('coinName', 'symbol name');
    itModifiesValueWhenChanged('coinName', 'Bitcoin');
    itSavesExistingValueWhenSubmitted('coinName',
      'Bitcoin',
      { coinName: 'Bitcoin', coinSymbol: 'BTC' });
  });
  describe('coin symbol field', () => {
    itDisplaysfieldInput('coinSymbol');
    itRendersLabel('coinSymbol', 'coin symbol');
    itContainsValue('coinSymbol', 'BTC');
    itModifiesValueWhenChanged('coinSymbol', 'ETC');
    itSavesExistingValueWhenSubmitted('coinSymbol',
      'ETC',
      { coinName: 'symbol name', coinSymbol: 'ETC' });
  });
});