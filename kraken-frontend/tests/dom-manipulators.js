import ReactDOM from 'react-dom';

export const createContainer = () => {
  const container = document.createElement('div');
  const element = (selector) => container.querySelector(selector);
  const elements = (selector) => Array.from(container.querySelectorAll(selector));
  const form = (formId) => container.querySelector(`form[id="${formId}"]`);
  const field = (formId, fieldName) => form(formId).elements[fieldName];
  const labelFor = (labelElement) => container.querySelector(`label[for="${labelElement}"]`);
  return {
    render: (component) => ReactDOM.render(component, container),
    element,
    elements,
    form,
    field,
    labelFor,
  };
};
