import ReactDOM from 'react-dom';

export const createContainer = () => {
  const container = document.createElement('div');
  const element = (selector) => container.querySelector(selector);
  const elements = (selector) => Array.from(container.querySelectorAll(selector));
  return {
    render: (component) => ReactDOM.render(component, container),
    element,
    elements,
  };
};
