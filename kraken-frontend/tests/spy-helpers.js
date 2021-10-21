export const fetchResponseOk = (body) => Promise.resolve({
  ok: true,
  json: () => Promise.resolve(body),
});
export const fetchResponseError = () => Promise.resolve({ ok: false });
export const fetchRequestBody = (fetchSpy) => {
  //console.log(`mock ${JSON.parse(fetchSpy.mock.calls)}`);
  return JSON.parse(fetchSpy.mock.calls[0][1].body);
};
